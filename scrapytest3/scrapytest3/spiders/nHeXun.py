# -*- coding: utf-8 -*-
import scrapy
import time

from bs4 import UnicodeDammit
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import re
from scrapytest3.spiders.CommonSpider import CommonSpider
from scrapy import Selector

RULE_TEXT = './text() | .//p[not(@style) or @style!="display: none;"]//text()[not(ancestor::li) and not(' \
            'parent::script) and not(parent::a) and not(parent::style)] | .//div/text()[not(ancestor::li)] '


class HeXunSpider(CommonSpider):
    name = 'HeXun'
    allowed_domains = ['hexun.com']
    start_urls = [
        'http://www.hexun.com/',
        # "http://news.hexun.com/2018-12-17/195568002.html",
    ]
    web_name = '和讯网'
    div_exclusions = []

    rules = [
        Rule(LinkExtractor(allow=r'http://news.hexun.com/.*htm'), cb_kwargs={'cate': '新闻'}, callback='parseitem',
             follow=True),  # 新闻
        Rule(LinkExtractor(allow=r'http://stock.hexun.com/.*htm'), cb_kwargs={'cate': '股票'}, callback='parseitem',
             follow=True),  # 股票
        Rule(LinkExtractor(allow=r'http://funds.hexun.com/.*htm'), cb_kwargs={'cate': '基金'}, callback='parseitem',
             follow=True),  # 基金
        Rule(LinkExtractor(allow=r'http://tech.hexun.com/.*htm'), cb_kwargs={'cate': '科技'}, callback='parseitem',
             follow=True),  # 科技
        Rule(LinkExtractor(allow=r'http://p2p.hexun.com/.*htm'), cb_kwargs={'cate': 'p2p'}, callback='parseitem',
             follow=True),  # p2p
        Rule(LinkExtractor(allow=r'http://futures.hexun.com/.*htm'), cb_kwargs={'cate': '期货'}, callback='parseitem',
             follow=True),  # 期货
        Rule(LinkExtractor(allow=r'http://insurance.hexun.com/.*htm'), cb_kwargs={'cate': '保险'}, callback='parseitem',
             follow=True),  # 保险
        Rule(LinkExtractor(allow=r'http://bank.hexun.com/.*htm'), cb_kwargs={'cate': '银行'}, callback='parseitem',
             follow=True),  # 银行
    ]

    def customerParseItem(self, response, item, **kwargs):
        dmt = UnicodeDammit(response.body, override_encodings=['gbk', 'utf-8'], is_html=True)
        text = response.body.decode(dmt.original_encoding, 'ignore')
        sel = Selector(text=text)
        # is_content_page = sel.xpath('//div[@class="art_context"]').extract_first()
        item['source'] = self.web_name
        item["publish_time"] = ''
        # if is_content_page:
        text1 = sel.xpath('//div[@class="tip fl"]/span/text()').extract_first()
        if text1:
            time = text1.split(" ")[0]
            if re.match('\d{4}-\d{2}-\d{2}', time):
                cur = time.split("-")
                item['publish_time'] = cur[0] + "年" + cur[1] + "月" + cur[2] + "日"

        pattern = re.compile('责任编辑：[\u4e00-\u9fa5]*')
        text2 = re.search(pattern, response.text)
        if text2:
            item['author'] = text2.group().split("：")[1]
        text3 = sel.xpath('//div[@class="tip fl"]/a/text()').extract_first()
        if text3 is None or text3.strip() == '':
            text3 = sel.xpath('//div[@class="tip fl"]/text()').extract_first()
        if text3 and text3.strip() != "":
            item['source'] = text3.strip()
        return item
