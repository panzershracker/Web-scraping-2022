import scrapy
from scrapy.http import HtmlResponse
from castoparser.items import CastoparserItem
from scrapy.loader import ItemLoader


class CastoramaSpider(scrapy.Spider):
    name = 'castorama'
    allowed_domains = ['castorama.ru']
    start_urls = ['https://www.castorama.ru/tools/power-tools']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@title="След."]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        links = response.xpath('//div[@class="category-products"]/ul/li/a[1]')
        for link in links:
            yield response.follow(link, callback=self.link_parse)

    def link_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=CastoparserItem(), response=response)

        loader.add_value('_id', response.url.split('/')[-1])
        loader.add_value('url', response.url)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('price', '(//span[@class="regular-price"]//span/text())[1]')
        loader.add_xpath('photo', '//img[contains(@class, "top-slide__img")]/@data-src')
        loader.add_xpath('specs_labels', '//*[contains(@class, "product-specifications")]//*[contains(@class, "specs-table__attribute-name ")]/text()')
        loader.add_xpath('specs_values', '//*[contains(@class, "product-specifications")]//*[contains(@class, "specs-table__attribute-value")]/text()')
        loader.add_value('specs', None)

        yield loader.load_item()

        # _id = response.url.split('/')[-1]
        # href = response.url
        # name = response.xpath().get()
        # price = response.xpath('//span[@class="price"]/span/span/text()[1]').get()
        # photo = response.xpath('//img[contains(@class, "top-slide__img")]/@data-src').getall()
        # yield CastoparserItem(href=href, name=name, price=price, photo=photo)
