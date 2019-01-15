# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
from scrapytest3.spiders.CommonSpider import CommonSpider
from bs4 import BeautifulSoup, UnicodeDammit
from scrapy import Selector


class NewsChinaSpider(CommonSpider):
    name = 'ZhongGuoXinWen'

    allowed_domains = ['chinanews.com']
    start_urls = [
        'http://www.chinanews.com/',
    ]

    rules = [
        Rule(LinkExtractor(allow=r'http://www.chinanews.com/cj/2018.*shtml'), cb_kwargs={'cate': '财经'},
             callback='parseitem', follow=True),  # 财经
        Rule(LinkExtractor(allow=r'http://www.chinanews.com/gn/.*shtml'), cb_kwargs={'cate': '时政'},
             callback='parseitem', follow=True),  # 时政
        Rule(LinkExtractor(allow=r'http://www.chinanews.com/mil/.*shtml'), cb_kwargs={'cate': '军事'},
             callback='parseitem', follow=True),  # 军事
        Rule(LinkExtractor(allow=r'http://www.chinanews.com/gj/.*shtml'), cb_kwargs={'cate': '国际'},
             callback='parseitem', follow=True),  # 国际
    ]

    def customerParseItem(self, response, item, **kwargs):
        dmt = UnicodeDammit(response.body, override_encodings=['gbk', 'utf-8'], is_html=True)
        text = response.body.decode(dmt.original_encoding, 'ignore')
        sel = Selector(text=text)
        item['source'] = '中国新闻网'
        item["publish_time"] = ''
        item['author'] = ''

        text0 = sel.xpath('//*[@class="left-t"]/text()').extract_first()
        # 获得时间和来源网站
        if text0:
            if "来源" in text0:
                ss = text0.split("来源：")
                item["publish_time"] = ss[0].split(" ")[1].strip()
                item["source"] = ss[1]
        # 获得新闻编辑
        text2 = sel.xpath('//*[@class="left_name"]/text()').extract()
        if text2:
            str1 = ''
            item["author"] = str1.join(text2).strip()
        return item
