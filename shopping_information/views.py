import datetime

from django.db.models import Prefetch, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from shopping_information import filters
from shopping_information.filters import CheckDateFilter, ShopFilter
from shopping_information.models import PayCheck, PurchasedProducts, Shop, Buyer
from shopping_information.serializers import CreatePayCheckSerialiser, PayCheckListSerializer, ShopSerialiser, \
    ShopListSerialiser, CreatePayChecksSerialiser


class CreateCheckView(generics.CreateAPIView):
    serializer_class = CreatePayChecksSerialiser


class PayCheckListView(generics.ListAPIView):

    queryset = PayCheck.objects.all()
    serializer_class = PayCheckListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = CheckDateFilter


class ShopsListView(generics.ListAPIView):
    queryset = PayCheck.objects.all().distinct('shop__id')
    serializer_class = ShopListSerialiser
    filter_backends = [DjangoFilterBackend]
    filterset_class = ShopFilter


class SumByDateView(APIView):

    def get(self, request):
        start_date = request.query_params['start_date']
        end_date = request.query_params['end_date']

        # TODO возможно еще нужна проверка end_date>start_date
        try:
            start_dt = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return Response("Incorrect data format, should be YYYY-MM-DD", status=400)

        total_sum = PayCheck.objects\
            .filter(date_check__range=[start_dt,
                                       datetime.datetime.combine(end_dt, datetime.time.max)])\
            .aggregate(Sum('pay_check_sum'))
        # total_sum = PayCheck.objects\
        #     .filter(date_check__gte=start_dt, date_check__lte__contains=end_dt)\
        #     .aggregate(Sum('pay_check_sum'))
        return Response(total_sum)
