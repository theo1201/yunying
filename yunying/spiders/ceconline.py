# -*- coding: utf-8 -*-
import scrapy


from yunying.items import YunyingItem
import re
class Ceconline(scrapy.Spider):
    name = 'ceconline'
    allowed_domains = ['ceconline.com']
    start_urls = ['http://www.ceconline.com/FSSearch.do?keyword=%C7%E9%C9%CC%B8%DF%B5%C4%C8%CB&pageno=01&sortBy=5',
                  'http://www.ceconline.com/FSSearch.do?keyword=%D6%B0%B3%A1%B9%CA%CA%C2&pageno=01&sortBy=5']

    custom_settings = {
        # 数据库名称
        "MONGODB_DBNAME": "Yunying",
        # 存放数据的表名称
        "MONGODB_SHEETNAME": "huodonghezi"
    }
    def __init__(self):
        self.count = 1

    def parse(self, response):
        urls = response.css(".h3_title::attr(href)").extract()
        baseurl = "http://www.ceconline.com"
        urls = [baseurl+i for i in urls]
        for i in urls:
            yield scrapy.Request(i, callback=self.parse_item)


        # next_url = response.css(".nxt::attr(href)").extract_first()
        self.count = self.count + 1
        sub_str = 'pageno=%s'%(str(self.count).zfill(2))
        next_url= re.sub("pageno=\d+",sub_str,response.url)
        if next_url:
            yield scrapy.Request(next_url, callback=self.parse)


    def parse_item(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        items = YunyingItem()

        items["title"] = response.css(".article_title::text").extract_first().strip()
        items["content"] = response.css(".article_text").xpath("string(.)").extract_first().strip()
        items["link"] = response.url
        # items["editor"] = ''
        items["publishtime"] = response.css('.article_info::text').re("[\d-]+")[0]
        # items["category"] = ''

        yield items


