# -*- coding: utf-8 -*-
import scrapy

from yunying.items import YunyingItem
import datetime






class IyunyingSpider(scrapy.Spider):
    name = 'iyunying'
    allowed_domains = ['iyunying.org']
    start_urls = ['http://www.iyunying.org/yunying',
                 'http://www.iyunying.org/jobs',
                 'http://www.iyunying.org/news',
                 'http://www.iyunying.org/yxzs',
                 'http://www.iyunying.org/pm',
                 'http://www.iyunying.org/social',
                 'http://www.iyunying.org/ziliao',
                 'http://www.iyunying.org/growth-hacker',
                 'http://www.iyunying.org/questions']

    # start_urls = ['http://www.iyunying.org/yunying/yhyy/page/'+str(i) for i in range(1,16)]

    # custom_settings = {
    #     # 数据库名称
    #     "MONGODB_DBNAME":"Yunying",
    #     # 存放数据的表名称
    #     "MONGODB_SHEETNAME":"iyunying"
    # }

    def parse(self, response):
        urls = response.xpath('//*[@id="wrap"]/div/div/div/ul/li/div[2]/h2/a/@href').extract()
        items = YunyingItem()
        items["category"] = response.url.split('/')[3]
        for i in urls:
            yield scrapy.Request(i,callback=self.parse_item,meta={'item': items})

        next_url = response.css('.next::attr(href)').extract_first()
        if next_url:
            yield scrapy.Request(next_url, callback=self.parse)


    def parse_item(self,response):

        items = response.meta['item']

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        items["title"] = response.xpath("//article/div/div[1]/h1/text()").extract_first()
        items["content"] = response.xpath("//article/div/div[4]").xpath("string(.)").extract_first()
        items["link"] = response.url
        items["editor"] = response.xpath('//article/div/div[1]/div/a[1]/text()').extract_first()
        publishtime = response.xpath("//article/div/div[1]/div/span[2]/text()").extract_first()
        publishtime = datetime.datetime.now().strftime('%Y-%m-%d') if publishtime.index("年")==-1 else publishtime
        items["publishtime"] = publishtime

        yield  items




