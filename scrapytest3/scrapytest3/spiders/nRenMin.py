import logging
import os
import re

from bs4 import UnicodeDammit
from scrapy import Request, Selector, FormRequest

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

from scrapytest3.spiders.CommonSpider import CommonSpider


class RmwSpider(CommonSpider):
    name = "RenMin"
    allowed_domains = ['people.com.cn']
    start_urls = ["http://www.people.com.cn/"]
    content_xpaths = []

    rules = [
        Rule(LinkExtractor(allow=r'http://politics.people.com.cn/.*htm'), cb_kwargs={'cate': '政治'},
             callback='parseitem', follow=True),
        Rule(LinkExtractor(allow=r'http://world.people.com.cn/.*htm'), cb_kwargs={'cate': '国际'},
             callback='parseitem', follow=True),
        Rule(LinkExtractor(allow=r'http://military.people.com.cn/.*htm'), cb_kwargs={'cate': '军事'},
             callback='parseitem', follow=True),
        Rule(LinkExtractor(allow=r'http://finance.people.com.cn/.*htm'), cb_kwargs={'cate': '财经'},
             callback='parseitem', follow=True),
        Rule(LinkExtractor(allow=r'http://money.people.com.cn/.*htm'), cb_kwargs={'cate': '金融'},
             callback='parseitem', follow=True),
    ]

    def customerParseItem(self, response, item, **kwargs):
        dmt = UnicodeDammit(response.body, override_encodings=['gbk', 'utf-8'], is_html=True)
        text = response.body.decode(dmt.original_encoding, 'ignore')
        sel = Selector(text=text)
        url_segments = response.url.split("/")
        item['publish_time'] = ''
        if len(url_segments) > 3:
            year = re.match(re.compile('^\d{4}$'), url_segments[-3])
            month_day = re.match(re.compile('^\d{4}$'), url_segments[-2])
            if year and month_day:
                # 在允许屏道内，且含日期的url,判断为内容页
                item['publish_time'] = u"{0}年{1}月{2}日".format(url_segments[-3],
                                                              url_segments[-2][:2], url_segments[-2][2:])
        item['source'] = sel.xpath('//div[@class="box01"]/div[@class="fl"]/a/text()'
                                   '|//div[@class="fr"]/a/text()'
                                   '|//p[@class="sou"]/span[@id="p_origin"]/a/text()').extract_first()
        item['author'] = sel.xpath('//div/p[@class="author"]/text() | //div[@class="edit clearfix"]/text()').extract_first()
        return item
