from django_filters import DateTimeFilter, CharFilter
from django_filters.rest_framework import FilterSet

from shopping_information.models import PayCheck


class CheckDateFilter(FilterSet):
    start_date = DateTimeFilter(field_name="date_check", lookup_expr="gte")
    end_date = DateTimeFilter(field_name="date_check", lookup_expr="lte")
    date_check = DateTimeFilter(field_name="date_check__date")
    buyer = CharFilter(field_name='buyer__id')

    class Meta:
        model = PayCheck
        fields = ['start_date', 'end_date', 'date_check', 'buyer']


class ShopFilter(FilterSet):
    buyer = CharFilter(field_name='buyer__id')

    class Meta:
        model = PayCheck
        fields = ['buyer']
