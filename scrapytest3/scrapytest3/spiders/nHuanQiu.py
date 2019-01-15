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
    name = 'HuanQiu'
    allowed_domains = ['huanqiu.com']
    start_urls = [
        'http://www.huanqiu.com/',
    ]
    web_name = '环球网'

    rules = [
        Rule(LinkExtractor(allow=r'http://china.huanqiu.com/.*htm'), cb_kwargs={'cate': '国内'}, callback='parseitem',
             follow=True),  # 国内
        Rule(LinkExtractor(allow=r'http://taiwan.huanqiu.com/.*htm'), cb_kwargs={'cate': '台湾'}, callback='parseitem',
             follow=True),  # 台湾
        Rule(LinkExtractor(allow=r'http://mil.huanqiu.com/.*htm'), cb_kwargs={'cate': '军事'}, callback='parseitem',
             follow=True),  # 军事
        Rule(LinkExtractor(allow=r'http://world.huanqiu.com/.*htm'), cb_kwargs={'cate': '国际'}, callback='parseitem',
             follow=True),  # 国际
        Rule(LinkExtractor(allow=r'http://opinion.huanqiu.com/.*htm'), cb_kwargs={'cate': '评论'}, callback='parseitem',
             follow=True),  # 评论
        Rule(LinkExtractor(allow=r'http://finance.huanqiu.com/.*htm'), cb_kwargs={'cate': '财经'}, callback='parseitem',
             follow=True),  # 财经
        Rule(LinkExtractor(allow=r'http://tech.huanqiu.com/.*htm'), cb_kwargs={'cate': '科技'}, callback='parseitem',
             follow=True),  # 科技

    ]

    def customerParseItem(self, response, item, **kwargs):
        sel = Selector(response=response)
        is_content_page = sel.xpath('//div[@class="la_con"]').extract_first()
        item['source'] = self.web_name
        item["publish_time"] = ''
        if is_content_page:
            text1 = sel.xpath('//*[@class="la_t_a"]/text()').extract_first()
            if text1:
                time = text1.split(" ")[0]
                if re.match('\d{4}-\d{2}-\d{2}', time):
                    cur = time.split("-")
                    item['publish_time'] = cur[0] + "年" + cur[1] + "月" + cur[2] + "日"
            text3 = sel.xpath('//*[@class="la_t_b"]/a/text()').extract_first()
            if text3 and text3.strip() != "":
                item['source'] = text3.strip()

        else:
            item['handle'] = 2  # 非内容页处理标记为2

        return item
