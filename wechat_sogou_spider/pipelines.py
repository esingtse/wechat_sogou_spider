# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json,redis
from wechat_sogou_spider.items import WechatSogouSpiderItem

class WechatSogouSpiderPipeline(object):
    def __init__(self):
        # 连接Redis
        try:
            redis_config = {
                "host": "127.0.0.1",
                "port": 6379
            }
            self.redis_server = redis.Redis(**redis_config)
            print 'Connect to redis successfully!'
        except Exception as ex:
            self.log('Connect to redis failed! error:{1}'.format(ex))

    def process_item(self, item, spider):
        if isinstance(item, WechatSogouSpiderItem):
            for key in WechatSogouSpiderItem.fields:
                if item.get(key)==None:
                    item[key]=''
            self.insert_content_info(item)

    def insert_content_info(self, item):
        '''
        插入微信内容
        :param item:
        :return:
        '''
        postItem = dict(item)  # 把item转化成字典形式
        postItem = json.dumps(postItem)
        print postItem
        self.redis_server.lpush('wechat_fetch_spider:wechat_content', postItem)
