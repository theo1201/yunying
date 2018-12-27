# -*- coding: utf-8 -*-
import scrapy


from yunying.items import YunyingItem
import re
class Xiaogushi(scrapy.Spider):
    name = 'xiaogushi'
    allowed_domains = ['xiaogushi.com']
    start_urls = ['http://www.xiaogushi.com/Article/renwu/']

    # custom_settings = {
    #     # 数据库名称
    #     "MONGODB_DBNAME": "Yunying",
    #     # 存放数据的表名称
    #     "MONGODB_SHEETNAME": "huodonghezi"
    # }

    def parse(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        urls = response.css(".x_m_l_title_1>a::attr(href)").extract()
        baseurl = "http://www.xiaogushi.com"
        urls = [baseurl+i for i in urls]
        for i in urls:
            yield scrapy.Request(i, callback=self.parse_item)

        next_url = response.css(".m_l_fenye>b+a::attr(href)").extract_first()
        next_url = baseurl+next_url
        if next_url:
            yield scrapy.Request(next_url, callback=self.parse)


    def parse_item(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        items = YunyingItem()

        items["title"] = response.css(".xgs_m_left1>h1::text").extract_first().strip()
        items["content"] = response.css(".xgs_m_neirong").xpath("string(.)").extract_first().strip()
        items["link"] = response.url
        items["editor"] = response.css('.xgs_m_xinxi>span::text').re("\s+(.*)")[0]
        items["publishtime"] = response.css('.xgs_m_xinxi>span::text').re("[\d-]+")[0]
        items["category"] = 'zhichanggushi'

        yield items


