import re

from bs4 import BeautifulSoup
from scrapy import Request, Selector
from scrapy.spiders import CrawlSpider

from huanqiuNews.items import HuanqiunewsItem
from huanqiuNews.rule import SpiderBehavior, Rule


class Spider(CrawlSpider):
    name = "huanqiuSpider"
    allowed_domains = ["huanqiu.com"]
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60"
    headers = {
        "User-Agent":user_agent
    }
    def start_requests(self):
        # start_url = []
        start_url=["http://www.huanqiu.com/","http://world.huanqiu.com/","http://china.huanqiu.com/","http://mil.huanqiu.com/",
                   "http://taiwan.huanqiu.com/","http://opinion.huanqiu.com/","http://finance.huanqiu.com/","http://tech.huanqiu.com/",
                   "http://art.huanqiu.com/","http://go.huanqiu.com/"]
        for url in start_url:
            yield Request(url=url, meta={'behavior': SpiderBehavior.LIST},callback=self.parse,dont_filter = True)


    def parse(self, response):
        print("---------------------------------")
        print(response.url)
        behavior = response.meta['behavior']
        sel = Selector(response=response)
        is_content_page = sel.xpath('//div[@class="la_con"]').extract_first()
        if behavior == SpiderBehavior.CONTENT and is_content_page:

            item = HuanqiunewsItem()
            item['html'] =response.text
            item['url'] = response.url
            item['title']=''
            item['source']='环球网'
            item["publish_time"]=''
            item['content']=''
            item['author']=''
            item['type']=''

            item['title']=sel.xpath('//div[@class="l_a"]/h1/text()').extract_first()

            text0=sel.xpath('//div[@class="nav_left"]/a/text()').extract()
            if text0:
                item['type']=text0[1]

            text1=sel.xpath('//*[@class="la_t_a"]/text()').extract_first()
            if text1:
                time=text1.split(" ")[0]
                if re.match('\d{4}-\d{2}-\d{2}',time):
                    cur=time.split("-")
                    item['publish_time']=cur[0]+"年"+cur[1]+"月"+cur[2]+"日"

            soup=BeautifulSoup(response.text,"lxml")
            content=soup.find(class_='la_con')
            [s.extract() for s in soup('script')]
            if content is not None:
                item['content']=content.get_text().replace("\u3000","\r\n")

            text2=sel.xpath('/html/head/meta[@name="author"]/@content').extract_first()
            item['author']=text2

            text3=sel.xpath('//*[@class="la_t_b"]/a/text()').extract_first()
            if text3 and text3.strip()!="":
                item['source']=text3.strip()

            yield item


        urls = sel.xpath('//a/@href').extract()
        for url in urls:
            if url:
                url = response.urljoin(url)
                if re.search(r'^http[s]{0,}?:/{2}\w.+$', url):
                    rule = Rule(url)
                    if rule.behavior != SpiderBehavior.DENY:
                        yield Request(url=rule.url, meta={'behavior': rule.behavior}, callback=self.parse)
