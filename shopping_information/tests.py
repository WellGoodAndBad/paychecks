import datetime
from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APIClient


# from .models import Task


class ShopInformationTests(TestCase):

    client = APIClient()
    test_paycheck = {
        "buyer": {"last_name": "ANDERSON", "first_name": "toM"},
        "shop": {"title": "LENTA"},
        "purchased_products": [
            {"title": "Red Chilly", "amount": 3, "price": 42.31},
            {"title": "Icecream", "amount": 4, "price": 2.55}
        ]
    }
    test_paycheck_two = {
        "buyer": {"last_name": "Smith", "first_name": "agent"},
        "shop": {"title": "Mega"},
        "purchased_products": [
            {"title": "Meat", "amount": 1, "price": 66.99},
            {"title": "Tea", "amount": 9, "price": 7.11}
        ]
    }

    create_paychecks = {
        "paychecks": [
            test_paycheck,
            test_paycheck_two,
        ]
    }
    cur_date = datetime.datetime.today().strftime("%Y-%m-%d")

    def test_create_task(self):

        resp = self.client.post(path='/api/v1/create_paycheck',
                                data=self.create_paychecks,
                                content_type="application/json")
        self.assertEqual(resp.status_code, 201)

    def test_get_paychecks(self):

        resp = self.client.post(path='/api/v1/create_paycheck',
                                data=self.create_paychecks,
                                content_type="application/json")
        user_id = resp.data['paychecks'][0]['buyer']['id']
        self.assertEqual(resp.status_code, 201)

        # Все чеки
        resp = self.client.get('/api/v1/paychecks')
        self.assertEqual(len(resp.data), 2)
        self.assertEqual(resp.status_code, 200)

        # все чеки за дату
        resp = self.client.get(f'/api/v1/paychecks?date_check={self.cur_date}')
        self.assertEqual(len(resp.data), 2)
        self.assertEqual(resp.status_code, 200)

        # все чеки для одного клиента(список товаров одного покупателя)
        resp = self.client.get(f'/api/v1/paychecks?buyer={user_id}')
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.status_code, 200)

        # все чеки в интервале дат
        resp = self.client.get(f'/api/v1/paychecks?start_date=2022-01-01&end_date=2022-01-29')
        self.assertEqual(len(resp.data), 0)
        self.assertEqual(resp.status_code, 200)

    def test_user_shops(self):

        resp = self.client.post(path='/api/v1/create_paycheck',
                                data=self.create_paychecks,
                                content_type="application/json")
        user_id = resp.data['paychecks'][0]['buyer']['id']
        resp = self.client.get(f'/api/v1/user_shops?buyer={user_id}')
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.status_code, 200)

    def test_sum_by_date_range(self):

        self.client.post(path='/api/v1/create_paycheck',
                         data=self.create_paychecks,
                         content_type="application/json")
        resp = self.client.get(f'/api/v1/sum_by_dates?start_date=2022-05-01&end_date={self.cur_date}')
        self.assertEqual(float(resp.data['pay_check_sum__sum']), 268.11)
        self.assertEqual(resp.status_code, 200)
