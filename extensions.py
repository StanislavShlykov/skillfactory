from config import keys,api
import requests
import json
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="Tester")

class BotException(Exception):
    pass

class BotLogic:
    @staticmethod
    def convert(base:str, tar:str, val:float):
        if base == tar:
            raise BotException(f'Невозможно конвертировать одинаковые валюты {base}')

        try:
            base_tic = keys[base]
        except KeyError:
            raise BotException(f'Введите корректно валюту {base}')

        try:
            tar_tic = keys[tar]
        except KeyError:
            raise BotException(f'Введите корректно валюту {tar}')

        try:
            val = float(val)
        except ValueError:
            raise BotException(f'Введите корректно количество валюты {val}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_tic}&tsyms={tar_tic}')
        text = round(json.loads(r.content)[tar_tic] * float(val), 2)

        return text

    @staticmethod
    def weather(param):
        location = geolocator.geocode(param)
        r = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?lat={location.latitude}&lon={location.longitude}&appid={api}&units=metric&lang=ru')
        content = json.loads(r.content)
        temp = content['main']['temp']
        temp_min = content['main']['temp_min']
        temp_max = content['main']['temp_max']
        description = content['weather'][0]['description'].capitalize()
        text = f'{location}\n{description}\nТемпература-->{temp}\nМакс.Температура-->{temp_max}\nМин.Температура-->{temp_min}'
        return text
