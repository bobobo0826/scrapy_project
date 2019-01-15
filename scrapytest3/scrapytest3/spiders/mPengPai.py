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
    name = 'PengPai'
    allowed_domains = ['thepaper.cn']
    user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36"
    headers = {
        "User-Agent": user_agent
    }
    start_urls = [
        'https://www.thepaper.cn/',
    ]

    rules = [
        Rule(LinkExtractor(allow=r'https://www.thepaper.cn/newsDetail_forward_\d+'), cb_kwargs={'cate': ''},
             callback='parseitem', follow=True),
    ]

    def customerParseItem(self, response, item, **kwargs):
        print('customerParseItem')
        sel = Selector(response=response)
        is_content_page = sel.xpath('//div[@class="newscontent"]').extract_first()
        item['source'] = '澎湃网'
        item["publish_time"] = ''
        item['author'] = ''
        item['cate'] = sel.xpath('//div/a[@id="select"]/text()').extract_first()
        if is_content_page:
            channels = sel.xpath('//div[@class="news_path"]/a/text()').extract()
            if channels and len(channels) >= 2:
                item['cate'] = channels[1].strip()
            news_about = sel.xpath('//div[@class="news_about"]//p/text()').extract()
            if not news_about:
                return
            if len(news_about) == 3:
                time = news_about[1].lstrip().split(" ")[0]
                item['source'] = news_about[0]
            else:
                time = news_about[0].lstrip().split(" ")[0]
            ss = sel.xpath('//*[@class="news_about"]/p/span/text()').extract_first()
            source = re.match('(?<=来源[：:]).+', ss)
            if source:
                item['source'] = source.group()
            if re.match("^\d{4}-\d{2}-\d{2}$", time):
                ymd = time.split("-")
                item["publish_time"] = "%s年%s月%s日" % (ymd[0], ymd[1], ymd[2])
            author = sel.xpath('//*[@class="news_editor"]/text()').extract_first()
            if author:
                sss = author.split("：")
                if len(sss) >= 2:
                    item["author"] = author.split("：")[1]
        else:
            item['handle'] = 2  # 非内容页处理标记为2

        return item
