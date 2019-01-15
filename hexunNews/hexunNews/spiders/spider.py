import re

from bs4 import BeautifulSoup
from scrapy import Request, Selector
from scrapy.spiders import CrawlSpider

from hexunNews.items import HexunnewsItem
from hexunNews.rule import SpiderBehavior, Rule


class Spider(CrawlSpider):
    name = "hexunSpider"
    allowed_domains = ["hexun.com"]
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60"
    headers = {
        "User-Agent":user_agent
    }
    def start_requests(self):
        start_url = ["http://www.hexun.com/","http://news.hexun.com/","http://roll.hexun.com/","http://stock.hexun.com/",
                     "http://funds.hexun.com/","http://p2p.hexun.com/","http://tech.hexun.com/","http://futures.hexun.com/",
                     "http://crudeoil.hexun.com/","http://insurance.hexun.com/","http://bank.hexun.com/","http://opinion.hexun.com/",
                     "http://money.hexun.com/","http://trust.hexun.com/","http://bond.hexun.com/","http://iof.hexun.com/",
                     "http://dazong.hexun.com/","http://qizhi.hexun.com/","http://gold.hexun.com/","http://forex.hexun.com/",
                     "http://nj.house.hexun.com/","http://auto.hexun.com/","http://haiwai.hexun.com/"]
        # start_url=["http://futures.hexun.com/2018-12-12/195517485.html"]
        for url in start_url:
            yield Request(url=url, meta={'behavior': SpiderBehavior.LIST},callback=self.parse,dont_filter = True)


    def parse(self, response):
        print("---------------------------------")
        print(response.url)
        behavior = response.meta['behavior']
        sel = Selector(response=response)
        is_content_page = sel.xpath('//div[@class="art_context"]').extract_first()
        if behavior == SpiderBehavior.CONTENT and is_content_page:

            item = HexunnewsItem()
            item['html'] =response.text
            item['url'] = response.url
            item['title']=''
            item['source']='和讯网'
            item["publish_time"]=''
            item['content']=''
            item['author']=''
            item['type']=''

            item['title']=sel.xpath('//div[@class="layout mg articleName"]/h1/text()').extract_first()

            text0=sel.xpath('//div[@class="links"]/a/text()').extract()
            if text0:
                item['type']=text0[1]

            text1=sel.xpath('//div[@class="tip fl"]/span/text()').extract_first()
            if text1:
                time=text1.split(" ")[0]
                if re.match('\d{4}-\d{2}-\d{2}',time):
                    cur=time.split("-")
                    item['publish_time']=cur[0]+"年"+cur[1]+"月"+cur[2]+"日"

            soup=BeautifulSoup(response.text,"lxml")
            [s.extract() for s in soup('script')]
            content=soup.find(class_='art_contextBox')
            if content is None:
                content = soup.find(class_='art_context')
            if content is not None:
                item['content']=content.get_text().replace("\u3000","\r\n")

            pattern=re.compile('责任编辑：[\u4e00-\u9fa5]*')
            text2=re.search(pattern,response.text)
            if text2:
                item['author']=text2.group().split("：")[1]

            text3=sel.xpath('//div[@class="tip fl"]/a/text()').extract_first()
            if text3 is None or text3.strip()=='':
                text3 = sel.xpath('//div[@class="tip fl"]/text()').extract_first()
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
