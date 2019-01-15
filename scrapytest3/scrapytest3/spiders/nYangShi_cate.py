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
    name = 'YangShi'
    allowed_domains = ['cctv.com']
    start_urls = [
        'http://www.cctv.com/',
    ]

    rules = [
        Rule(LinkExtractor(allow=r'http://news.cctv.com/china/.*htm'), cb_kwargs={'cate': '国内'}, callback='parseitem',
             follow=True),  # 国内
        Rule(LinkExtractor(allow=r'http://military.cctv.com/.*htm'), cb_kwargs={'cate': '军事'}, callback='parseitem',
             follow=True),  # 军事
        # Rule(LinkExtractor(allow=r'http://www.xinhuanet.com/world/.*htm'), cb_kwargs={'cate': '国际'},
        #      callback='parseitem', follow=True),  # 国际
    ]

    def customerParseItem(self, response, item, **kwargs):
        print('customerParseItem')
        sel = Selector(response=response)
        item["publish_time"] = ''
        item['author'] = ''
        text0 = sel.xpath('//*[@class="info"]/i/a/text()').extract_first()
        if text0:
            item['source'] = text0.split(" ")[0]
        text1 = sel.xpath('//*[@class="info"]/i/text()').extract()
        if text1:
            for i in text1:
                if "年" in i:
                    pattern = re.compile('\d{4}年\d{2}月\d{2}日')
                    time = re.search(pattern, i)
                    item['publish_time'] = time.group()

        return item
