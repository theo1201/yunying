# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings

import pymongo

class MongoPipeline(object):

    def __init__(self):
        host = settings["MONGODB_HOST"]
        port = settings["MONGODB_PORT"]
        db_name = settings["MONGODB_DBNAME"]
        self.client = pymongo.MongoClient(host=host, port=port)
        self.db = self.client[db_name]
        # self.post = db[settings['MONGODB_SHEETNAME']]



    def process_item(self, item, spider):
        artileinfo = dict(item)
        self.db[spider.name].insert(artileinfo)
        return item


    def close_spider(self, spider):
        self.client.close()


