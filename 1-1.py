"""
1. Посмотреть документацию к API GitHub,
разобраться как вывести список репозиториев для конкретного пользователя,
сохранить JSON-вывод в файле *.json.
"""

import requests
from pprint import pprint
import json

name = 'panzershracker'

resp = requests.get(f'https://api.github.com/users/{name}/repos')

repos_dict = {i['name']: i['html_url'] for i in resp.json()}

with open(f'{name}_repos.json', 'w', encoding='utf-8') as f:
    json.dump(repos_dict, f, ensure_ascii=False, indent=1)

pprint(repos_dict)









