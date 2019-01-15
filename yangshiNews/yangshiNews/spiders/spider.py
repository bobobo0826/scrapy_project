import re

from bs4 import BeautifulSoup
from scrapy import Request, Selector
from scrapy.spiders import CrawlSpider

from yangshiNews.items import YangshinewsItem
from yangshiNews.rule import SpiderBehavior, Rule


class Spider(CrawlSpider):
    name = "yangshiSpider"
    allowed_domains = ["cctv.com"]
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60"
    headers = {
        "User-Agent":user_agent
    }
    def start_requests(self):
        start_url = ["http://www.cctv.com/","http://news.cctv.com/china/","http://news.cctv.com/world/","http://news.cctv.com/","http://jingji.cctv.com/","http://military.cctv.com/index.shtml","http://travel.cctv.com/","http://food.cctv.com/","http://jiankang.cctv.com/","http://opinion.cctv.com/"]
        # start_url=["http://food.cctv.com/2018/12/07/ARTIWw7LtgqWKRYl5DJGGK1X181207.shtml"]
        for url in start_url:
            yield Request(url=url, meta={'behavior': SpiderBehavior.LIST},callback=self.parse,dont_filter = True)


    def parse(self, response):
        print("---------------------------------")
        print(response.url)
        behavior = response.meta['behavior']
        sel = Selector(response=response)
        is_content_page = sel.xpath('//div[@class="cnt_bd"]').extract_first()
        if behavior == SpiderBehavior.CONTENT and is_content_page:

            item = YangshinewsItem()
            item['html'] =response.text
            item['url'] = response.url
            item['title']=''
            item['source']='央视网'
            item["publish_time"]=''
            item['content']=''
            item['author']=''
            item['type']=''

            item['title']=sel.xpath('//*[@class="cnt_bd"]/h1/text()').extract_first()
            item['type']=sel.xpath('//*[@class="info"]/em/a/text()').extract_first()

            text0=sel.xpath('//*[@class="info"]/i/a/text()').extract_first()
            if text0:
                item['source']=text0.split(" ")[0]

            text1=sel.xpath('//*[@class="info"]/i/text()').extract()
            if text1:
                for i in text1:
                    if "年" in i:
                        pattern = re.compile('\d{4}年\d{2}月\d{2}日')
                        time=re.search(pattern,i)
                        item['publish_time']=time.group()

            text2=sel.xpath('//*[@class="cnt_bd"]/p/text()').extract()
            if text2:
                item['content']='\r\n'.join(text2)
            yield item


        urls = sel.xpath('//a/@href').extract()
        for url in urls:
            if url:
                url = response.urljoin(url)
                if re.search(r'^http[s]{0,}?:/{2}\w.+$', url):
                    rule = Rule(url)
                    if rule.behavior != SpiderBehavior.DENY:
                        yield Request(url=rule.url, meta={'behavior': rule.behavior}, callback=self.parse)
