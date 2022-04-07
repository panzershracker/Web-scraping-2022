from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from castoparser import settings
from castoparser.spiders.castorama import CastoramaSpider


if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(CastoramaSpider)
    crawler_process.start()

