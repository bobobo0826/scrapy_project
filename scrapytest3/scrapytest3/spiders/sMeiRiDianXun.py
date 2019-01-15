# encoding=utf-8
import re
import datetime

from bs4 import BeautifulSoup
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.spiders import CrawlSpider

from scrapytest3.items import Scrapytest3Item


class Spider(CrawlSpider):
    name = "MeiRiDianXun"
    allowed_domains = ["mrdx.cn"]

    def start_requests(self):
        start_date = '2018-01-01'
        end_date = datetime.date.today()
        cur_date = end_date
        while str(cur_date) >= start_date:
            cur = str(cur_date).replace('-', '')
            url = "http://mrdx.cn/content/" + cur + "/Page01HO.htm"
            yield Request(url=url, meta={'counter': 3}, callback=self.parse, dont_filter=True)
            cur_date = cur_date - datetime.timedelta(days=1)

    def parse(self, response):
        selector = Selector(response)
        hrefs = selector.xpath('//a[@class="atitle"]/@href').extract()
        rr = re.compile(r'责任编辑：[\u4e00-\u9fa5]+\s*[\u4e00-\u9fa5]*')
        editors = rr.findall(response.text)
        i = 0
        editor = ''
        for href in hrefs:
            if "Page" in href:
                url = response.url.split("Page")[0] + href
                if i < len(editors):
                    editor = editors[i]
                i = i + 1
                yield Request(url=url, meta={'editor': editor}, callback=self.parse1, dont_filter=True)

    def parse1(self, response):
        selector = Selector(response)
        hrefs = selector.xpath('//a[@class="atitle"]/@href').extract()
        tt = selector.xpath('//*[@id="table5"]/tbody/tr/td[1]/strong/text()').extract_first()
        e = response.meta['editor']
        for href in hrefs:
            if "Artice" in href:
                url = response.url.split("Page")[0] + href
                yield Request(url=url, meta={'type': tt, 'editor': e}, callback=self.parse2)

    def parse2(self, response):
        selector = Selector(response)
        items = Scrapytest3Item()
        items['website'] = self.name
        items["url"] = response.url
        items["cate"] = response.meta['type']
        items["author"] = response.meta['editor']
        items["text"] = ''
        items["title"] = ''
        items["publish_time"] = ''
        items["source"] = '新华每日电讯'
        items["title"] = selector.xpath(
            '//*[@id="contenttext"]/font/table/tbody/tr[2]/td/div/strong/font/text()').extract_first()
        text0 = selector.xpath('//*[@id="contenttext"]/font/table/tbody/tr[5]/td/text()|'
                               '//*[@id="contenttext"]/font/table/tbody/tr[5]/td/div[1]/text()|'
                               '//*[@id="contenttext"]/font/div/text()|'
                               '/html/body/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/span[2]/table[1]/tbody/tr[6]/td/text()|'
                               '//*[@id="contenttext"]/font/div[1]/table/tbody/tr[5]/td/text()').extract()
        if text0:
            for item in text0:
                if "稿件来源" in item:
                    items["source"] = item.split("稿件来源：")[1].strip()
                    time = item.split("稿件来源：")[0].split("（")[1].split("）")[0].strip()
                    if re.match("^\d{4}-\d{2}-\d{2}$", time):
                        ymd = time.split("-")
                        items["publish_time"] = "%s年%s月%s日" % (ymd[0], ymd[1], ymd[2])
                else:
                    break

        content = ''
        text1 = selector.xpath('//*[@id="contenttext"]/font/div[2]/text()').extract_first()
        if text1:
            content = content + text1 + '\n'
        text2 = selector.xpath('//*[@id="contenttext"]/font/div[2]/p/text()').extract()
        if text2:
            content = content + "\r\n".join(text2)
        else:
            text3 = selector.xpath('//*[@id="contenttext"]/font/div[2]/div/text()').extract()
            if text3:
                content = content + "\r\n".join(text3)
        items["text"] = "      " + content.lstrip()
        yield items
