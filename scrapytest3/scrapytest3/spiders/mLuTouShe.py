# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
from scrapytest3.spiders.CommonSpider import CommonSpider
from bs4 import BeautifulSoup, UnicodeDammit
from scrapy import Selector

# 要翻墙
class LuTouSheSpider(CommonSpider):
    name = 'LuTouShe'
    web_name = '路透社'
    allowed_domains = ['cn.reutersmedia.net']
    start_urls = [
        "https://cn.reutersmedia.net/",
    ]
    div_exclusions = []
    content_xpaths = []  # 初始化已找到的xpath

    rules = [
        Rule(LinkExtractor(allow=r'https://cn.reutersmedia.net/article/[\w-]*id\w*'), callback='parseitem',
             follow=True)
    ]

    def customerParseItem(self, response, item, **kwargs):
        dmt = UnicodeDammit(response.body, override_encodings=['gbk', 'utf-8'], is_html=True)
        text = response.body.decode(dmt.original_encoding, 'ignore')
        sel = Selector(text=text)
        item['cate'] = response.xpath('//div[@class="ArticleHeader_content-container"]/div['
                                      '@class="ArticleHeader_channel"]/a/text()').extract_first().strip()
        item['author'] = sel.xpath('/html/body/meta[@name="Author"]/@content').extract_first().strip()
        pub_time = sel.xpath('//div[@class="ArticleHeader_date"]/text()').extract_first().split('/')[0].strip()
        item['publish_time'] = transdate(pub_time).strip()
        url_segments = response.url.split("/")
        if len(url_segments) > 3:
            ym = re.match(re.compile('\d{4}-\d{2}'), url_segments[-3])
            day = re.match(re.compile('\d{2}'), url_segments[-2])
            if ym and day:
                ym_arr = url_segments[-3].split("-")
                # 在允许屏道内，且含日期的url,判断为内容页
                item['publish_time'] = u"{0}年{1}月{2}日".format(ym_arr[0], ym_arr[1], url_segments[-2])
        return item


def transdate(pub_time):
    # print(pub_time)
    months_set = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
                  'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11',
                  'December': '12'}
    month = pub_time.split(',')[0].split(' ')[0].strip().strip()
    day = pub_time.split(',')[0].split(' ')[1].strip().strip()
    if len(day) == 1:
        day = '0' + day
    year = pub_time.split(',')[1].strip()
    month = months_set[month].strip()
    return year + '年' + month + '月' + day + '日'
