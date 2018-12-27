# -*- coding: utf-8 -*-
import scrapy
import re

from yunying.items import YunyingItem
import time

class Mrzcl(scrapy.Spider):
    name = 'woshipm'
    allowed_domains = ['woshipm.com']
    start_urls = ['http://www.woshipm.com/tag/%E5%BF%83%E7%90%86%E5%AD%A6']


    def parse(self, response):
        urls = response.css('.post-title>a::attr(href)').extract()


        for i in urls:
            yield scrapy.Request(i, callback=self.parse_item)
        next_url =response.css(".nav-links>span+a::attr(href)").extract_first()

        if next_url:
            yield scrapy.Request(next_url,callback=self.parse)


    def parse_item(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        items = YunyingItem()
        items["title"] = response.css(".article-title::text").extract_first()
        items["content"] = response.css(".grap").xpath("string(.)").extract_first().strip()
        items["link"] = response.url
        items["category"] = "xinlixue"
        items["publishtime"] = response.css(".post-meta-item::text").extract_first().strip()
        items["editor"] = response.css("div[class*='u-flex1']>div>a::text").extract_first()
        yield items