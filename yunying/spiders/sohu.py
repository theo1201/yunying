# -*- coding: utf-8 -*-
import scrapy
import re

from yunying.items import YunyingItem


class Sohu(scrapy.Spider):
    name = 'sohu'
    allowed_domains = ['sohu.com']
    start_urls = ['http://learning.sohu.com/zcdz/index_%d.shtml'%i for i in range(1,3)]
    start_urls.append('http://learning.sohu.com/zcdz/index.shtml')
    def parse(self, response):

        urls = response.xpath("//div[@class='lc']/div[@class='f14list']/ul/li/a/@href").extract()
        from scrapy.shell import inspect_response
        inspect_response(response, self)
        for i in urls:
            yield scrapy.Request(i, callback=self.parse_item,meta={'item': items})
        #
        # next_url = response.
        # next_url = response.url+next_url
        #
        # if next_url:
        #     yield scrapy.Request(next_url,callback=self.parse)


    def parse_item(self, response):

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        items = YunyingItem()
        items["title"] = response.css(".title >h1::text").extract_first()
        items["content"] = response.css(".content p").xpath("string(.)").extract_first()
        items["link"] = response.url
        items["category"] ="zhichangfaze"
        items["editor"] = response.css(".info::text").extract_first()


        yield items