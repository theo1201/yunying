

# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlparse
from yunying.items import YunyingItem
import re

class YunyingpaiSpider(scrapy.Spider):
    name = 'tencent1'
    allowed_domains = ['huodonghezi.com']
    categorys = ["chanpin", "yonghu", "huodong", "neirong"]
    start_urls = ['http://www.huodonghezi.com/app/%s/' % (i) for i in categorys]


    # custom_settings = {
    #     # 数据库名称
    #     "MONGODB_DBNAME": "Yunying",
    #     # 存放数据的表名称
    #     "MONGODB_SHEETNAME": "huodonghezi"
    # }

    def parse(self, response):
        urls = response.xpath('//*[@id="tab-new"]//div[2]/div[1]/a/@href').extract()
        params = re.search("/app/([a-z]+)/",response.url).group(1)
        items = YunyingItem()
        items["category"] = params
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        for i in urls:
            yield scrapy.Request(i, callback=self.parse_item,meta={'item': items})

        next_url = response.xpath('//a[@class="pagination-cur"]/../following-sibling::li[1]/a/@href').extract_first()
        if next_url:
            yield scrapy.Request(next_url,callback=self.parse)

    def parse_item(self, response):
        items = response.meta['item']
        items["title"] = response.css(".article-title::text").extract_first()
        items["content"] = response.css(".article-container").xpath("string(.)").extract_first()
        items["link"] = response.url
        items["editor"] = response.css('.article-layout>div>span>a::text').extract_first()
        items["publishtime"] = response.css(".article-title+div>span:nth-child(2)::text").extract_first()

        yield items


