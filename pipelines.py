# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import os
import castoparser.settings
import hashlib


def specs_zip(labels, values):
    specs = dict(zip(labels, values))
    return specs

class CastoparserPipeline:
    def __init__(self):
        client = MongoClient('mongodb://127.0.0.1:27017')
        self.db = client.web_scraping

    def new_item(self, item):
        item['specs'] = specs_zip(item['specs_labels'], item['specs_values'])
        del item['specs_labels']
        del item['specs_values']

        return item

    def process_item(self, item, spider):
        new_item = self.new_item(item)

        collection = self.db[spider.name]
        collection.insert_one(new_item)


class CastoPhotosPipeLine(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photo']:
            for img in item['photo']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photo'] = [itm[1] for itm in results if itm[0]]
        print()
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        file_name = request.url.split('/')[-1]
        path = item['name'] + '/' + file_name
        return path

