# -*- coding: utf-8 -*-
import scrapy


from yunying.items import YunyingItem
import re
class Xigushi(scrapy.Spider):
    name = 'xigushi'
    allowed_domains = ['xigushi.com']
    start_urls = ['http://www.xigushi.com/jcgs/list_5_1.html']

    # custom_settings = {
    #     # 数据库名称
    #     "MONGODB_DBNAME": "Yunying",
    #     # 存放数据的表名称
    #     "MONGODB_SHEETNAME": "huodonghezi"
    # }

    def parse(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        urls = response.xpath("//div[@class='list']/dl/dd/ul/li/a/@href").extract()
        baseurl = "http://www.xigushi.com"
        urls = [baseurl+i for i in urls]
        for i in urls:
            yield scrapy.Request(i, callback=self.parse_item)

        next_url = response.css(".thisclass+li>a::attr(href)").extract_first()
        next_url = response.url.replace(response.url.split('/')[-1],next_url)
        if next_url:
            yield scrapy.Request(next_url, callback=self.parse)


    def parse_item(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        items = YunyingItem()

        items["title"] = response.css("//div[@class='by']/dl/dd/h1/text()").extract_first().strip()
        items["content"] = response.css(".info+p").xpath("string(.)").extract_first().strip()
        items["link"] = response.url
        items["editor"] = response.css('.info::text').re("\u4f5c\u8005:(.*?)\s")[0]
        items["publishtime"] = response.css('.info::text').re("[\d-]+")[0]
        items["category"] = 'zhichanggushi'

        yield items


