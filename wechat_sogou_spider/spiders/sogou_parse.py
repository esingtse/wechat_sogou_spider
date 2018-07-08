#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/7/6 14:05
# @Author  : Esing
# @File    : sogou_parse.py
# @Software: PyCharm

import datetime as DT
from bs4 import BeautifulSoup
from scrapy_splash import SplashRequest
from scrapy_redis.spiders import RedisSpider
from wechat_sogou_spider.items import WechatSogouSpiderItem
from urlparse import urlparse

class SogouFeterSpider(RedisSpider):
    name = "sogouSpider"

    def make_requests_from_url(self, url):
        '''
        重写Spider基类的方法
        :param url:
        :return:
        '''
        return SplashRequest(url)

    def parse(self, response):
        '''
        解析页面详细信息
        :param response:
        :return:
        '''
        soup = BeautifulSoup(
            response.body,
            "html.parser",
            from_encoding="gb18030")
        website_url = response.url

        if soup.select('div.text_area > div.global_error_msg.warn'):
            self.log(u'website_url: {} 该内容已被发布者删除'.format(website_url))
            return

        if soup.select('div.icon_area > i.icon_msg.warn'):
            self.log(u'website_url: {} 此内容因违规无法查看'.format(website_url))
            return

        item = WechatSogouSpiderItem()
        # 解析标题
        title_script = soup.select('div#img-content > h2 > script')
        if len(title_script):
            title_script[0].decompose()
        item['title'] = None
        title = soup.select('div#img-content > h2')
        if title:
            item['title'] = self.trip_text(title[0].text)
        else:
            self.log('wechat_url: {} parse article_title failed'.format(website_url))

        # 解析发布时间
        item['pub_time'] = None
        pub_time = soup.select('div#meta_content > em#publish_time')
        if pub_time:
            pub_time_str = self.trip_text(pub_time[0].text)[:20]
            if pub_time_str == '今天' or pub_time_str == 'Today':
                item['pub_time'] = DT.datetime.now().strftime("%Y-%m-%d")
            elif pub_time_str == '昨天' or pub_time_str == 'Yesterday':
                item['pub_time'] = DT.date.today() - DT.timedelta(days=1)
        else:
            self.log('website_url: {} parse pub_time failed'.format(website_url))

        # 解析内容
        item['content'] = None
        content = soup.select('div#js_content')
        if content:
            item['content'] = self.trip_text(content[0].text)
        else:
            self.log('website_url: {} parse article_content failed'.format(website_url))

        item['site_name'] = '搜狗搜索'
        pr = urlparse(response.url)
        item['site_domain'] = pr.netloc
        item['grab_time'] = DT.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['page_url'] = website_url
        yield item

    def trip_text(self, t):
        return t.replace(' ', '').replace('\n', '').replace('\r', '')