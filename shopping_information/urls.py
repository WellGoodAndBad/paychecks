from django.urls import path
from . import views


urlpatterns = [
    path('paychecks', views.PayCheckListView.as_view()),
    path('create_paycheck', views.CreateCheckView.as_view()),
    path('user_shops', views.ShopsListView.as_view()),
    path('sum_by_dates', views.SumByDateView.as_view()),
]
