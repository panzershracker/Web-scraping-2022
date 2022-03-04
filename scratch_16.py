"""
Необходимо собрать информацию о вакансиях на вводимую должность
(используем input или через аргументы получаем должность) с сайтов HH(обязательно)
и/или Superjob(по желанию).
Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
Получившийся список должен содержать в себе минимум:
-Наименование вакансии.
-Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
-Ссылку на саму вакансию.
-Сайт, откуда собрана вакансия.
-По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов.
Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv.
"""
import random

import requests
from bs4 import BeautifulSoup as soup
from pprint import pprint
import pandas as pd
import time
from tabulate import tabulate

position = 'data-engineer'
url = 'https://hh.ru/vacancies/'
columns = ['name', 'salary_min', 'salary_max', 'currency', 'link', 'site_name', 'city', 'company']
df = pd.DataFrame(columns=columns)

with requests.session() as session:
    session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                                    'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                    'Chrome/98.0.4758.102 Safari/537.36'

    page = 0

    resp = session.get(url + position + f'?page={page}')

    while resp.ok and page != 50:
        dom = soup(resp.text, 'html.parser')

        vacs_on_page = dom.find('div', {'data-qa': 'vacancy-serp__results'})
        vacs_on_page = vacs_on_page.findChildren('div', {'class': 'vacancy-serp-item'}, recursive=False)

        for vac in vacs_on_page:

            vac_name = vac.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).text
            vac_location = vac.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text.replace('NBSP','')
            vac_href = vac.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).href
            vac_company = vac.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'}).text
            vac_sal = vac.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            vac_site = 'https://hh.ru/'
            vac_currency = None
            min_sal, max_sal = None, None

            if vac_sal is not None:
                vac_sal = vac_sal.text
                vac_currency = vac_sal[-4:].strip()

                min_sal, max_sal = min_sal, max_sal

                if vac_sal.startswith('от'):
                    min_sal = int(''.join(i for i in vac_sal if i.isdigit()))

                elif vac_sal.startswith('до'):
                    max_sal = int(''.join(i for i in vac_sal if i.isdigit()))

                elif vac_sal[0].isdigit():
                    min_sal, max_sal = vac_sal.split('–')

                    min_sal = int(min_sal.replace('\u202f', ''))
                    max_sal = int(max_sal.replace('\u202f', '')[:-4])

            else:
                vac_sal = None

            new_row = pd.DataFrame([{'name': vac_name,
                                     'salary_min': min_sal,
                                     'salary_max': max_sal,
                                     'currency': vac_currency,
                                     'link': vac_href,
                                     'site_name': vac_site,
                                     'city': vac_location,
                                     'company': vac_company}],
                                   columns=columns)

            df = pd.concat([df, new_row], ignore_index=True)

        print(f'Page number = {page} was collected')
        time.sleep(random.randint(1, 3))
        df.to_csv(f'hh_vacancies_{position}.csv', index=False)

        page += 1

print(f'{page} pages was collected in total.')
# print(tabulate(df, headers='keys'))
