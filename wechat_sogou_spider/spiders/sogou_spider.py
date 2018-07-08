#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/4 16:11
# @Author  : Esing
# @File    : sogou_spider.py
# @Software: PyCharm

from scrapy.spiders.crawl import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib import quote
from scrapy.selector import Selector
from scrapy_redis.connection import get_redis_from_settings
from wechat_sogou_spider.settings import REDIS_START_URLS_KEY, KEYWORDS
import redis

class SougouSpider(CrawlSpider):
    name = "sogou_wechat"
    start_urls = []
    for keyword in KEYWORDS:
        url = 'http://weixin.sogou.com/weixin?usip=&query=%s&ft=&tsn=1&et=&interation=&type=2&wxid=&page=1&ie=utf8' % (
            quote(keyword))
        start_urls.append(url)

    # CrawSpider的规则
    rules = (
        # 下一页的所有链接
        Rule(
            LinkExtractor(
                allow="^http://weixin.sogou.com/\S*page=\d+&ie=utf8$"),
            callback='parse_article_link',
            follow=True),

        # 文章URL的所有链接
        # Rule(LinkExtractor(allow="^http://mp.weixin.qq.com\S*new=1$",
        # restrict_xpaths='//div[@class="txt-box"]/h3/a'),
        # callback='parse_article_link', follow=True),
    )

    # 抓取配置，覆盖SETTINGS的配置
    custom_settings = {
        'CONCURRENT_REQUESTS': 5,
        'DOWNLOAD_DELAY': 2,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 8,
        'DEPTH_LIMITD': 0,
        'DEPTH_PRIORITY': 1,
    }

    def parse_article_link(self, response):
        '''
        解析每页的文章临时URL
        :param response: 网页响应内容
        :return: 将结果存入Redis
        '''
        if response.status == '200':
            selector = Selector(response)
            article_links = selector.xpath(
                '//div[@class="txt-box"]/h3/a/@href')
            for link in article_links:
                # 将url写入redis
                try:
                    redis_config = {
                        "host": "192.168.0.202",
                        "port": 6379
                    }
                    self.redis_server = redis.Redis(**redis_config)
                    self.redis_server.lpush(
                        REDIS_START_URLS_KEY, 'http://mp.weixin.qq.com/s?src=11&timestamp=1530866775&ver=981&signature=LceXK8mpsPymlMCyqEFmZ9YWtOC*UxKBJzob2NqSEqUSGF*6o9a4iJp9GU2-1qjn1e4*9VNAqlZ1fKQqmLX6SkJNdT4OU*Fkkn-CNWdrLl5CLKMw9qmBFngzBFfwcoOU&new=1')
                    print 111111
                except Exception as ex:
                    self.log(
                        'redis lpush failed!!! page_url:{0} error:{1}'.format(
                            '1', ex))
        else:
            self.log('Request Fail!!!')

    # def exchange_cookies(self, cookies):
    #     '''
    #     转cookes
    #     :param cookies:
    #     :return:
    #     '''
    #     itemDict = {}
    #     items = cookies.split(';')
    #     for item in items:
    #         key = item.split('=')[0].replace(' ', '')
    #         value = item.split('=')[1]
    #         itemDict[key] = value
    #     return itemDict
