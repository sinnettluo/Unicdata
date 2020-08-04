# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import requests
import base64

# *******************************************************************************#
#                              下载器中间件-随机请求头中间件                  #
# 作用：每次请求时，随机使用一个请求头                                             #
# 相应setting中要设置请求头列表。由自定义参数USER_AGENTS 决定                      #                                        #
# *******************************************************************************#
class RandomUserAgentMiddleware(object):
    """随机响应头设置"""
    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        # print("********Current UserAgent********" + random.choice(self.agents))
        request.headers.setdefault('User-Agent', random.choice(self.agents))


# class ProxyMiddleware(object):
#     def __init__(self):
#         # 阿布云代理服务器
#         self.proxyServer = "http://http-dyn.abuyun.com:9020"
#         # 代理隧道验证信息,根据个人不同
#         proxyUser = "H1GRHO96MZI0W20D"
#         proxyPass = "861802FCBA2E537F"
#         self.proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8") # Python3
#         # self.proxyAuth = "Basic " + base64.b64encode(proxyUser + ":" + proxyPass) # Python2
#
#     def process_request(self, request, spider):
#         '''处理请求request'''
#         request.headers['Proxy-Authorization'] = self.proxyAuth
#         request.meta['proxy'] = self.proxyServer     # 这句就决定了你先将request发送到阿布云

def getProxy():
    url = 'http://120.27.216.150:5000'
    proxy = requests.get(url, auth=('admin', 'zd123456')).text[0:-6]
    return proxy


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = "http://" + getProxy()
        print('proxy success !')
        # if spider.name in ['jzg_price', 'autohome_error_new']:
        #     request.meta['proxy'] = "http://" + getProxy()
        #     print('proxy success !')

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        if response.status in [418, 502]:
            request.meta['proxy'] = "http://" + getProxy()
            return request
        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response


class XinlangSpiderMiddleware(object):
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

        # Should return either None or an iterable of Request, dict
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


class XinlangDownloaderMiddleware(object):
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
