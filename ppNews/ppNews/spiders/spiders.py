# encoding=utf-8
import re
import datetime
import scrapy
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from ppNews.items import PpnewsItem
import time
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
# from zg_news.items import ZgNewsItem
shishi=["中国政库","中南海","舆论场","打虎记","人事风向","法治中国","一号专案","港台来信","长三角政商","直击现场","暖闻","澎湃质量报告","绿政公署","澎湃国际","外交学人","澎湃防务","唐人街","澎湃人物","浦江头条","教育家","全景现场","美数课","快看"]
caijing=["10%公司","能见度","地产界","财经上下游","金改实验室","牛市点线面","科技湃","澎湃商学院","自贸区连线","进博会在线"]
class Spider(CrawlSpider):
    name = "ppNewsSpider"
    allowed_domains = ["thepaper.cn"]


    def start_requests(self):
        start_url=["https://www.thepaper.cn/channel_25950","https://www.thepaper.cn/channel_25951"]
        for url in start_url:
            yield Request(url=url, meta={'behavior': "list"},callback=self.parse,dont_filter = True)

    def parse(self,response):
        behavior = response.meta['behavior']
        selector = Selector(response)
        if behavior=="content":
            type_arr = selector.xpath('//*[@class="news_path"]/a/text()').extract()
            if type_arr:
                type1=type_arr[0]
                type2 = type_arr[1]
                if type2 in shishi:
                    type1 = "时事"
                if type2 in caijing:
                    type1 = "财经"
            else:
                type1=''
                type2 = ''
            if type1:
                PpnewsItems = PpnewsItem()
                PpnewsItems["type1"] = type1
                PpnewsItems["type2"] = type2
                PpnewsItems["title"] = selector.xpath('//*[@class="news_title"]/text()').extract_first()
                news_about = selector.xpath('//*[@class="news_about"]/p/text()').extract()
                if len(news_about)==3:
                    time=news_about[1].lstrip().split(" ")[0]
                    PpnewsItems["source"] = news_about[0]
                else:
                    time=news_about[0].lstrip().split(" ")[0]
                if re.match("^\d{4}-\d{2}-\d{2}$", time):
                    ymd = time.split("-")
                    PpnewsItems["datetime"]= "%s年%s月%s日" % (ymd[0], ymd[1], ymd[2])

                ss = selector.xpath('//*[@class="news_about"]/p/span/text()').extract_first()
                if ss:
                    if "来源" in ss:
                        PpnewsItems["source"]=ss.split("：")[1]
                text1 = selector.xpath('//*[@class="news_txt"]/text()').extract()
                if text1:
                    PpnewsItems["content"] = '\r\n'.join(text1)
                text2 = selector.xpath('//*[@class="news_editor"]/text()').extract_first()
                if text2:
                    PpnewsItems["editor"] = text2.split("：")[1]
                PpnewsItems["html"] = response.text
                PpnewsItems["url"] = response.url
                yield PpnewsItems

        urls=selector.xpath('//a/@href').extract()
        for url in urls:
            if url:
                if "newsDetail_forward_" in url and "hotComm" not in url:
                    url="https://www.thepaper.cn/"+url
                    yield Request(url=url, meta={'behavior': "content"}, callback=self.parse,dont_filter = True)


    # def parse(self, response):
    #     """ 抓取新闻链接 """
    #
    #     selector = Selector(response)
    #     flag1=response.text
    #     flag2=selector.xpath('//*[@class="bn_bt index"]/a/text()').extract()
    #     # print(flag)
    #     if "文章已下线" not in flag1 and "精选" in flag2:
    #         type_arr= selector.xpath('//*[@class="news_path"]/a/text()').extract()
    #         if type_arr:
    #             type2=type_arr[1]
    #         else:
    #             type2=''
    #         if type2 in shishi:
    #             type1="时事"
    #         elif type2 in caijing:
    #             type1="财经"
    #         else:
    #             type1=''
    #         if type1:
    #             PpnewsItems=PpnewsItem()
    #             PpnewsItems["type1"]=type1
    #             PpnewsItems["type2"]=type2
    #             PpnewsItems["title"]=selector.xpath('//*[@class="news_title"]/text()').extract_first()
    #             text0=selector.xpath('//*[@class="news_about"]/p/text()').extract()
    #             if text0:
    #                 PpnewsItems["source"]=text0[0]
    #                 PpnewsItems["datetime"] =text0[1].strip().split(" ")[0]
    #             else:
    #                 PpnewsItems["source"]="澎湃新闻"
    #             text1=selector.xpath('//*[@class="news_txt"]/text()').extract()
    #             if text1:
    #                 PpnewsItems["content"] = '\r\n'.join(text1)
    #             text2 = selector.xpath('//*[@class="news_editor"]/text()').extract_first()
    #             if text2:
    #                 PpnewsItems["editor"]=text2.split("：")[1]
    #             PpnewsItems["html"]=flag1
    #             PpnewsItems["url"] = response.url
    #             yield PpnewsItems



