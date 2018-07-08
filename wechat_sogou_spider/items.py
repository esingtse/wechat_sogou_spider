# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class WechatSogouSpiderItem(scrapy.Item):
    title = scrapy.Field()
    pub_time = scrapy.Field()
    content = scrapy.Field()
    page_url = scrapy.Field()
    site_name = scrapy.Field()
    site_domain = scrapy.Field()
    grab_time = scrapy.Field()
