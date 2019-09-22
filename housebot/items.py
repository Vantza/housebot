# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HousebotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    address = scrapy.Field()
    floor = scrapy.Field()
    followInfo = scrapy.Field()
    tag = scrapy.Field()
    totalPrice = scrapy.Field()
    unitPrice = scrapy.Field()
    pass
