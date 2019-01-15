# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field



class ZgNewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # id=Field()
    type=Field()
    title=Field()
    url=Field()
    datetime=Field()
    source=Field()
    content=Field()
    editor=Field()
    html = Field()
    pass
