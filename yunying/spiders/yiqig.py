# -*- coding: utf-8 -*-
import scrapy
import re

from yunying.items import YunyingItem


class Yiqig(scrapy.Spider):
    name = 'yiqig'
    allowed_domains = ['yiqig.com']
    start_urls = ['http://www.yiqig.com/zhichanglizhi/zhichangzhinan/',
                  'http://www.yiqig.com/zhichanglizhi/qiuzhizhinan/']
    # start_urls = ['https://www.yunyingpai.com/user/page/'+str(i) for i in range(1,45)]

    # custom_settings = {
    #     # 数据库名称
    #     "MONGODB_DBNAME": "Yunying",
    #     # 存放数据的表名称
    #     "MONGODB_SHEETNAME": "yunyingpai"
    # }

    def parse(self, response):
        urls = response.css('h3>a::attr(href)').extract()
        urls = ["http://www.yiqig.com"+i for i in urls]
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)


        items = YunyingItem()
        for i in urls:
            yield scrapy.Request(i, callback=self.parse_item,meta={'item': items})

        next_url = response.xpath('//div[@class="dede_pages"]//li[last()-3]/a/@href').extract_first()
        next_url = response.url+next_url

        if next_url:
            yield scrapy.Request(next_url,callback=self.parse)


    def parse_item(self, response):

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        items  = response.meta['item']
        items["title"] = response.css(".title >h1::text").extract_first()
        items["content"] = response.css(".content p").xpath("string(.)").extract_first()
        items["link"] = response.url
        items["category"] ="zhichangfaze"
        items["editor"] = response.css(".info::text").extract_first()


        yield items