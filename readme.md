## rest-api tasks managers
- docker-compose build
- docker-compose up

##### Создание чеков POST /api/v1/create_paycheck 

{"paychecks": [{
  "buyer": {"last_name": "foX", "first_name": "brone"},
  "shop": {"title": "OPP"},
  "purchased_products": [
      {"title": "CHILLY", "amount": 3, "price": 42.55},
      {"title": "icecream", "amount": 4, "price": 4.55}]
},
{
  "buyer": {"last_name": "Bob", "first_name": "Yellow"},
  "shop": {"title": "777"},
  "purchased_products": [
      {"title": "tomate", "amount": 2, "price": 4.75},
      {"title": "icecream", "amount": 4, "price": 4.55}]
}]}

##### для получения Чеков: - /api/v1/paychecks
query параметры
* start_date', 'end_date' - чеки в интервале дат
* 'date_check' - чеки за конкретную дату
* 'buyer' - список чеков конкретного покупателя("он же список продуктов покупателя)

##### список магазинов: - /api/v1/user_shops
query параметры
* buyer (UUID format) - id покупителя в базе

##### сумма чеков в интервале дат: - /api/v1/sum_by_dates?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD



