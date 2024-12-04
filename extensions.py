import requests
import json

from telebot.types import KeyboardButtonRequestUser


class APIException(Exception):
    pass
class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: float):
        try:
            base_ticker = {'доллар': 'USD', 'евро': 'EUR', 'рубль': 'RUB'}.get(base.lower())
            quote_ticker = {'доллар': 'USD', 'евро': 'EUR', 'рубль': 'RUB'}.get(quote.lower())
            if not base_ticker or not quote_ticker:
                raise APIException('Неизвестная валюта')
            if base_ticker == quote_ticker:
                raise APIException('Нельзя переводить в ту же валюту')

            r = requests.get(f'https://api.exchangerate-api.com/v4/latest/{base_ticker}')
            r.raise_for_status()
            result = json.loads(r.content)['rates'][quote_ticker]
            return round(result * amount,2)

        except requests.exceptions.RequestException as e:
            raise APIException(f"Ошибка сети: {e}")
        except json.JSONDecodeError as e:
            raise APIException (f"Ошибка JSON: {e}")
        except KeyError as e:
            raise APIException(f"Неизвестная валюта в API: {e}")