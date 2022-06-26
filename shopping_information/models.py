import uuid

from django.db import models


class Buyer(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    last_name = models.CharField(max_length=120)
    first_name = models.CharField(max_length=120)


class Shop(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    title = models.CharField(max_length=120)


class PurchasedProducts(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    title = models.CharField(max_length=120)
    amount = models.IntegerField()
    price = models.DecimalField(max_digits=20,  decimal_places=2)
    total_amount = models.DecimalField(max_digits=20,  decimal_places=2)


class PayCheck(models.Model):
    id = models.UUIDField(primary_key=True,
                          default=uuid.uuid4,
                          editable=False)
    buyer = models.ForeignKey(Buyer,
                              on_delete=models.DO_NOTHING,
                              blank=True)
    purchased_products = models.ManyToManyField(PurchasedProducts,
                                                related_name='products')
    date_check = models.DateTimeField(auto_now_add=True)
    shop = models.ForeignKey(Shop,
                             on_delete=models.DO_NOTHING)
    pay_check_sum = models.DecimalField(max_digits=20,  decimal_places=2)

