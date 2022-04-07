# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, Compose, TakeFirst


def int_price(raw_price):
    price = raw_price[0].replace('', '')
    try:
        price = int(price)
    except:
        return price
    return price


def strip_items(strings_list):
    return [i.strip() for i in strings_list]


class CastoparserItem(scrapy.Item):
    _id = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=Compose(int_price))
    photo = scrapy.Field()
    specs_labels = scrapy.Field(input_processor=Compose(strip_items))
    specs_values = scrapy.Field(input_processor=Compose(strip_items))
    specs = scrapy.Field()
    print()
