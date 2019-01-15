# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class RmrbnewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url=Field()
    title=Field()
    datetime=Field()
    type=Field()
    author=Field()
    source=Field()
    content=Field()
    html=Field()
    pass
