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

class WechatSogouSpiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class WechatSogouSpiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class UserAgentMiddleware(object):
    '''
    换User-Agent
    '''
    def process_request(self, request, spider):
        agent = random.choice(agents)
        request.headers["User-Agent"] = agent

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