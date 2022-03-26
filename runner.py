from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from bookspider import settings
from bookspider.spiders.labirint import LabirintSpider


if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(LabirintSpider)
    crawler_process.start()

