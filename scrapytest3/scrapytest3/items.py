# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Scrapytest3Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 网站
    website = scrapy.Field()
    # 链接
    url = scrapy.Field()
    # 标题
    title = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 正文
    text = scrapy.Field()
    # 关键字
    keywords = scrapy.Field()
    # 栏目
    cate = scrapy.Field()
    # 来源
    source = scrapy.Field()
    # 上一级url
    fromUrl = scrapy.Field()
    # 深度
    deep = scrapy.Field()
    # 处理
    handle = scrapy.Field()

    # download_timeout = scrapy.Field()

    link_text = scrapy.Field()

    rule = scrapy.Field()

    html = scrapy.Field()

    publish_time = scrapy.Field()
    # content = scrapy.Field()

