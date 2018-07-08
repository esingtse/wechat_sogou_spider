# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random,redis,logging,time,json
from scrapy import signals
from wechat_sogou_spider.user_agents import agents
from scrapy.exceptions import IgnoreRequest
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from wechat_sogou_spider.spiders.cookies import CookiesManager
from scrapy.utils.response import response_status_message
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

class RandomUserAgentMiddleware(UserAgentMiddleware):
    """
    生成随机的User-Agent
    """

    def __init__(self, user_agent):
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        o = cls(crawler.settings['USER_AGENTS'])
        crawler.signals.connect(o.spider_opened, signal=signals.spider_opened)
        return o

    def process_request(self, request, spider):
        agent = random.choice(self.user_agent)
        request.headers['User-Agent'] = agent


# class CookiesManagerMiddleware(RetryMiddleware):
#     def __init__(self, settings):
#         RetryMiddleware.__init__(self, settings=settings)
#         self.rconn = redis.Redis(settings.get('REDIS_HOST', 'localhsot'), settings.get('REDIS_PORT', 6379))
#         self.cookiemanager = CookiesManager()
#         self.cookiemanager.init_all_cookies(self.rconn)
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(crawler.settings)
#
#     def process_request(self, request, spider):
#         hkey = 'wechat:cookie'
#         accountlist = self.rconn.hkeys(hkey)
#
#         # 随机cookies
#         account = random.choice(accountlist)
#         cookies = json.loads(self.rconn.hget(hkey, account).decode('utf-8'))
#         request.cookies = cookies
#         request.meta["account"] = account
#
#     def process_response(self, request, response, spider):
#         if response.status in [300, 301, 302, 303]:
#             try:
#                 redirect_url = response.headers["location"]
#                 if redirect_url == 'https://mp.weixin.qq.com':  # Cookie失效
#                     logging.info("One Cookie going to update...")
#                     self.cookiemanager.updateCookie(request.meta['account'], self.rconn)
#                 # elif "weibo.cn/security" in redirect_url:  # 账号被限
#                 #     logging.info("One Account is locked! Remove it!")
#                 #     self.cookiemanager.removeCookie(request.meta["account"], self.rconn)
#                 elif "weibo.cn/pub" in redirect_url:
#                     logging.info(
#                         "Redirect to 'http://weibo.cn/pub'!( Account:%s )" % request.meta["account"].split("-")[0])
#                 reason = response_status_message(response.status)
#                 return self._retry(request, reason, spider) or response  # 重试
#             except Exception as e:
#                 raise IgnoreRequest
#         elif response.status in [403, 414]:
#             logging.info("%s! Stopping..." % response.status)
#             time.sleep(60)
#         else:
#             return response