# -*- coding: utf-8 -*-
import scrapy
import re

from yunying.items import YunyingItem
import time

class Maigoo(scrapy.Spider):
    name = 'maigoo'
    allowed_domains = ['maigoo.com']
    start_urls = ['https://www.maigoo.com/zq/list_2554.html']
    # start_urls = ['https://www.yunyingpai.com/user/page/'+str(i) for i in range(1,45)]

    # custom_settings = {
    #     # 数据库名称
    #     "MONGODB_DBNAME": "Yunying",
    #     # 存放数据的表名称
    #     "MONGODB_SHEETNAME": "yunyingpai"
    # }
    def __init__(self):
        self.count = 1

    def parse(self, response):
        urls = response.css('.desc>a::attr(href)').extract()
        urls = [i.replace("//","https://") for i in urls]
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        for i in urls:
            yield scrapy.Request(i, callback=self.parse_item)

        t = str(time.time()).replace('.','')[0:13]
        self.count = self.count + 1
        next_url = "https://www.maigoo.com/ajaxstream/loadblock/?str=zq%3Aarticle2_" \
                  "catid%3A2554%2Cnum%3A6%2Cpage%3A{0}&append=0&t={1}".format(self.count,t)
        if next_url:
            yield scrapy.Request(next_url,callback=self.parse)


    def parse_item(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        items = YunyingItem()
        items["title"] = response.css(".artcontent>h1::text").extract_first()
        items["content"] = response.css(".only-cont").xpath("string(.)").extract_first().strip()
        items["link"] = response.url
        items["editor"] = response.xpath("//a[@class='blue qzone']/text()").extract_first()
        # items["publishtime"] = response.css(".f2::text").re("[\d-]+")[0]

        yield items