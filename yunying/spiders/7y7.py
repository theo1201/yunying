# -*- coding: utf-8 -*-
import scrapy
from yunying.items import YunyingItem

# 这个网页需要延迟访问。。有限制

class y7(scrapy.Spider):
    name = '7y7'
    allowed_domains = ['7y7.com']
    start_urls = ['http://www.7y7.com/qinggan/qingshang/']

    # custom_settings = {
    #     # 数据库名称
    #     "MONGODB_DBNAME": "Yunying",
    #     # 存放数据的表名称
    #     "MONGODB_SHEETNAME": "huodonghezi"
    # }

    def parse(self, response):
        urls = response.css(".top>a::attr(href)").extract()
        baseurl = 'http://www.7y7.com'
        urls = [baseurl+i for i in urls]
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        for i in urls:
            yield scrapy.Request(i, callback=self.parse_item)

        next_url = response.css(".current+a::attr(href)").extract_first()
        next_url = baseurl+next_url
        if next_url:
            yield scrapy.Request(next_url, callback=self.parse)


    def parse_item(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        items = response.meta['item'] if response.meta.get('item') else YunyingItem()

        if not items.get("title"):
            items["title"] = response.css(".artitle>h1::text").extract_first()
            items["link"] = response.url
            items["editor"] = response.css(".art-auther span").re("\u6765\u6e90\uff1a(.*?)<")[0]
            items["publishtime"] = response.css(".art-auther>span::text").extract_first()
            items["category"] = 'qingshang'
        items["content"] = items.setdefault("content", "") + "".join(response.css(".all_img p").xpath(
            "string(.)").extract())

        try:
            link_url = response.css(".cur+a::attr(href)").extract_first()
            if link_url != "javascript:void(0)":
                next_url = response.url.replace(response.url.split('/')[-1], link_url[2:])
                yield scrapy.Request(next_url, callback=self.parse_item, meta={'item': items})
        except:
            pass

        yield items


