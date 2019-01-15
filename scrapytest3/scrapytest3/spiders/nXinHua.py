# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import re
from scrapytest3.spiders.CommonSpider import CommonSpider
from bs4 import BeautifulSoup
from scrapy import Selector


class XinHuaSpider(CommonSpider):
    name = 'XinHua'
    allowed_domains = ['xinhuanet.com']
    start_urls = [
        'http://www.xinhuanet.com',
    ]
    rules = [
        Rule(LinkExtractor(allow=r'http://www.xinhuanet.com/politics/.*\d+\.htm'), cb_kwargs={'cate': '时政'},
             callback='parseitem', follow=True),  # 财经
        Rule(LinkExtractor(allow=r'http://www.xinhuanet.com/fortune/.*\d+\.htm'), cb_kwargs={'cate': '财经'},
             callback='parseitem', follow=True),  # 时政
        Rule(LinkExtractor(allow=r'http://www.xinhuanet.com/mil/.*\d+\.htm'), cb_kwargs={'cate': '军事'},
             callback='parseitem', follow=True),  # 军事
        Rule(LinkExtractor(allow=r'http://www.xinhuanet.com/world/.*\d+\.htm'), cb_kwargs={'cate': '国际'},
             callback='parseitem', follow=True),  # 国际
    ]

    def customerParseItem(self, response, item, **kwargs):
        sel = Selector(response=response)
        is_content_page = sel.xpath('//div[@class="main"]').extract_first()
        item["publish_time"] = ''
        item['author'] = ''
        if is_content_page:
            text0 = sel.xpath('//*[@class="h-time"]/text()').extract_first()
            if text0:
                time = text0.split(" ")[1]
                if re.match("^\d{4}-\d{2}-\d{2}$", time):
                    ymd = time.split("-")
                    item["publish_time"] = "%s年%s月%s日" % (ymd[0], ymd[1], ymd[2])

            text1 = sel.xpath('//*[@id="source"]/text()').extract_first()
            if text1:
                item['source'] = text1.replace(" ", "")

            text2 = sel.xpath('//*[@class="p-jc"]/text()').extract()
            if text2:
                for i in text2:
                    if "责任编辑" in i:
                        item['author'] = i.split("：")[1].replace("\r\n", "")
        else:
            item['handle'] = 2  # 非内容页处理标记为2

        return item
