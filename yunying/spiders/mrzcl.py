# -*- coding: utf-8 -*-
import scrapy
import re

from yunying.items import YunyingItem
import time

class Mrzcl(scrapy.Spider):
    name = 'mrzcl'
    allowed_domains = ['mrzcl.com']
    start_urls = ['http://www.mrzcl.com/workplace','http://www.mrzcl.com/marketing']
    # start_urls = ['https://www.yunyingpai.com/user/page/'+str(i) for i in range(1,45)]

    def parse(self, response):
        urls = response.css('h2>a::attr(href)').extract()
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        for i in urls:
            yield scrapy.Request(i, callback=self.parse_item)
        next_url =response.css("li.active+li>a::attr(href)").extract_first()

        if next_url:
            yield scrapy.Request(next_url,callback=self.parse)


    def parse_item(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        items = YunyingItem()
        items["title"] = response.css(".article-title>a::text").extract_first()
        items["content"] = response.css(".article-content").xpath("string(.)").extract_first().strip()
        items["link"] = response.url
        items["category"] = response.css("#mute-category>a::text").extract_first().strip()
        items["publishtime"] = response.css("time.muted::text").extract_first().strip()
        items["editor"] = response.css(".muted:not(#mute-category)>a::text").extract_first()
        yield items