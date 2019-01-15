# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import re
from scrapytest3.spiders.CommonSpider import CommonSpider
from bs4 import BeautifulSoup, UnicodeDammit
from scrapy import Selector


class CanKaoSpider(CommonSpider):
    name = 'CanKao'
    allowed_domains = ['cankaoxiaoxi.com']
    start_urls = [
        'http://www.cankaoxiaoxi.com/',
    ]
    web_name = '参考消息'

    rules = [
        Rule(LinkExtractor(allow=r'http://www.cankaoxiaoxi.com/china/.*htm'), cb_kwargs={'cate': '国内'},
             callback='parseitem', follow=True),  # 财经
        Rule(LinkExtractor(allow=r'http://www.cankaoxiaoxi.com/finance/.*htm'), cb_kwargs={'cate': '财经'},
             callback='parseitem', follow=True),  # 时政
        Rule(LinkExtractor(allow=r'http://www.cankaoxiaoxi.com/mil/.*htm'), cb_kwargs={'cate': '军事'},
             callback='parseitem', follow=True),  # 军事
        Rule(LinkExtractor(allow=r'http://www.cankaoxiaoxi.com/world/.*htm'), cb_kwargs={'cate': '国际'},
             callback='parseitem', follow=True),  # 国际
    ]

    def customerParseItem(self, response, item, **kwargs):
        # 编码规则不一样
        dmt = UnicodeDammit(response.body, override_encodings=['gbk', 'utf-8'], is_html=True)
        text = response.body.decode(dmt.original_encoding, 'ignore')
        sel = Selector(text=text)
        item['source'] = self.web_name
        item["publish_time"] = ''
        item['author'] = ''
        pubtime = sel.xpath('//div[@class="bg-content"]/span[@id="pubtime_baidu"]/text()|'
                            '//div[@class="bg-content"]/span[@class="cor666"]/text()|'
                            '//div[@class="info"]/span[@id="pubtime_baidu"]/text()').extract_first()
        if pubtime:
            item['publish_time'] = pubtime[0:4] + '年' + pubtime[5:7] + '月' + pubtime[8:10] + '日'
        else:
            ss = response.url.split('/')
            timestr = ss[-3] + ss[-2]
            item['publish_time'] = timestr[0:4] + '年' + timestr[4:6] + '月' + timestr[6:8] + '日'
        item['source'] = sel.xpath('//div[@class="bg-content"]/span[@id="source_baidu"]/a/text()|'
                                   '//div[@class="bg-content"]/span[@class="cor666"]/a/text()|'
                                   '//div[@class="info"]/span[@id="source_baidu"]/text()').extract_first().replace(
            '来源：', '')
        item['author'] = sel.xpath(
            '//div[@class="bg-content" or @class="info"]/span[@id="editor_baidu"]/text()').extract_first()
        item['author'] = item['author'].replace('责任编辑：', '') if item['author'] else ''
        return item
