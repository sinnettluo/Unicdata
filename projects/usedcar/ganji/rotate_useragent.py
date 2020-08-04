# -*-coding:utf-8-*-

import logging
import requests
import time
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from ganji.redial import Redial
from selenium import webdriver
from selenium.webdriver.common.proxy import ProxyType
from scrapy.conf import settings
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import scrapy


"""避免被ban策略之一：使用useragent池。

使用注意：需在settings.py中进行相应的设置。
"""

import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

class RotateUserAgentMiddleware(UserAgentMiddleware):

    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        ua = random.choice(self.user_agent_list)
        if ua:
            #显示当前使用的useragent
            #print "********Current UserAgent:%s************" %ua
            #记录
            logging.log(msg='Current UserAgent: ' + ua, level=logging.DEBUG)
            request.headers.setdefault('User-Agent', ua)

    #the default user_agent_list composes chrome,I E,firefox,Mozilla,opera,netscape
    #for more user agent strings,you can find it in http://www.useragentstring.com/pages/useragentstring.php
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    ]

from scrapy.http import HtmlResponse
class SeleniumMiddleware(object):

    def getProxy(self):
        url = 'http://120.27.216.150:5000'
        # url = 'http://101.89.150.172:5000'
        proxy = requests.get(url, auth=('admin', 'zd123456')).text[0:-6]
        return proxy

    def process_request(self, request, spider):
        if spider.name in ['aokangda','renrenche','auto51']:
            if spider.name == "guazi":
                # profile = webdriver.FirefoxProfile()
                # profile.add_extension("modify_headers-0.7.1.1-fx.xpi")
                # profile.set_preference("extensions.modify_headers.currentVersion", "0.7.1.1-fx")
                # profile.set_preference("modifyheaders.config.active", True)
                # profile.set_preference("modifyheaders.headers.count", 1)
                # profile.set_preference("modifyheaders.headers.action0", "Add")
                # profile.set_preference("modifyheaders.headers.name0", "User-Agent")
                # profile.set_preference("modifyheaders.headers.value0",
                #                        'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"')
                # profile.set_preference("modifyheaders.headers.enabled0", True)
                #
                # profile.set_preference('network.proxy.type', 1)
                # proxy_ip = self.getProxy()
                # profile.set_preference('network.proxy.http', proxy_ip[0:-6])
                # profile.set_preference('network.proxy.http_port', 18888)
                # profile.set_preference('network.proxy.no_proxies_on', 'localhost, 127.0.0.1')
                #
                # print('opening browser')
                # binary = FirefoxBinary("/home/firefox/firefox")
                # browser = webdriver.Firefox(firefox_binary=binary, executable_path=settings["FIREFOX_PATH"], firefox_profile=profile)

                # options = webdriver.ChromeOptions()
                # # options.add_argument('--proxy-server=http://%s' % self.getProxy())
                # options.add_argument(
                #     'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"')
                # print('opening browser')
                # # options.add_argument('--proxy-server=http://%s' % self.getProxy())
                # browser = webdriver.Chrome(
                #     executable_path=settings['CHROME_PATH'],
                #     chrome_options=options)

                # browser.set_page_load_timeout(300)

                # desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
                # desired_capabilities[
                #     "phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
                # proxy = webdriver.Proxy()
                # proxy.proxy_type = ProxyType.MANUAL
                # proxy.http_proxy = self.getProxy()
                # proxy.add_to_capabilities(desired_capabilities)
                #
                # spider.browser.start_session(desired_capabilities)

                spider.browser.set_page_load_timeout(30)
                # browser = webdriver.PhantomJS(executable_path="D:/phantomjs.exe",
                #                               desired_capabilities=desired_capabilities)
                # browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs", desired_capabilities=desired_capabilities)
                try:
                    spider.browser.get(request.url)
                except Exception as e:
                    print(e)
                    return request
                time.sleep(5)
                page_content = spider.browser.page_source
                # print(page_content)
                page_url = spider.browser.current_url
                # browser.quit()
                return HtmlResponse(url=page_url, body=page_content, encoding="utf-8")
            if spider.name == "youxin":
                # desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
                # desired_capabilities[
                #     "phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
                # proxy = webdriver.Proxy()
                # proxy.proxy_type = ProxyType.MANUAL
                # proxy.http_proxy = self.getProxy()
                # proxy.add_to_capabilities(desired_capabilities)
                # spider.browser.start_session(desired_capabilities)
                try:
                    spider.browser.get(request.url)
                except Exception as e:
                    print(e)
                    return request
                time.sleep(5)
                page_content = spider.browser.page_source
                page_url = spider.browser.current_url
                return HtmlResponse(url=page_url, body=page_content, encoding="utf-8")
            try:
                spider.browser.get(request.url)
            except Exception as e:
                print(e)
                return request
            if request.url in ["http://www.58.com/ershouche/changecity/","https://www.xin.com/quanguo/"]:
                time.sleep(5)
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8")


class RedialMiddleware(object):
    def process_response(self, request, response, spider):
        print(response.status)
        if spider.name in ["xcar", "zg2sc", "kaixin"]:
            if response.status == 200:
                return response
            elif response.status >= 400:
                rd = Redial()
                try:
                    rd.reconnect()
                except Exception as e:
                    print(e)
                    if str(e) == "-1":
                        rd.connect()
                    else:
                        rd.reconnect()

import requests

class ProxyMiddleware(object):

    def getProxy(self):
        url = 'http://120.27.216.150:5000'
        # url = 'http://101.89.150.172:5000'
        proxy = requests.get(url, auth=('admin', 'zd123456')).text[0:-6]
        return proxy

    def process_response(self, request, response, spider):
        print(str(response.status) + response.url)
        # if response.status == 203:
        #     print(response.body)
        if response.url == "http://m.51auto.com/shanghai?":
            return scrapy.Request(url="http://m.51auto.com/quanguo/pabmdcigf", dont_filter=True)

        return response



    def process_request(self, request, spider):
        # print(requests.url)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
        }
        cookies = {
            '_Xdwuv':'5046671120584',
        }
        if spider.name in ["xcar"]:
            # response = requests.request("get", request.url, headers=headers, cookies=cookies)
            # print(response.text)
            # return HtmlResponse(url=request.url, body=response.text, encoding="utf-8")
            # request.cookies = cookies
            # print(request.cookies)
            pass

        cookies = {
            "antispamWallToken": "3465896248d9ff0f64d3e4b6b188f2a73e260d9ee46fc2a0afd7f51f5810617e",
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            # 'Accept-Language': 'zh-CN,zh;q=0.8',
            # 'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            # 'Accept-Encoding': 'gzip, deflate, br',
            # 'Cookies': 'antispamWallToken=3465896248d9ff0f64d3e4b6b188f2a73e260d9ee46fc2a0afd7f51f5810617e',
            # 'Host': "www.renrenche.com"
        }
        # if spider.name in ['renrenche']:
        #     print(request.cookies)
        #     print(request.headers)
        #     response = requests.request("get", "https://www.renrenche.com/sh/ershouche", headers=headers, cookies=cookies)
        #     # print(response.url)
        #     return HtmlResponse(url=request.url, body=response.text, encoding="utf-8")
        #     # request.headers["User-agent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"
        #     # request.headers['Host'] = 'www.renrenche.com'
        #     # request.cookies = cookies

        if spider.name in ['che58']:
            # pass
            request.headers['Host'] = ['www.58.com']
            # request.meta['dont_redirect'] = True
            # request.meta['handle_httpstatus_list'] = [302]
        if spider.name in ['ganji']:
            request.headers['Host'] = ['www.ganji.com']
            request.headers['User-Agent'] = [
                'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36']
            request.headers['Accept-Language'] = ['zh-CN,zh;q=0.8']
            request.cookies = {
                'ganji_login_act':'1516608870216',
                'citydomain':'anshan',
                'xxzl_deviceid':'lq%2BDPCYLo%2BlXXzTrdUAMtePMYtC9NnCnMfoUesKH8KyiEFYtnz8ncqNjtfVavV4k'
            }
        if spider.name in ['hx2car', 'che58', 'ganji', 'haoche51','che168', 'youxin', 'zg2sc']:
            request.meta['proxy'] = "http://" + self.getProxy()
            request.meta['download_timeout'] = 8

            # print(request.headers)
            print(request.meta['proxy'])
        if spider.name in ['guazi']:
            # request.headers['Host'] = ['www.guazi.com']
            # if request.url.find("www") >= 0:
            #     request.headers['Referrer'] = ['https://www.guazi.com']
            request.headers['User-Agent'] = [
                'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36']
            # request.meta['proxy'] = "http://" + self.getProxy()
            request.meta['download_timeout'] = 8
            request.cookies = {
                "antipas":"55967606737348786z35F8s50d2"
            }
            request.meta['proxy'] = "http://" + self.getProxy()
            print(request.cookies)
            print(request.headers)

            # print(request.meta['proxy'])
