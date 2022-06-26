from decimal import Decimal

from django.db import transaction
from rest_framework import serializers

from .models import PayCheck, PurchasedProducts, Buyer, Shop


class ShopSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Shop
        fields = '__all__'


class PurchasedProductsSerialiser(serializers.ModelSerializer):

    class Meta:
        model = PurchasedProducts
        exclude = ['total_amount',]


class AllDataProductsSerialiser(serializers.ModelSerializer):

    class Meta:
        model = PurchasedProducts
        fields = '__all__'


class BuyerSerialiser(serializers.ModelSerializer):

    class Meta:
        model = Buyer
        fields = '__all__'


class CreatePayCheckSerialiser(serializers.ModelSerializer):
    buyer = BuyerSerialiser()
    purchased_products = PurchasedProductsSerialiser(many=True)
    shop = ShopSerialiser()

    class Meta:
        model = PayCheck
        exclude = ('pay_check_sum',)


class CreatePayChecksSerialiser(serializers.ModelSerializer):
    paychecks = CreatePayCheckSerialiser(many=True)

    class Meta:
        model = PayCheck
        fields = ('paychecks',)

    def validate(self, data):
        for dt in data['paychecks']:
            last_name = dt['buyer']['last_name']
            first_name = dt['buyer']['first_name']
            if last_name.isalpha() and first_name.isalpha():
                dt['buyer']['last_name'] = last_name.title()
                dt['buyer']['first_name'] = first_name.title()
            else:
                raise serializers.ValidationError("Incorrect users data")

        return data

    def create(self, validated_data):
        return_data = []
        for v_data in validated_data['paychecks']:
            shop_data = v_data.pop('shop')
            buyer_data = v_data.pop('buyer')
            purchased_products = v_data.pop('purchased_products')
            pay_check_sum = sum(
                [Decimal(purchased_product["price"]) * purchased_product["amount"]
                 for purchased_product in purchased_products]
            )
            with transaction.atomic():

                # TODO эта проверка не нужна,
                #  так как надо привязаться к авторизации и брать пользователя по ID
                if not (buyer := Buyer.objects.filter(last_name=buyer_data["last_name"]).first()):
                    buyer = Buyer.objects.create(**buyer_data)

                # TODO здесь тоже нужна какая то нормальная валидация или таблица,
                #  которая будет пополняться и магазин бедет селектиться из нее
                if not (shop := Shop.objects.filter(title=shop_data["title"]).first()):
                    shop = Shop.objects.create(**shop_data)

                pay_check = PayCheck.objects.create(buyer=buyer,
                                                    shop=shop,
                                                    pay_check_sum=pay_check_sum,
                                                    **v_data)

                for purchased_product in purchased_products:
                    total_amount = Decimal(purchased_product["price"]) * purchased_product["amount"]
                    prod = PurchasedProducts.objects.create(total_amount=total_amount, **purchased_product)
                    pay_check.purchased_products.add(prod)
                return_data.append(pay_check)

        return {"paychecks": return_data}


class PayCheckListSerializer(serializers.ModelSerializer):
    buyer = BuyerSerialiser(read_only=True)
    purchased_products = AllDataProductsSerialiser(read_only=True, many=True)
    shop = ShopSerialiser(read_only=True)

    class Meta:
        model = PayCheck
        fields = '__all__'


class ShopListSerialiser(serializers.ModelSerializer):
    shop = ShopSerialiser(read_only=True)

    class Meta:
        model = PayCheck
        fields = ['shop']


class SumByDateSerializer(serializers.Serializer):
   total_sum = serializers.DecimalField(max_digits=20,  decimal_places=2)
