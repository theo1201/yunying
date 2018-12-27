# -*- coding: utf-8 -*-
import scrapy


from yunying.items import YunyingItem


class Seoxiehui(scrapy.Spider):
    name = 'seoxiehui'
    allowed_domains = ['seoxiehui.cn']
    start_urls = ['https://www.seoxiehui.cn/zhuanlan/yunying/']

    custom_settings = {
        # 数据库名称
        "MONGODB_DBNAME": "Yunying",
        # 存放数据的表名称
        "MONGODB_SHEETNAME": "huodonghezi"
    }

    def parse(self, response):
        urls = response.css(".cl>dd>h2>a::attr(href)").extract()
        for i in urls:
            yield scrapy.Request(i, callback=self.parse_item)

        next_url = response.css(".nxt::attr(href)").extract_first()
        if next_url:
            yield scrapy.Request(next_url, callback=self.parse)


    def parse_item(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        items = YunyingItem()

        items["title"] = response.css(".ph::text").extract_first()
        items["content"] = response.css(".d").xpath("string(.)").extract_first()
        items["link"] = response.url
        items["editor"] = response.css('.xg1>a::text').extract_first()
        items["publishtime"] = response.css(".time::text").extract_first()
        items["category"] = response.css(".article-info>a::text").extract_first()

        yield items


