import re

from scrapy import Request, Selector
from scrapy.spiders import CrawlSpider

from ppxw_spider.items import ArticleItem
from ppxw_spider.rule import SpiderBehavior, Rule


class PpxwSpider(CrawlSpider):
    name = "ppxw_spider"
    allowed_domains = ["thepaper.cn"]
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60"
    headers = {
        "User-Agent":user_agent
    }
    def start_requests(self):
        start_url = ["https://www.thepaper.cn/channel_25950", "https://www.thepaper.cn/channel_25951"]
        for url in start_url:
            yield Request(url=url, meta={'behavior': SpiderBehavior.LIST},callback=self.parse,dont_filter = True)
        # for url in self.start_urls:
        #     print(url)
        #     yield Request(url=url, meta={'behavior': SpiderBehavior.LIST}, callback=self.parse)

    def parse(self, response):
        behavior = response.meta['behavior']
        sel = Selector(response=response)
        is_content_page = sel.xpath('//div[@class="newscontent"]').extract_first()
        if behavior == SpiderBehavior.CONTENT and is_content_page:
            item = ArticleItem()
            item['html'] = response.text
            item['url'] = response.url
            item['channel']=''
            item['title']=''
            item['source']=''
            item["publish_time"]=''
            item['content']=''
            item['author']=''

            channels = sel.xpath('//div[@class="news_path"]/a/text()').extract()
            if channels and len(channels) >= 2:
                item['channel'] = channels[1].strip()

            title=sel.xpath('//h1[@class="news_title"]/text()').extract_first()
            if title:
                item['title'] =title

            news_about = sel.xpath('//div[@class="news_about"]//p/text()').extract()
            if len(news_about) == 3:
                time = news_about[1].lstrip().split(" ")[0]
                item['source'] = news_about[0]
            else:
                time = news_about[0].lstrip().split(" ")[0]
            ss = sel.xpath('//*[@class="news_about"]/p/span/text()').extract_first()
            if ss:
                if "来源" in ss:
                    item['source']=ss.split("：")[1]
            if re.match("^\d{4}-\d{2}-\d{2}$", time):
                ymd = time.split("-")
                item["publish_time"] = "%s年%s月%s日" % (ymd[0], ymd[1], ymd[2])
            author = sel.xpath('//*[@class="news_editor"]/text()').extract_first()
            if author:
                item["author"] = author.split("：")[1]

            paras = sel.xpath('//div[@class="news_txt"]/text()').extract()
            if paras:
                item['content'] = "\r\n".join(paras)
            yield item
        urls = sel.xpath('//a/@href').extract()
        for url in urls:
            if url:
                url = response.urljoin(url)
                if re.search(r'^http[s]{0,}?:/{2}\w.+$', url):
                    rule = Rule(url)
                    if rule.behavior != SpiderBehavior.DENY:
                        yield Request(url=rule.url, meta={'behavior': rule.behavior}, callback=self.parse)
