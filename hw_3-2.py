"""
2. Написать функцию, которая производит поиск и выводит на экран вакансии
с заработной платой больше введённой суммы (необходимо анализировать оба поля зарплаты).
"""

from pymongo import MongoClient
from pprint import pprint

client = MongoClient('mongodb://127.0.0.1:27017')

db = client['web_scraping']
vacancies = db.hh_ru_vacancies


def salary_gte(collection, value):
    for i in collection.find({'$or': [{'salary_min': {'$gte': value}}, {'salary_max': {'$gte': value}}]}):
        yield i


[pprint(i) for i in salary_gte(vacancies, 100000)]





