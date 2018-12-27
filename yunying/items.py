# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YunyingItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    content = scrapy.Field()
    link = scrapy.Field()
    editor = scrapy.Field()
    publishtime = scrapy.Field()
    category =scrapy.Field()
