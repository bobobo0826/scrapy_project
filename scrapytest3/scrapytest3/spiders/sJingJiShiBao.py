import datetime
import json
import logging
import re
from json import JSONDecodeError

from scrapy import Request, Selector, FormRequest
from scrapy.spiders import CrawlSpider

from scrapytest3.items import Scrapytest3Item
from scrapytest3.spiders.CommonSpider import CommonSpider


class JjsbSpider(CrawlSpider):
    name = 'JingJiShiBao'
    web_name = '中国经济时报'
    start_date = '2018-12-11'
    end_date = datetime.date.today()
    root_dir = 'D:/spider/jjsb'

    def start_requests(self):
        cur_date = self.end_date
        while str(cur_date) >= self.start_date:
            url = "http://jjsb.cet.com.cn/DigitaNewspaper.aspx?date=" + str(cur_date) + \
                  "&btn_sch_date=%E6%90%9C%E7%B4%A2"
            self.log("search %s news" % cur_date, level=20)
            yield Request(url=url, method="GET", meta={'behavior': SpiderBehavior.SEARCH, 'url_name': str(cur_date)},
                          callback=self.parse)
            cur_date = cur_date - datetime.timedelta(days=1)

    def parse(self, response):
        behavior = response.meta['behavior']
        url_name = response.meta['url_name'] if 'url_name' in response.meta else ''
        sel = Selector(response=response)
        if behavior == SpiderBehavior.CONTENT:

            item = self.get_item(response, url_name)
            yield item
        elif behavior == SpiderBehavior.SEARCH:
            self.log('search %s' % url_name, logging.INFO)
            szb_urls = sel.xpath('//a/@href').extract()
            for szb in szb_urls:
                if re.match('^szb_\d+_A\d{2}\.html$', szb):
                    yield Request(url="http://jjsb.cet.com.cn/" + szb, method="GET",
                                  meta={'behavior': SpiderBehavior.SECTION, 'url_name': szb}, callback=self.parse)

        elif behavior == SpiderBehavior.SECTION:
            self.log('section %s' % url_name, logging.INFO)
            name = response.url.split('/')[-1].split('.')[0]
            content_urls = sel.xpath('//area/@href').extract()
            for url in content_urls:
                if re.match('^show_\d+\.html$', url):
                    content_id = re.compile('\d+').findall(url)[0]
                    yield FormRequest(url='http://jjsb.cet.com.cn/ashx/tb_article.ashx', method="POST",
                                      formdata={"cmd": "dispid", "id": content_id},
                                      meta={'behavior': SpiderBehavior.CONTENT, 'url_name': content_id}, callback=self.parse)

    def get_item(self, response, id_):
        body = response.body
        str1 = body.decode('gb2312', errors='ignore').encode('utf8')
        try:
            data = json.loads(str1)
        except JSONDecodeError:
            data = None
        item = Scrapytest3Item()
        if data:
            if data['content'] is not None and data['content'] != "":
                content = data['content'].replace('<br&nbsp;/>', '\n').replace('&nbsp;', ' ') \
                    .replace('<br>', '\n')
                time = data['publishDate'][0:4] + '年' + data['publishDate'][5:7] + '月' + data['publishDate'][8:10] + '日'
                self.log('%s news is parsing' % time, logging.INFO)
                pattern = re.compile(r'\s*[■].*\n')
                content = re.sub(pattern, "", content)
                item['title'] = data['title'].replace('■', '')
                item['author'] = data['author'].replace('■', '')
                item['source'] = '中国经济时报'
                item['website'] = self.name
                item["url"] = response.url
                item['cate'] = data['verName'].replace('■', '')
                item['publish_time'] = time
                item['text'] = content.replace('■', '')
                self.log('%s news is saving' % time, logging.INFO)
                return item


class SpiderBehavior:
    SEARCH = 1
    SECTION = 2
    CONTENT = 3
    DENY = 4
