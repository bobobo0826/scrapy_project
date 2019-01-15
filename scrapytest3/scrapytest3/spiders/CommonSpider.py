# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup, UnicodeDammit
from scrapy import Selector
from scrapy.spiders import CrawlSpider, Rule
import re
from scrapytest3.items import Scrapytest3Item
from scrapytest3.spiders.parse_content import ParseContent, RULE_TEXT


class CommonSpider(CrawlSpider):
    content_xpaths = []  # 已找到的内容 xpath， 一个网站可能有不同版本的内容页
    div_exclusions = []

    def getMeta(self, response, key, default_value):
        return response.meta[key] if response.meta.get(key) else default_value

    def customerParseItem(self, response, item, **kwargs):
        raise NotImplementedError('请实现customerParseItem方法')

    def parse_content(self, sel):
        if not self.content_xpaths:
            xpath = ParseContent.search_content_xpath(sel, self.div_exclusions)
            self.content_xpaths.append(xpath)
            div = sel.xpath(xpath)
        else:
            for xpath in self.content_xpaths:
                div = sel.xpath(xpath)
                if ParseContent.guess_content(div):
                    break
            else:
                xpath = ParseContent.search_content_xpath(sel, self.div_exclusions)
                div = sel.xpath(xpath)
                self.content_xpaths.append(xpath)
        paragraphs = div.xpath(RULE_TEXT).extract()
        paragraphs = [text.strip() for text in paragraphs if text]
        paragraphs = [text for text in paragraphs if text]
        content = '\r\n    '.join(paragraphs)
        return content

    def parseitem(self, response, **kwargs):
        print(response)
        dmt = UnicodeDammit(response.body, override_encodings=['gbk', 'utf-8'], is_html=True)
        text = response.body.decode(dmt.original_encoding, 'ignore')
        sel = Selector(text=text)
        item = Scrapytest3Item()
        deep = int(self.getMeta(response, 'depth', '0'))
        item['deep'] = deep
        # item['fromUrl'] = self.getMeta(response, 'fromUrl', '')
        item['rule'] = self.getMeta(response, 'rule', '')
        item['link_text'] = self.getMeta(response, 'link_text', '')
        # item['download_timeout'] = self.getMeta(response,'download_timeout','')
        item['website'] = self.name
        item['url'] = response.url
        title = sel.xpath('/html/head/title/text()').extract_first()
        item['title'] = title.strip() if title else item['link_text']
        # page = response.url.split("/")[-1]
        item['handle'] = 1
        item['cate'] = kwargs['cate'] if 'cate' in kwargs and kwargs['cate'] else ''
        item['text'] = self.parse_content(response)
        item['author'] = sel.xpath('/html/head/meta[@name="author"]/@content').extract_first()
        item = self.customerParseItem(response, item, **kwargs)
        # print(item)
        yield item
