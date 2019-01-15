# encoding=utf-8
import re
import datetime

from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.spiders import CrawlSpider

from scrapytest3.items import Scrapytest3Item


class Spider(CrawlSpider):
    name = "RenMinRiBao"
    host = "http://paper.people.com.cn"

    def start_requests(self):
        start_date = '2018-01-01'
        end_date = datetime.date.today()
        cur_date = end_date
        while str(cur_date) >= start_date:
            cur = str(cur_date).replace('-', '')
            url = "http://paper.people.com.cn/rmrb/html/" + cur[0] + cur[1] + cur[2] + cur[3] + "-" + cur[4] + cur[
                5] + "/" + cur[6] + cur[7] + "/nbs.D110000renmrb_01.htm"
            yield Request(url=url, callback=self.parse)
            cur_date = cur_date - datetime.timedelta(days=1)

    def parse(self, response):
        # print(response)
        selector = Selector(response)
        hrefs = selector.xpath('//*[@id="pageLink"]/@href').extract()
        for href in hrefs:
            url = response.url.split("nbs")[0] + href
            yield Request(url=url, callback=self.parse1)

    def parse1(self, response):
        # print(response)
        selector = Selector(response)
        hrefs = selector.xpath('//*[@id="titleList"]/ul/li/a/@href').extract()
        type = selector.xpath('//div[@class="l_t"]/text()').extract_first().replace(" ", "")
        for href in hrefs:
            url = response.url.split("nbs")[0] + href
            yield Request(url=url, meta={"type": type}, callback=self.parse2)

    def parse2(self, response):
        print(response)
        selector = Selector(response)
        item = Scrapytest3Item()
        # item["html"] = response.text
        item["cate"] = response.meta["type"]
        item["author"] = ''
        item['text'] = ''
        item["title"] = ''
        item['publish_time'] = ''
        item["source"] = ''
        item['website'] = self.name
        item["url"] = response.url
        item["title"] = selector.xpath('//div[@class="text_c"]/h1/text()').extract_first()
        text0 = selector.xpath('//div[@class="text_c"]/h4/text()').extract_first()
        if text0:
            if "记者" in text0:
                item["author"] = text0.split("记者")[1].strip()
            else:
                item["author"] = text0.strip()

        text1 = selector.xpath('//div[@class="lai"]/text()').extract_first()
        if text1:
            item["source"] = text1.replace("\r\n", "").replace(" ", "").strip()

        text2 = selector.xpath('//div[@id="riqi_"]/text()').extract_first()
        if text2:
            for i in text2.split(" "):
                if "年" in i:
                    item['publish_time'] = i
        text3 = selector.xpath('//div[@id="ozoom"]/p/text()').extract()
        if text3:
            item['text'] = "\r\n".join(text3)
        yield item
