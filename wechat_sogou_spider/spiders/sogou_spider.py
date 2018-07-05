#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/4 16:11
# @Author  : Esing
# @File    : sogou_spider.py
# @Software: PyCharm

# If this runs wrong, don't ask me, I don't know why;
# If this runs right, thank god, and I don't know why.
import scrapy
from scrapy.spiders.crawl import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
import re

class DmozSpider(CrawlSpider):
    name = "dmoz"
    allowed_domains = ["hr.tencent.com"]
    start_urls = [
        "http://hr.tencent.com/position.php?&start=0#a"
    ]
    rules = (
        Rule(LinkExtractor(allow='start=(.*?)#a'), callback='parse_a', follow=True, ),
    )

    def parse_a(self, response):
        # selector = Selector(response)
        # url = selector.xpath('//img[@class="pic-large"]')
        print response.url
