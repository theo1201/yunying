# -*- coding: utf-8 -*-
import scrapy
import re

from yunying.items import YunyingItem


class T201980(scrapy.Spider):
    name = '201980'
    allowed_domains = ['201980.com']
    start_urls = ['https://www.201980.com/tag/zhichanggushi_1299_1.html']
    # start_urls = ['https://www.yunyingpai.com/user/page/'+str(i) for i in range(1,45)]


    def parse(self, response):
        urls = response.css('.geme_dl_info a::attr(href)').extract()

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        for i in urls:
            yield scrapy.Request(i, callback=self.parse_item)

        next_url = response.css('#rambo+div a::attr(href)').extract_first()
        baseurl = "https://www.201980.com"
        next_url = baseurl+next_url
        if next_url:
            yield scrapy.Request(next_url,callback=self.parse)


    def parse_item(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        items = YunyingItem()
        items["title"] = response.css(".con_box>div>h1::text").extract_first()
        items["content"] = response.css(".content").xpath("string(.)").extract_first().strip()
        items["link"] = response.url
        items["editor"] = response.css('.f2::text').re("\u6765\u6e90\uff1a(.*?)\s")[0]
        items["publishtime"] = response.css(".f2::text").re("[\d-]+")[0]

        yield items