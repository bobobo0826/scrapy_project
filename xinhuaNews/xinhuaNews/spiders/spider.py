import re

from bs4 import BeautifulSoup
from scrapy import Request, Selector
from scrapy.spiders import CrawlSpider

from xinhuaNews.items import XinhuanewsItem
from xinhuaNews.rule import SpiderBehavior, Rule


class Spider(CrawlSpider):
    name = "xinhuaSpider"
    allowed_domains = ["xinhuanet.com","news.cn"]
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60"
    headers = {
        "User-Agent":user_agent
    }
    def start_requests(self):
        start_url = ["http://www.xinhuanet.com/","http://www.xinhuanet.com/politics/","http://www.xinhuanet.com/mil/index.htm","http://www.xinhuanet.com/fortune/","http://www.xinhuanet.com/money/index.htm","http://www.xinhuanet.com/tw/index.htm","http://www.xinhuanet.com/energy/index.htm","http://www.xinhuanet.com/yuqing/index.htm"]
        # start_url=["http://www.xinhuanet.com/gangao/2018-12/05/c_1210009030.htm"]
        for url in start_url:
            yield Request(url=url, meta={'behavior': SpiderBehavior.LIST},callback=self.parse,dont_filter = True)


    def parse(self, response):
        print("---------------------------------")
        print(response.url)
        behavior = response.meta['behavior']
        sel = Selector(response=response)
        is_content_page = sel.xpath('//div[@class="main"]').extract_first()
        if behavior == SpiderBehavior.CONTENT and is_content_page:

            item = XinhuanewsItem()
            item['html'] = response.text
            item['url'] = response.url
            item['title']=''
            item['source']='新华网'
            item["publish_time"]=''
            item['content']=''
            item['author']=''
            item['type']=''

            title=sel.xpath('//div[@class="h-title"]/text()').extract_first()
            if title:
                item['title']=title.replace("\r\n","")

            text0=sel.xpath('//*[@class="h-time"]/text()').extract_first()
            if text0:
                time=text0.split(" ")[1]
                if re.match("^\d{4}-\d{2}-\d{2}$", time):
                    ymd = time.split("-")
                    item["publish_time"] = "%s年%s月%s日" % (ymd[0], ymd[1], ymd[2])


            text1=sel.xpath('//*[@id="source"]/text()').extract_first()
            if text1:
                item['source']=text1.replace(" ","")

            text2=sel.xpath('//*[@class="p-jc"]/text()').extract()
            if text2:
                for i in text2:
                    if "责任编辑" in i:
                        item['author']=i.split("：")[1].replace("\r\n","")

            soup = BeautifulSoup(response.text, "lxml")
            text3 = soup.find('div', id='p-detail')
            content=''
            if text3 is not None:
                if text3.get_text():
                    content=text3.get_text().replace("图集","").replace("+1","")
            if "【纠错】" in content:
                content=content.split("【纠错】")[0]
            item['content'] = content.replace(" ", "")


            if "politics" in response.url:
                item['type']="时政"
            if "fortune" in response.url:
                item['type']="财经"
            if "mil" in response.url:
                item['type'] = "军事"
            if "tw" in response.url:
                item['type'] = "台湾"
            if "money" in response.url:
                item['type'] = "金融"
            if "yuqing" in response.url:
                item['type'] = "舆情"
            if "energy" in response.url:
                item['type'] = "能源"
            if "local" in response.url:
                item['type'] = "地方"
            if "legal" in response.url:
                item['type'] = "法治"
            if "world" in response.url:
                item['type'] = "国际"
            if "gangao" in response.url:
                item['type'] = "港澳"
            if "tech" in response.url:
                item['type'] = "科技"

            yield item


        urls = sel.xpath('//a/@href').extract()
        for url in urls:
            if url:
                url = response.urljoin(url)
                if re.search(r'^http[s]{0,}?:/{2}\w.+$', url):
                    rule = Rule(url)
                    if rule.behavior != SpiderBehavior.DENY:
                        yield Request(url=rule.url, meta={'behavior': rule.behavior}, callback=self.parse)
