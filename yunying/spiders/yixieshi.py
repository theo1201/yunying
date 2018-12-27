# -*- coding: utf-8 -*-
import scrapy
import re

from yunying.items import YunyingItem


class Yixieshi(scrapy.Spider):
    name = 'yixieshi'
    allowed_domains = ['yixieshi.com']
    start_urls = ['http://www.yixieshi.com/yyzs/pd',
                  'http://www.yixieshi.com/zcgl',]
    # start_urls = ['https://www.yunyingpai.com/user/page/'+str(i) for i in range(1,45)]

    # custom_settings = {
    #     # 数据库名称
    #     "MONGODB_DBNAME": "Yunying",
    #     # 存放数据的表名称
    #     "MONGODB_SHEETNAME": "yunyingpai"
    # }

    def parse(self, response):
        urls = response.css('.col-md-8>h2>a::attr(href)').extract()


        items = YunyingItem()
        # items["category"] = 'chanpin'
        for i in urls:
            yield scrapy.Request(i, callback=self.parse_item,meta={'item': items})

        next_url = response.css('.next-page>a::attr(href)').extract_first()
        if next_url:
            yield scrapy.Request(next_url,callback=self.parse)


    def parse_item(self, response):

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        items  = response.meta['item']
        items["title"] = response.css(".post-title::text").extract_first()
        items["content"] = response.css(".article-content").xpath("string(.)").extract_first()
        items["link"] = response.url
        items["category"] =response.css(".article-meta span:nth-child(2)>a::text").extract_first()
        items["publishtime"] = response.css(".article-meta>span::text").extract_first()

        yield items