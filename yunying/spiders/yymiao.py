# -*- coding: utf-8 -*-
import scrapy
import re

from yunying.items import YunyingItem


class Yymiao(scrapy.Spider):
    name = 'yymiao'
    allowed_domains = ['yymiao.cn']
    start_urls = ['https://www.yymiao.cn/yunying/rumen',
                 'https://www.yymiao.cn/yingxiao/seo',
                 'https://www.yymiao.cn/wenan/cehua',
                 'https://www.yymiao.cn/anli/yyal',
                 'https://www.yymiao.cn/zl/tool']
    # start_urls = ['https://www.yunyingpai.com/user/page/'+str(i) for i in range(1,45)]

    # custom_settings = {
    #     # 数据库名称
    #     "MONGODB_DBNAME": "Yunying",
    #     # 存放数据的表名称
    #     "MONGODB_SHEETNAME": "yunyingpai"
    # }

    def parse(self, response):
        urls = response.xpath('//*[@id="wrap"]//ul/li/div[2]/h2/a/@href').extract()
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        items = YunyingItem()
        items["category"] = response.url.split('/')[3]
        for i in urls:
            yield scrapy.Request(i, callback=self.parse_item,meta={'item': items})

        next_url = response.css('.next::attr(href)').extract_first()
        if next_url:
            yield scrapy.Request(next_url,callback=self.parse)


    def parse_item(self, response):


        items  = response.meta['item']
        items["title"] = response.css(".entry-title::text").extract_first()
        items["content"] = response.css("div[class='entry-content clearfix']").xpath("string(.)").extract_first()
        items["link"] = response.url
        items["editor"] = response.css('.nickname::text').extract_first()
        items["publishtime"] = response.css(".dot+span::text").extract_first()

        yield items