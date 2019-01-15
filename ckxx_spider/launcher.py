from scrapy.crawler import CrawlerProcess

from ckxx_spider.spiders.ckxx_spider import CkxxSpider

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(CkxxSpider)
    process.start() # the script will block here until all crawling jobs are finished