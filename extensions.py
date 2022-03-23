import requests
import json
from config import keys

class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert ( quote:str, base: str, amount: str):

        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты{base}.')

        try:
            q_ticket = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту{quote}')

        try:
            b_ticket = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту{base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать колличество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={q_ticket}&tsyms={b_ticket}')
        total_base = json.loads(r.content)[keys[base]]
        return total_base