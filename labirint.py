import scrapy
from scrapy.http import HtmlResponse
from bookspider.items import BookspiderItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/genres/2304/?page=1']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@title="Следующая"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath('//*[@id="catalog"]/div/div[3]/div/div[4]'
                               '/div/div/div/div[1]/div/div[1]/a/@href').getall()
        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        href = response.url
        name = response.xpath('//h1/text()').get()
        author = response.xpath('//a[@data-event-label="author"]/text()').get()
        price = response.xpath('//span[@class="buying-priceold-val-number"]/text()').get()
        sale_price = response.xpath('//span[@class="buying-pricenew-val-number"]/text()').get()
        rating = response.xpath('//div[@id="rate"]/text()').get()

        yield BookspiderItem(href=href, name=name,
                             author=author, price=price,
                             sale_price=sale_price, rating=rating)
