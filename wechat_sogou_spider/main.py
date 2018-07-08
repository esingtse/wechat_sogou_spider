#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/4 16:11
# @Author  : Esing
# @File    : main.py
# @Software: PyCharm


import sys
reload(sys)
sys.setdefaultencoding('utf8')

from scrapy.crawler import CrawlerProcess
from wechat_sogou_spider.spiders.sogou_spider import SougouSpider
from wechat_sogou_spider.spiders.sogou_parse import SogouFeterSpider
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
process.crawl(SogouFeterSpider)
process.start()