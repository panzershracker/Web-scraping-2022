# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient

class BookspiderPipeline:
    def __init__(self):
        client = MongoClient('mongodb://127.0.0.1:27017')
        self.db = client.web_scraping

    def process_item(self, item, spider):
        item['_id'] = self.id_from_href(item)

        collection = self.db[spider.name]
        collection.insert_one(item)
        return item

    def id_from_href(self, item: ItemAdapter):
        return int(item['href'].split('/')[-2])


