#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/4 16:11
# @Author  : Esing
# @File    : main.py
# @Software: PyCharm

# If this runs wrong, don't ask me, I don't know why;
# If this runs right, thank god, and I don't know why.
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from scrapy.crawler import CrawlerProcess
from wechat_sogou_spider.spiders.sogou_spider import DmozSpider
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())
process.crawl(DmozSpider)
process.start()