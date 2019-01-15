# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class ArticleItem(scrapy.Item):
    html = Field()
    url = Field()
    title = Field()
    publish_time = Field()
    source = Field()
    channel = Field()
    author = Field()
    content = Field()
