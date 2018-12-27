# -*- coding: utf-8 -*-
import scrapy


from yunying.items import YunyingItem


# 这个网页需要延迟访问。。有限制

class Xphabit(scrapy.Spider):
    name = 'xphabit'
    allowed_domains = ['xphabit.com']
    start_urls = ['http://www.xphabit.com/']

    # custom_settings = {
    #     # 数据库名称
    #     "MONGODB_DBNAME": "Yunying",
    #     # 存放数据的表名称
    #     "MONGODB_SHEETNAME": "huodonghezi"
    # }

    def parse(self, response):
        urls = response.css(".title>a::attr(href)").extract()
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        for i in urls:
            yield scrapy.Request(i, callback=self.parse_item)

        next_url = response.css(".on+td>a::attr(href)").extract_first()
        if next_url:
            yield scrapy.Request(next_url, callback=self.parse)


    def parse_item(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        items = YunyingItem()

        items["title"] = response.css("#vtitle::text").extract_first()
        items["content"] = response.css("#v1pane").xpath("string(.)").extract_first()
        items["link"] = response.url
        items["editor"] = ''
        items["publishtime"] = response.css(".icon-time::text").extract_first()
        items["category"] = 'qingshang'

        yield items


