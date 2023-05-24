import json
import requests
from config import keys


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, quote, amount):
        try:
            base_key = keys[base]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            quote_key = keys[quote]
        except KeyError:
            raise APIException(f"Валюта {quote} не найдена!")

        if base_key == quote_key:
            raise APIException(f'Невозможно конвертировать одинаковую валюту {base}!')

        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIException(f'Не верно указано количество {amount}!')

        url = f"https://api.apilayer.com/exchangerates_data/convert?to={quote_key}&from={base_key}&amount={amount}"
        payload = {}
        headers = {"apikey": "2wNbVZ8KHIECAiSGP7OjeHhD4Cu5PaBK"}
        response = requests.get(url, headers=headers, data=payload)
        total_base = json.loads(response.content)['result']
        new_price = float(total_base)
        new_price = round(new_price, 3)
        message = f"Цена {amount} {base} в {quote} : {new_price}"
        return message