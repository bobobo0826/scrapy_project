# encoding=utf-8
import re
import datetime

from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.spiders import CrawlSpider

from jjckNews.items import JjcknewsItem

class Spider(CrawlSpider):
    name = "jjckNewsSpider"
    host = "http://dz.jjckb.cn"


    def start_requests(self):
        start = input("Enter your startTime(20181101):")
        end = input("Enter your endTime(20181101):")
        index = int(end)
        while index >= int(start):
            cur = '%d' % index
            if int(cur[4] + cur[5]) <= 12 and 31 >= int(cur[6] + cur[7]) >= 1:
                url = "http://dz.jjckb.cn/www/pages/webpage2009/html/" + cur[0] + cur[1] + cur[2] + cur[3] + "-" + cur[4] + cur[5] +"/"+ cur[6] + cur[7] + "/node_2.htm"
                yield Request(url=url, meta={'counter':3},callback=self.parse,dont_filter=True)
            index = index - 1

    def parse(self, response):
        selector = Selector(response)
        flag=selector.xpath('//*[@class="hei14"]/a/text()').extract()
        number=response.meta['counter']

        if "下一版" in flag:
            url=response.url.split("_")[0]+"_"+str(number)+".htm"
            number=number+1
            yield Request(url=url,meta={'counter':number},callback=self.parse)

        href=selector.xpath('//a[@class="hei12"]/@href').extract()
        type = selector.xpath('//table[@class="hei12"]/tbody/tr/td/strong/text()').extract_first()
        for h in href:
            if "content" in h:
                parse1_url=response.url.split("node")[0]+h
                yield Request(url=parse1_url,meta={'type':type},callback=self.parse1)



    def parse1(self,response):
        """抓取新闻html"""
        JjcknewsItems = JjcknewsItem()
        JjcknewsItems["url"]=response.url
        JjcknewsItems["html"]=response.text
        JjcknewsItems["datetime"]=''
        JjcknewsItems["source"]='经济参考报'
        JjcknewsItems["content"]=''
        JjcknewsItems["author"]=''
        JjcknewsItems["title"]=''
        JjcknewsItems["type"] = response.meta["type"]

        selector = Selector(response)
        JjcknewsItems["title"] = selector.xpath('//*[@class="hei16b"]/text()').extract_first()
        text0 = selector.xpath('//*[@class="black12"]/text()').extract_first()

        #获得时间、来源网站、记者
        if text0:
            str=text0.split(" ")
            for i in str:
                if re.match("^\d{4}-\d{2}-\d{2}$", i):
                    ymd = i.split("-")
                    JjcknewsItems["datetime"] = "%s年%s月%s日" % (ymd[0], ymd[1], ymd[2])
                if "来源" in i:
                    JjcknewsItems["source"]=i.split("：")[1]
            if "记者" in text0:
                JjcknewsItems["author"]=str[5]

        #获得新闻内容
        content=''
        text1 = selector.xpath('//td[@class="hei14"]/table').extract_first()
        if text1:
            soup = BeautifulSoup(text1)
            text2 = soup.get_text().lstrip().split(" ")
            content='\r\n'.join(text2)
        JjcknewsItems["content"]=content
        yield JjcknewsItems







