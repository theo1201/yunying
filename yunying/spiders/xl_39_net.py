# -*- coding: utf-8 -*-
import scrapy
import re

from yunying.items import YunyingItem


class T201980(scrapy.Spider):
    name = 'xl'
    allowed_domains = ['xl.39.net']
    start_urls = ['http://xl.39.net/baike/']
    # start_urls = ['https://www.yunyingpai.com/user/page/'+str(i) for i in range(1,45)]

    # custom_settings = {
    #     # 数据库名称
    #     "MONGODB_DBNAME": "Yunying",
    #     # 存放数据的表名称
    #     "MONGODB_SHEETNAME": "yunyingpai"
    # }

    def parse(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        urls = response.css(".jf_left_c").re('<a.*?href="(.*?html)">.*?<\/a>')
        for i in urls:
            yield scrapy.Request(i, callback=self.parse_item)


    def parse_item(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        items = YunyingItem()
        items["title"] = response.css(".art_box>h1::text").extract_first()
        items["content"] = response.css("#contentText").xpath("string(.)").extract_first().strip()
        items["link"] = response.url
        items["editor"] = response.css('.date>a::text').extract_first()
        items["publishtime"] = response.css(".date::text").re("[\d-]+")[0]

        yield items