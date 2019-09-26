# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HousebotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    resource = scrapy.Field()
    fetchDate = scrapy.Field()
    title = scrapy.Field()
    address = scrapy.Field()
    floor = scrapy.Field()
    followInfo = scrapy.Field()
    tag = scrapy.Field()
    priceInfo = scrapy.Field()
    unitPrice = scrapy.Field()

    room = scrapy.Field()
    type = scrapy.Field()
    area = scrapy.Field()
    pass
