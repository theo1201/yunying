# -*- coding: utf-8 -*-
import scrapy
import re

from yunying.items import YunyingItem


class YunyingpaiSpider(scrapy.Spider):
    name = 'yunyingpai'
    allowed_domains = ['yunyingpai.com']
    start_urls = ['https://www.yunyingpai.com/news',
                 'https://www.yunyingpai.com/user',
                 'https://www.yunyingpai.com/content',
                 'https://www.yunyingpai.com/activity',
                 'https://www.yunyingpai.com/market',
                 'https://www.yunyingpai.com/media',
                 'https://www.yunyingpai.com/data',
                 'https://www.yunyingpai.com/app',
                 'https://www.yunyingpai.com/brand',
                 'https://www.yunyingpai.com/channel',
                 'https://www.yunyingpai.com/paperwork',
                 'https://www.yunyingpai.com/work']

    # start_urls = ['https://www.yunyingpai.com/user/page/'+str(i) for i in range(1,45)]

    # custom_settings = {
    #     # 数据库名称
    #     "MONGODB_DBNAME": "Yunying",
    #     # 存放数据的表名称
    #     "MONGODB_SHEETNAME": "yunyingpai"
    # }

    def parse(self, response):
        urls = response.xpath("//div/section//h3/a/@href").extract()
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        items = YunyingItem()
        items["category"] = response.url.split('/')[3]
        for i in urls:
            yield scrapy.Request(i, callback=self.parse_item,meta={'item': items})


        next_url = response.css('a[class="next page-numbers"]::attr(href)').extract_first()
        if next_url:
            yield scrapy.Request(next_url,callback=self.parse)


    def parse_item(self, response):

        items  = response.meta['item']
        items["title"] = response.xpath("//div/article/header/h2/text()").extract_first()
        items["content"] = response.xpath("//div/article/div[4]").xpath("string(.)").extract_first()
        items["link"] = response.url
        items["editor"] = response.xpath('//div/article/header/div/a/text()').extract_first()
        items["publishtime"] = response.xpath("//div/article/header/div/time/text()").extract_first()

        yield items