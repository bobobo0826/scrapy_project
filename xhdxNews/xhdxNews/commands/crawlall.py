#encoding=utf-8
from scrapy.commands import ScrapyCommand

from xhdxNews import settings
import pymongo
import time
import requests
import logging

from xhdxNews.statistics import Statistics
from scrapy.utils.project import get_project_settings

class Command(ScrapyCommand):
    requires_project = True
    def __init__(self):
        self.stat=Statistics()
        self.logging=logging.getLogger(__name__)
        self.client=pymongo.MongoClient(host="localhost",port=27017)
        self.db=self.client["xhdx_db"]
    def syntax(self):
        return '[options]'
    def short_desc(self):
        return 'Runs all of the spiders'
    def run(self, args, opts):
        print("===================run===============")
        self.stat.start_time()
        spider_list=self.crawler_process.spider_loader.list()
        for name in spider_list:
            self.crawler_process.crawl(name, **opts.__dict__)
        self.crawler_process.start()
        #爬取结束
        self.logging.warning("All spider Closed")
        self.stat.end_time()
        self.stat.json_display()