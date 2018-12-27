# -*- coding: utf-8 -*-
import scrapy
import re

from yunying.items import YunyingItem
from urllib import parse
category_dict = {'105': 'ASO',
                 '106': 'SEM',
                 '107': '信息流',
                 '108': '营销推广',
                 '101': '用户运营',
                 '102': '活动运营',
                 '103': '新媒体运营',
                 '104': '数据运营',
                 '109': '行业动态',
                 '110': '职场成长',
                 '111': '资料下载',
                 '112': '课程活动'}

class Niaogebiji(scrapy.Spider):
    name = 'niaogebiji'

    allowed_domains = ['niaogebiji.com']
    start_urls = ['https://www.niaogebiji.com/pc/article/catlist/?type=article&catid=%d'%(i)
                  for i in range(101,113)]

    # start_urls = ['https://www.yunyingpai.com/user/page/'+str(i) for i in range(1,45)]

    # custom_settings = {
    #     # 数据库名称
    #     "MONGODB_DBNAME": "Yunying",
    #     # 存放数据的表名称
    #     "MONGODB_SHEETNAME": "yunyingpai"
    # }

    def parse(self, response):
        urls = response.css('div[class="article left"]>a::attr(href)').extract()
        urls = ["https://www.niaogebiji.com"+ i for i in urls]

        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        result = parse.urlparse(parse.unquote(response.url))
        query_dict = parse.parse_qs(result.query)

        items = YunyingItem()
        items["category"] = category_dict[query_dict['catid'][0]]

        for i in urls:
            yield scrapy.Request(i, callback=self.parse_item,meta={'item': items})

        timepoint = response.css("div[data-timepoint]::attr(data-timepoint)").extract()[-1]
        next_url = "https://www.niaogebiji.com/pc/index/getMoreArticle/?catid={0}&timepoint={1}&format=html".format(
            query_dict['catid'][0],timepoint
        )
        if next_url:
            yield scrapy.Request(next_url,callback=self.parse)


    def parse_item(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)

        items  = response.meta['item']
        items["title"] = response.css("h1::text").extract_first()
        items["content"] = response.css(".article").xpath("string(.)").extract_first()
        items["link"] = response.url
        items["editor"] = response.css('.author::text').extract_first()
        items["publishtime"] = response.css(".writeTime::text").extract_first()

        yield items