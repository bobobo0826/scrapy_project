# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JjcknewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url=scrapy.Field()
    title=scrapy.Field()
    type=scrapy.Field()
    author=scrapy.Field()
    datetime=scrapy.Field()
    source=scrapy.Field()
    content=scrapy.Field()
    html=scrapy.Field()

    pass
