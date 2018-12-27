# -*- coding: utf-8 -*-

# Scrapy settings for yunying project

BOT_NAME = 'yunying'

SPIDER_MODULES = ['yunying.spiders']
NEWSPIDER_MODULE = 'yunying.spiders'

USER_AGENT = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"

USER_AGENTS = [
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.2)',
    'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
    'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
    'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
    'Mozilla/5.0 (Linux; U; Android 4.0.3; zh-cn; M032 Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.27 Safari/525.13'
]

COOKIES_ENABLED = False

# MONGODB 主机名
MONGODB_HOST = "127.0.0.1"
# MONGODB 端口号
MONGODB_PORT = 27017
# # 数据库名称
MONGODB_DBNAME="Yunying"
# 存放数据的表名称
MONGODB_SHEETNAME="woshipm"


# ----------- selenium参数配置 -------------
SELENIUM_TIMEOUT = 25           # selenium浏览器的超时时间，单位秒
LOAD_IMAGE = True               # 是否下载图片
WINDOW_HEIGHT = 900             # 浏览器窗口大小
WINDOW_WIDTH = 900
# ----------- 中间件配置 -------------
DOWNLOADER_MIDDLEWARES ={
    # 'yunying.middlewares.SeleniumMiddleware': 543,
}

ITEM_PIPELINES = {
    'yunying.pipelines.MongoPipeline':400
}