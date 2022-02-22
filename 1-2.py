"""
2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
Найти среди них любое, требующее авторизацию (любого типа).
Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
"""
import requests
import json
from pprint import pprint

api_key = ''
text = 'scraping'
endpoint = f'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key={api_key}&lang=en-ru&text={text}'

resp = requests.get(endpoint)

with open('api_resp.json', 'w', encoding='utf-8') as f:
    json.dump(resp.json(), f, ensure_ascii=False, indent=1)

pprint(resp.json())
