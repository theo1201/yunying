# -*- coding: utf-8 -*-
import scrapy
import re

from yunying.items import YunyingItem


class Hs13(scrapy.Spider):
    name = 'hs13'
    allowed_domains = ['hs13.cn']
    start_urls = ['http://www.hs13.cn/zcfz/',
                  'http://www.hs13.cn/zhichang/',
                  'http://www.hs13.cn/zcgs/',
                  'http://www.hs13.cn/cygs/']
    # start_urls = ['https://www.yunyingpai.com/user/page/'+str(i) for i in range(1,45)]

    # custom_settings = {
    #     # 数据库名称
    #     "MONGODB_DBNAME": "Yunying",
    #     # 存放数据的表名称
    #     "MONGODB_SHEETNAME": "yunyingpai"
    # }

    def parse(self, response):
        urls = response.css('.la>h3>a::attr(href)').extract()

        items = YunyingItem()
        for i in urls:
            yield scrapy.Request(i, callback=self.parse_item,meta={'item': items})

        next_url = response.xpath('//div[@class="page"]/li[last()-1]/a/@href').extract_first()
        next_url = "http://www.hs13.cn/zcfz/"+next_url
        if next_url:
            yield scrapy.Request(next_url,callback=self.parse)


    def parse_item(self, response):

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        items  = response.meta['item']
        items["title"] = response.css(".ico-00::text").extract_first()
        items["content"] = response.css(".article").xpath("string(.)").extract_first()
        items["link"] = response.url
        items["editor"] = response.css(".info span:nth-child(1)::text").extract_first()
        items["category"] ="zhichangfaze"
        items["publishtime"] = response.css(".info span:nth-child(3)::text").extract_first()


        yield items