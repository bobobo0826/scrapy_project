# encoding=utf-8
import re
import datetime

from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.spiders import CrawlSpider

from zg_news.items import ZgNewsItem

class Spider(CrawlSpider):
    name = "zg_newsSpider"
    host = "https://www.chinanews.com/"
    start_requests=[]



    def start_requests(self):
        start = input("Enter your startTime(20181101):")
        end= input("Enter your endTime(20181101):")
        index=int(end)
        while index>=int(start):
            cur='%d'%index
            if int(cur[4]+cur[5])<=12 and 31 >= int(cur[6] + cur[7]) >= 1:
                url="https://www.chinanews.com/scroll-news/"+cur[0]+cur[1]+cur[2]+cur[3]+"/"+cur[4]+cur[5]+cur[6]+cur[7]+"/news.shtml"
                yield Request(url=url, callback=self.parse,dont_filter=True)
            index = index - 1

    def parse(self, response):
        """ 抓取新闻链接 """

        selector = Selector(response)
        flag=response.text
        if "查看往日回顾" in flag:
            type_arr= selector.xpath('//*[@class="dd_lm"]/a/text()').extract()
            url_arr= selector.xpath('//*[@class="dd_bt"]/a/@href').extract()
            if type_arr and url_arr:
                for type, url in zip(type_arr, url_arr):
                    if "shipin" not in url and "tp" not in url:
                        url="https://www.chinanews.com"+url
                        yield Request(url=url, meta={'type': type}, callback=self.parse1)


    def parse1(self,response):
        """抓取新闻html"""
        ZgNewsItems = ZgNewsItem()
        ZgNewsItems["type"]=response.meta['type']
        ZgNewsItems["url"]=response.url
        ZgNewsItems["html"]=response.text
        ZgNewsItems["datetime"]=''
        ZgNewsItems["source"]='中国新闻网'
        ZgNewsItems["content"]=''
        ZgNewsItems["editor"]=''
        ZgNewsItems["title"]=''
        selector = Selector(response)
        text0 = selector.xpath('//*[@class="left-t"]/text()').extract_first()

        #获得时间和来源网站
        if text0:
            if "来源" in text0:
                ss=text0.split("来源：")
                ZgNewsItems["datetime"]=ss[0].split(" ")[1].strip()
                ZgNewsItems["source"]=ss[1]

        #获得新闻内容
        text1=selector.xpath('//*[@class="left_zw"]/p/text()').extract()
        if text1:
            str0=''
            ZgNewsItems["content"]=str0.join(text1)

        #获得新闻编辑
        text2=selector.xpath('//*[@class="left_name"]/text()').extract()
        if text2:
            str1=''
            ZgNewsItems["editor"]=str1.join(text2).strip()

        #获得新闻标题
        text3 = selector.xpath('//*[@id="cont_1_1_2"]/h1/text()').extract_first()
        if text3:
            ZgNewsItems["title"]=text3.lstrip().rstrip()
        yield ZgNewsItems










