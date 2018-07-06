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
import re,requests
from urllib import  quote
from scrapy.http.cookies import CookieJar

class DmozSpider(CrawlSpider):
    name = "dmoz"
    # keyword = '中山大学'
    # start_urls = ['http://weixin.sogou.com/weixin?type=2&s_from=input&query=%s&ie=utf8&_sug_=n&_sug_type_=' % (
    #     quote(keyword))]
    #
    #
    # rules = (
    #     Rule(LinkExtractor(allow="^http://weixin.sogou.com/\S*page=\d+&ie=utf8$"), callback='parse_a', follow=True, ),
    # )


    def start_requests(self):
        header = {}
        url = 'http://weixin.sogou.com/weixin?type=2&ie=utf8&query=%E4%B8%AD%E5%B1%B1%E5%A4%A7%E5%AD%A6&tsn=1&ft=&et=&interation=&wxid=&usip='

        cookies = 'SUV=1523436225574618; SMYUV=1523436225575213; UM_distinctid=162b3e0091a2ba-01fc39976b5738-3a614f0b-2a3000-162b3e0091da3; CXID=54EFD3B6AF8E1180937038ED9DF037BC; SUID=D8E617743665860A5ACF2C9A0007454B; IPLOC=CN4401; ad=53VSSkllll2z8hhzlllllV7ffg9lllllNxKuLlllll9llllllZlll5@@@@@@@@@@; SUIR=33753809797D17825CCBDA08796168C7; SNUID=92B2FACABBBECC8A2CF8B16DBC6A438F; sct=15'

        c = self.stringToDict(cookies)
        print c
        req = scrapy.Request(url=url,callback=self.parse_b,cookies=c)
        yield req


    def parse_b(self, response):
        print response.status
        print response.url

    def parse_a(self, response):
        # selector = Selector(response)
        # url = selector.xpath('//img[@class="pic-large"]')
        print response.url

    def stringToDict(self, cookies):
        '''
        转cookes
        :param cookies:
        :return:
        '''
        itemDict = {}
        items = cookies.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict