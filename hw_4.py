"""
Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
Для парсинга использовать XPath. Структура данных должна содержать:
название источника;
наименование новости;
ссылку на новость;
дата публикации.
Сложить собранные новости в БД
"""
from lxml import html
import requests
from datetime import datetime
from pymongo import MongoClient
from pprint import pprint

url = 'https://lenta.ru/'

client = MongoClient('mongodb://127.0.0.1:27017')
db = client['web_scraping']
news = db.lenta_news


def show_news():
    for i in news.find({}):
        yield i


def add_to_mongo(news, dict):
    if not news.find_one(dict):
        news.insert_one(dict)


def create_dict(title, link):

    result_dict = {'source': url,
                   'title': title,
                   'link': link,
                   'date': str(datetime.now().date())}

    return result_dict


with requests.session() as session:
    session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
                                    'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                                    'Chrome/98.0.4758.102 Safari/537.36'

    response = requests.get(url)

    dom = html.fromstring(response.text)

    main_new = dom.xpath('//div[@class="topnews__first-topic"]')
    main_new_link = main_new[0].xpath('.//a[@class="card-big _topnews _news"]/@href')
    main_new_title = main_new[0].xpath('.//h3[@class="card-big__title"]/text()')

    result = create_dict(main_new_title, main_new_link)
    add_to_mongo(news, result)

    news_grid = dom.xpath('//a[@class="card-mini _topnews"]')
    for i in news_grid:
        small_link = i.xpath('./@href')[0]
        small_title = i.xpath('.//span[@class="card-mini__title"]/text()')[0]
        if not small_link.startswith('http'):
            small_link = url[:-1] + small_link

        result = create_dict(small_title, small_link)
        add_to_mongo(news, result)


# [pprint(i) for i in show_news()]