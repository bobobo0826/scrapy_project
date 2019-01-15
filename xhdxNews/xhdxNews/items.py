# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class XhdxnewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url=Field()
    title=Field()
    type=Field()
    source=Field()
    datetime=Field()
    editor=Field()
    content=Field()
    html=Field()

    pass