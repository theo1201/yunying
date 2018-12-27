# -*- coding: utf-8 -*-
import scrapy
import re

from yunying.items import YunyingItem


class Meimeidu(scrapy.Spider):
    name = 'meimeidu'
    allowed_domains = ['meimeidu.com']
    # 'https://www.meimeidu.com/Home/Article/0',
    start_urls = ['https://www.meimeidu.com/Theme/List/46/0/0']

    def parse(self, response):
        baseurl = "https://www.meimeidu.com"
        urls = response.xpath('//*[@id="contenta"]/div[2]/table//td[1]/a/@href').extract()
        urls = [baseurl + i for i in urls]

        items = YunyingItem()
        if response.url.index("Theme/List")==-1:
            for i in urls:
                yield scrapy.Request(i, callback=self.parse_item,meta={'item': items})
        else:
            for i in urls:
                yield scrapy.Request(i, callback=self.parse_item2,meta={'item': items})

        next_url = response.css('.current+a::attr(href)').extract_first()
        next_url = baseurl+next_url

        if next_url:
            yield scrapy.Request(next_url,callback=self.parse)


    def parse_item(self, response):

        from scrapy.shell import inspect_response
        inspect_response(response, self)

        items  = response.meta['item']
        items["title"] = response.css(".dabiaoti::text").extract_first().strip()
        items["content"] = response.css(".neirong").xpath("string(.)").extract_first().strip()
        items["link"] = response.url
        items["editor"] = response.css(".xiaoxijulianjie::text").extract_first()
        items["category"] =response.css(".laiyuan>table>tr>td:nth-child(2)::text").re("\u7c7b\u522b\uff1a(.*?)\r\n")[0]
        items["publishtime"] = response.css(".laiyuan>table>tr>td:nth-child(2)::text").re("\u65e5\u671f\uff1a(.*?)\xa0")[0]

        yield items

    def parse_item2(self, response):

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        items  = response.meta['item']
        items["title"] = response.xpath("//div[@class='body']/table//tr/td[2]/h1/text()").extract_first().strip()
        items["content"] = response.xpath("//div[@class='content']/pre").xpath("string(.)").extract_first().strip()
        items["link"] = response.url
        items["editor"] =response.xpath("//span[@class='xiaoculan']/a/text()").extract_first().strip()
        items["category"] ="zhichangrensheng"
        items["publishtime"] = response.xpath("//div[@class='content']/p[2]/span/text()").extract_first().strip()

        yield items