# encoding=utf-8
import re
import datetime

from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.spiders import CrawlSpider

from rmrbNews.items import RmrbnewsItem


class Spider(CrawlSpider):
    name = "rmrbNewsSpider"
    host = "http://paper.people.com.cn"


    def start_requests(self):
        start = input("Enter your startTime(20181101):")
        end = input("Enter your endTime(20181101):")
        index = int(end)
        while index >= int(start):
            cur = '%d' % index
            if int(cur[4] + cur[5]) <= 12 and 31 >= int(cur[6] + cur[7]) >= 1:
                url = "http://paper.people.com.cn/rmrb/html/" + cur[0] + cur[1] + cur[2] + cur[3] + "-" + cur[4] + cur[5] +"/"+ cur[6] + cur[7] + "/nbs.D110000renmrb_01.htm"
                # print(00000000000000000)
                # print(url)
                yield Request(url=url, callback=self.parse)
            index = index - 1



    def parse(self, response):
        selector = Selector(response)
        hrefs=selector.xpath('//*[@id="pageLink"]/@href').extract()
        for href in hrefs:
            url=response.url.split("nbs")[0]+href
            yield Request(url=url,callback=self.parse1)




    def parse1(self,response):
        selector = Selector(response)
        hrefs=selector.xpath('//*[@id="titleList"]/ul/li/a/@href').extract()
        type=selector.xpath('//div[@class="l_t"]/text()').extract_first().replace(" ","")
        for href in hrefs:
            url=response.url.split("nbs")[0]+href
            yield Request(url=url,meta={"type":type},callback=self.parse2)

    def parse2(self,response):
        selector = Selector(response)
        RmrbnewsItems=RmrbnewsItem()
        RmrbnewsItems["url"]=response.url
        RmrbnewsItems["html"]=response.text
        RmrbnewsItems["type"]=response.meta["type"]
        RmrbnewsItems["author"]=''
        RmrbnewsItems["content"]=''
        RmrbnewsItems["title"]=''
        RmrbnewsItems["datetime"]=''
        RmrbnewsItems["source"]=''

        RmrbnewsItems["title"] = selector.xpath('//div[@class="text_c"]/h1/text()').extract_first()
        text0 = selector.xpath('//div[@class="text_c"]/h4/text()').extract_first()
        if text0:
            if "记者" in text0:
                RmrbnewsItems["author"] = text0.split("记者")[1].strip()
            else:
                RmrbnewsItems["author"]=text0.strip()

        text1 = selector.xpath('//div[@class="lai"]/text()').extract_first()
        if text1:
            RmrbnewsItems["source"] = text1.replace("\r\n", "").replace(" ", "").strip()

        text2 = selector.xpath('//div[@id="riqi_"]/text()').extract_first()
        if text2:
            for i in text2.split(" "):
                if "年" in i:
                    RmrbnewsItems["datetime"] = i
        text3 = selector.xpath('//div[@id="ozoom"]/p/text()').extract()
        if text3:
            RmrbnewsItems["content"] = "\r\n".join(text3)
        yield RmrbnewsItems









