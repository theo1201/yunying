# -*- coding: utf-8 -*-
import scrapy


from yunying.items import YunyingItem


class YunyingpaiSpider(scrapy.Spider):
    name = 'yunyingxuetang'
    allowed_domains = ['yunyingxuetang.com']
    start_urls = ['http://www.yunyingxuetang.com/xinmeiti',
                     'http://www.yunyingxuetang.com/growth',
                     'http://www.yunyingxuetang.com/app',
                     'http://www.yunyingxuetang.com/chanpin',
                     'http://www.yunyingxuetang.com/neirong',
                     'http://www.yunyingxuetang.com/huodong',
                     'http://www.yunyingxuetang.com/yonghu']
    # start_urls = ['http://www.yunyingxuetang.com/yonghu/page/%d'%(i) for i in range(1,6)][0:1]

    # custom_settings = {
    #     # 数据库名称
    #     "MONGODB_DBNAME": "Yunying",
    #     # 存放数据的表名称
    #     "MONGODB_SHEETNAME": "yunyingxuetang"
    # }

    def parse(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        urls = response.css(".content article>header>h2>a::attr(href)").extract()
        items = YunyingItem()
        items["category"] = response.url.split('/')[3]

        for i in urls:
            yield scrapy.Request(i, callback=self.parse_item,meta={'item': items})

        next_url = response.css('.next-page a::attr(href)').extract_first()
        from scrapy.shell import inspect_response
        inspect_response(response, self)
        if next_url:
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_item(self, response):

        items = response.meta["item"]

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        items["title"] = response.css(".article-title>a::text").extract_first()
        items["content"] = response.css(".article-content").xpath("string(.)").extract_first()
        items["link"] = response.url
        eandp = response.css('.article-meta>li::text').extract_first()
        items["editor"] = eandp.split(" ")[0]
        items["publishtime"] = eandp.split(" ")[-1]


        yield items


