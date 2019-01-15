import re

from bs4 import BeautifulSoup
from scrapy import Request, Selector
from scrapy.spiders import CrawlSpider

from ckxx_spider.items import  NewsInfoItem
from ckxx_spider.rules import Rule, SpiderBehavior
from ckxx_spider.settings import PARA_SEP


class CkxxSpider(CrawlSpider):
    name = "ckxx_spider"
    allowed_domains = ["cankaoxiaoxi.com"]
    start_urls = "http://www.cankaoxiaoxi.com/"


    def start_requests(self):
        yield Request(url=self.start_urls,meta={'behavior': SpiderBehavior.LIST}, callback=self.parse)

    def parse(self, response):
        behavior = response.meta['behavior']
        sel = Selector(response=response)
        if behavior == SpiderBehavior.CONTENT:
            item = NewsInfoItem()
            item['html'] = response.text
            item['url'] = response.url
            item['publish_time'] = response.meta['publish_time']
            item['channel'] = response.meta['channel']
            item['title'] = sel.xpath('//div[@class = "bg-content"]/h1/text()').extract_first()
            item['source'] = sel.xpath('//div[@class = "bg-content"]/span[@id="source_baidu"]/a/text()').extract_first()
            item['author'] = sel.xpath('//div[@class = "bg-content"]/span[@id="author_baidu"]/text()').extract_first()
            item['editor'] = sel.xpath('//div[@class = "bg-content"]/span[@id="editor_baidu"]/text()').extract_first()
            paragraphs = sel.xpath('//div[@id="ctrlfscont"]/p/text()').extract()

            if paragraphs:
                item['content'] = PARA_SEP.join(paragraphs)
            yield item
        urls = sel.xpath('//a/@href').extract()
        for url in urls:
            if url:
                url = response.urljoin(url)
                if re.search(r'^http[s]{0,}?:/{2}\w.+$', url):
                    rule = Rule(url)
                    if rule.behavior != SpiderBehavior.DENY:
                        yield Request(url=rule.url,meta={'behavior': rule.behavior, 'channel': rule.channel,
                                                         'publish_time': rule.publish_time}, callback=self.parse)






















