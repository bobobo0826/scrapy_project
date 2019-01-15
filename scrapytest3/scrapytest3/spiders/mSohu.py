# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import re
from scrapytest3.spiders.CommonSpider import CommonSpider
from bs4 import BeautifulSoup
from scrapy import Selector


class NewsChinaSpider(CommonSpider):
    name = 'SoHu'
    allowed_domains = ['sohu.com']
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
    headers = {
        "User-Agent": user_agent
    }
    start_urls = [
        'https://www.sohu.com/',
    ]

    rules = [
        Rule(LinkExtractor(allow=r'https://www.sohu.com/.*\d+'), cb_kwargs={'cate': '11'},
             callback='parseitem', follow=True),
    ]

    def customerParseItem(self, response, item, **kwargs):
        print('customerParseItem')
        sel = Selector(response=response)
        item['publish_time'] = sel.xpath('/html/head/meta[10]/@content').extract_first()[0:10]
        is_content_page = sel.xpath('//*[@id="mp-editor"]').extract_first()
        item['cate'] = sel.xpath('/html/body/div[1]/div[1]/span[2]/em').extract_first()
        return item
