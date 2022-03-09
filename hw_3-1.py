"""
1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
которая будет добавлять только новые вакансии/продукты в вашу базу.
"""


import random
import requests
from bs4 import BeautifulSoup as soup
import time
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('mongodb://127.0.0.1:27017')
db = client['web_scraping']
vacancies = db.hh_ru_vacancies

position = 'data-engineer'
url = 'https://hh.ru/vacancies/'


def add_to_mongo(vacancies, result_dict):
    if not vacancies.find_one(result_dict):
        vacancies.insert_one(result_dict)


with requests.session() as session:
    session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                                    'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                    'Chrome/98.0.4758.102 Safari/537.36'

    page = 0

    resp = session.get(url + position + f'?page={page}')
    dom = soup(resp.text, 'html.parser')
    last_page = int(dom.find_all('a', {'data-qa': 'pager-page'})[-1].text)

    while resp.ok and page != last_page:

        vacs_on_page = dom.find('div', {'data-qa': 'vacancy-serp__results'})
        vacs_on_page = vacs_on_page.findChildren('div', {'class': 'vacancy-serp-item'}, recursive=False)

        for vac in vacs_on_page:
            url_subt = 'https://hh.ru/vacancy/'

            vac_name = vac.find('a', {'data-qa': 'vacancy-serp__vacancy-title'}).text
            vac_location = vac.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).text.replace('NBSP','')
            vac_href = vac.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href']
            vac_id = int(vac_href.replace(url_subt, '').split('?')[0])
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

            result_dict = {'_id': vac_id,
                           'name': vac_name,
                           'salary_min': min_sal,
                           'salary_max': max_sal,
                           'currency': vac_currency,
                           'link': vac_href,
                           'site_name': vac_site,
                           'city': vac_location,
                           'company': vac_company}

            add_to_mongo(vacancies, result_dict)

        print(f'Page number = {page} was added to mongodb')
        time.sleep(random.randint(1, 3))

        page += 1

print(f'{page} pages was collected in total.')


