from scrapy.crawler import CrawlerProcess

from ppxw_spider.spiders.ppxw_spider import PpxwSpider

if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(PpxwSpider)
    process.start() # the script will block here until all crawling jobs are finished