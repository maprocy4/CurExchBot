import requests
import json
from config import curs


class APIException(Exception):
    pass

class CurConverter():
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        
        if quote == base:
            raise APIException(f"Невозможно выполнить перевод из {quote} в {base}")

        try:
            quote_ticker = curs[quote]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {quote}.")
        
        try:
            base_ticker = curs[base]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {base}.")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество {amount}.")
        
        r = requests.get(f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}")
        total_base = json.loads(r.content)[curs[base]]

        return total_base
