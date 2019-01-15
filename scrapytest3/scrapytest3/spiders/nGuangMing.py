# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
from scrapytest3.spiders.CommonSpider import CommonSpider
from bs4 import BeautifulSoup, UnicodeDammit
from scrapy import Selector


class GmwSpider(CommonSpider):
    name = 'GuangMing'
    web_name = '光明网'
    allowed_domains = ['gmw.cn']
    start_urls = [
        "http://www.gmw.cn/",
    ]
    div_exclusions = []
    content_xpaths = []  # 初始化已找到的xpath

    rules = [
        Rule(LinkExtractor(allow=r'http://politics.gmw.cn/.*htm'), cb_kwargs={'cate': '时政'}, callback='parseitem',
             follow=True),
        Rule(LinkExtractor(allow=r'http://world.gmw.cn/.*htm'), cb_kwargs={'cate': '国际'}, callback='parseitem',
             follow=True),
        Rule(LinkExtractor(allow=r'http://guancha.gmw.cn/.*htm'), cb_kwargs={'cate': '时评'}, callback='parseitem',
             follow=True),
        Rule(LinkExtractor(allow=r'http://economy.gmw.cn/.*htm'), cb_kwargs={'cate': '经济'}, callback='parseitem',
             follow=True),
        Rule(LinkExtractor(allow=r'http://mil.gmw.cn//.*htm'), cb_kwargs={'cate': '军事'}, callback='parseitem',
             follow=True),
    ]

    def customerParseItem(self, response, item, **kwargs):
        dmt = UnicodeDammit(response.body, override_encodings=['gbk', 'utf-8'], is_html=True)
        text = response.body.decode(dmt.original_encoding, 'ignore')
        sel = Selector(text=text)
        # is_content_page = sel.xpath('//div[@class="art_context"]').extract_first()
        source = sel.xpath('//span[@id="source"]/a/text()|//span[@id="source"]/a/text()').extract_first()
        item['source'] = self.web_name if not source else source
        item['author'] = sel.xpath('//div[@id="contentLiability"]/a/text()|//div[@class="g-main"]//p/span[@class="liability"]/text()').extract_first()
        item['publish_time'] = ''

        url_segments = response.url.split("/")
        if len(url_segments) > 3:
            ym = re.match(re.compile('\d{4}-\d{2}'), url_segments[-3])
            day = re.match(re.compile('\d{2}'), url_segments[-2])
            if ym and day:
                ym_arr = url_segments[-3].split("-")
                # 在允许屏道内，且含日期的url,判断为内容页
                item['publish_time'] = u"{0}年{1}月{2}日".format(ym_arr[0], ym_arr[1], url_segments[-2])

        return item
