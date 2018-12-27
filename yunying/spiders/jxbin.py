# -*- coding: utf-8 -*-
import scrapy
import re

from yunying.items import YunyingItem


class Jxbin(scrapy.Spider):
    name = 'jxbin'
    allowed_domains = ['jxbin.com']
    start_urls = ['http://www.jxbin.com/news',
                 'http://www.jxbin.com/seo',
                 'http://www.jxbin.com/chanpin',
                 'http://www.jxbin.com/yonghu',
                 'http://www.jxbin.com/neirong',
                 'http://www.jxbin.com/huodong',
                 'http://www.jxbin.com/xinmeiti',
                 'http://www.jxbin.com/app',
                 'http://www.jxbin.com/dianshang']

    # start_urls = ['https://www.yunyingpai.com/user/page/'+str(i) for i in range(1,45)]

    # custom_settings = {
    #     # 数据库名称
    #     "MONGODB_DBNAME": "Yunying",
    #     # 存放数据的表名称
    #     "MONGODB_SHEETNAME": "yunyingpai"
    # }

    def parse(self, response):
        urls = response.xpath("//section/article/article/h2/a/@href").extract()

        items = YunyingItem()
        items["category"] = response.url.split('/')[3]
        for i in urls:
            yield scrapy.Request(i, callback=self.parse_item,meta={'item': items})

        next_url = response.css('a[class="next page-numbers"]::attr(href)').extract_first()
        if next_url:
            yield scrapy.Request(next_url,callback=self.parse)


    def parse_item(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        items  = response.meta['item']
        items["title"] = response.css(".post-head h1::text").extract_first()
        items["content"] = response.css(".content-post").xpath("string(.)").extract_first()
        items["link"] = response.url
        items["editor"] = response.css('.category a::text').extract_first()
        items["publishtime"] = response.css(".date::text").extract_first()

        yield items