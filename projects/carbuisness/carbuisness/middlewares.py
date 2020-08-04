# -*- coding: utf-8 -*-

import requests
import time
import mydial
import scrapy

# ips = []
# with open('ips.txt', "r") as myip:
#     ips.append(myip.readlines())
#
# def writeip(ip):
#     with open('ips.txt', "a+") as myip:
#         text = ip + "\n"
#         myip.write(text)

# class MyproxiesSpiderMiddleware(object):
#     # def __init__(self, ip=''):
#         # self.ip = ip
#     def getProxy(self):
#         url = 'http://123.206.184.71:5000'
#         proxy = requests.get(url, auth=('admin', 'zd123456')).text
#         return proxy
#
#     def verification_code_test(self, response):
#         # test = []
#         test = response.xpath('//div[@class="container"]/p[@id="authType"]')  # 链家，存在验证码
#         # test.append(test1)
#         if test:
#             return True
#         else:
#             return False
#
#     # def process_request(self, request, spider):
#     #     # thisip = random.choice(IPPOOL)
#     #     ip = self.getProxy()
#     #     # time.sleep(15)
#     #     print("this is ip:" + ip)
#     #     request.meta["proxy"] = "http://" + ip
#
#     def process_response(self, response, request, spider):
#         # test = response.xpath('//div[@class="container"]/p[@id="authType"]')    # 链家，存在验证码
#     #     self.verification_code_test(response)
#     #
#     #     # if test:# or response.status>200:
#         if self.verification_code_test(response):
#     #         # ip = self.getProxy()
#     #         # while ip in ips:
#     #         #     time.sleep(8)
#     #         #     ip = self.getProxy()
#     #         # ips.append(ip)
#     #         # writeip(ip)
#     #         # request.meta["proxy"] = "http://" + ip
#     #         # print "--------------------------"
#     #         # print ip
#     #         # print "--------------------------"
#     #         # new_request = request.replace(url=request.meta['redirect_urls'][0])
#     #         # # request.replace([request.meta['url']], )
#     #         # return new_request
#             mydial.click()
#             return request
#         return response


class MyproxiesSpiderMiddleware(object):

    def __init__(self,**kwargs):
        # super(MyproxiesSpiderMiddleware,self).__init__(**kwargs)
        self.xpath_list = [
            '//div[@class="container"]/p[@id="authType"]',  # 链家，存在验证码
            '//div[@class="code_num"]/input[@id="btnSubmit"]',  # 58同城存在验证码
        ]

    def check_code(self, html):                         # 检查是否满足拨号条件，如果存在异常，就拨号
        """
        :param html:    参数html是网页源代码
        :return:        如果网页检测出需要拨号，返回True，不需要拨号则返回False
        """
        domtext = scrapy.selector.Selector(text=html)
        for i in self.xpath_list:
            test = domtext.xpath(i)
            if test:
                return True
        return False

    def process_response(self, request, response, spider):
        html = response.body
        if self.check_code(html):
            mydial.click()          # 拨号
            return request
        return response

        # test = response.xpath('//div[@class="container"]/p[@id="authType"]')  # 链家，存在验证码
        # city_wide = response.xpath('//div[@class="code_num"]/input[@id="btnSubmit"]')   # 58同城存在验证码
        # if test:
        #     mydial.click()
        #     return request
        # return response

