# encoding=utf-8
import re
import datetime

from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.spiders import CrawlSpider

from scrapytest3.items import Scrapytest3Item


class Spider(CrawlSpider):
    name = "JingJiCanKao"
    host = "http://dz.jjckb.cn"

    def start_requests(self):
        start_date = '2018-01-01'
        end_date = datetime.date.today()
        cur_date = end_date
        while str(cur_date) >= start_date:
            cur = str(cur_date).replace('-', '')
            url = "http://dz.jjckb.cn/www/pages/webpage2009/html/" + cur[0] + cur[1] + cur[2] + cur[3] + "-" + cur[
                4] + cur[5] + "/" + cur[6] + cur[7] + "/node_2.htm"
            yield Request(url=url, meta={'counter': 3}, callback=self.parse, dont_filter=True)
            cur_date = cur_date - datetime.timedelta(days=1)

    def parse(self, response):
        selector = Selector(response)
        flag = selector.xpath('//*[@class="hei14"]/a/text()').extract()
        number = response.meta['counter']

        if "下一版" in flag:
            url = response.url.split("_")[0] + "_" + str(number) + ".htm"
            number = number + 1
            yield Request(url=url, meta={'counter': number}, callback=self.parse)

        href = selector.xpath('//a[@class="hei12"]/@href').extract()
        type = selector.xpath('//table[@class="hei12"]/tbody/tr/td/strong/text()').extract_first()
        for h in href:
            if "content" in h:
                parse1_url = response.url.split("node")[0] + h
                yield Request(url=parse1_url, meta={'type': type}, callback=self.parse1)

    def parse1(self, response):
        """抓取新闻html"""
        items = Scrapytest3Item()
        items["url"] = response.url
        items["publish_time"] = ''
        items["source"] = '经济参考报'
        items["text"] = ''
        items["author"] = ''
        items["title"] = ''
        items["cate"] = response.meta["type"]
        items['website'] = self.name
        items["url"] = response.url
        selector = Selector(response)
        items["title"] = selector.xpath('//*[@class="hei16b"]/text()').extract_first()
        text0 = selector.xpath('//*[@class="black12"]/text()').extract_first()

        # 获得时间、来源网站、记者
        if text0:
            str = text0.split(" ")
            for i in str:
                if re.match("^\d{4}-\d{2}-\d{2}$", i):
                    ymd = i.split("-")
                    items["publish_time"] = "%s年%s月%s日" % (ymd[0], ymd[1], ymd[2])
                if "来源" in i:
                    items["source"] = i.split("：")[1]
            if "记者" in text0:
                items["author"] = str[5]

        # 获得新闻内容
        content = ''
        text1 = selector.xpath('//td[@class="hei14"]/table').extract_first()
        if text1:
            soup = BeautifulSoup(text1)
            text2 = soup.get_text().lstrip().split(" ")
            content = '\r\n'.join(text2)
        items["text"] = content
        yield items
