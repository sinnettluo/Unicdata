# -*-coding:utf-8-*-

import time
import random
import requests
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
from scrapy.http import HtmlResponse
import json
import logging


class ProxyMiddleware(object):

    def process_request(self, request, spider):
        if spider.name in ['tuhu_gongchangdian_2019_fix3', 'g9_opsteel', 'g8_ggang', 'g7_csesteel', 'g6_ouye', 'g3_zhaoggang2', 'g1_zhaogangwang', 'evp_fix2', 'gongxinbu_car', 'autohome_forum_pasate', 'lechebang_4s_int_10city_10miles2', 'lechebang_4s_ori_10city_10miles2', 'province_month_05','chehang168_02','chehang168_03','province_year', 'tmall', 'chehang168', 'weixiuchang_beijing', 'jd_fix2', 'dealer_rx2',  'tuhu_baoyang_dianping3', 'tuhu_tires', 'tuhu_baoyang_products', 'autohome_koubei_new', 'niuniuqiche', 'niuniuqiche_buchong', 'chuncheng_eluxing', 'iautos_modellist_fixed2',  'iautos_modellist2_fixed2', 'fagaiwei', "caizhengbu", 'gongxinbu_wjgs', 'gongxinbu_zcjd', 'gongxinbu_wjfb', 'jiaotongbu', 'https_test', 'autohome_butie', 'echongwang', 'wzfg']:
            print(self.get_Proxy())
            request.meta['proxy'] = "http://" + self.get_Proxy()
        if spider.name in ["new_weixin_%s" % settings["WEIXIN"]]:
            print(self.get_Proxy())
            request.meta['proxy'] = "http://" + self.get_Proxy()

    def process_response(self,request,response,spider):
        if response.status !=200:
            logging.log("fail_request",request.status,response.url)
            return request
        return response

    def get_Proxy(self):
        url = 'http://120.27.216.150:5000'
        proxy = requests.get(url, auth=('admin', 'zd123456')).text[0:-6]
        return proxy

class SeleniumMiddleware(object):

    def get_Proxy(self):
        url = 'http://120.27.216.150:5000'
        proxy = requests.get(url, auth=('admin', 'zd123456')).text[0:-6]
        return proxy

    def process_request(self, request, spider):

        if spider.name in ['jd'] and request.url == "https://www.jd.com/":
            spider.browser.get(request.url)
            time.sleep(2)
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8")

        if spider.name in ['gdp'] and request.url == "http://data.stats.gov.cn/easyquery.htm?cn=E0102":
            spider.browser.get(request.url)
            time.sleep(2)
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8")

        if spider.name in ['all_province_fix'] and request.url != "http://xzqh.mca.gov.cn/selectJson":
            spider.browser.get(request.url)
            time.sleep(2)
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8")

        if spider.name in ['iautos_modellist_fixed2'] and request.url == 'https://www.iautos.cn/chexing/':
            spider.browser.get(request.url)
            print("yes")
            time.sleep(2)
            return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8")

# class SetHeadersMiddleware(object):
#
#     def process_request(self, request, spider):
#         if spider.name in ["kbb"]:
#             request.headers['User-Agent'] = ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36']


class LechebangMiddleware(object):

    def __init__(self):
        self.appCode = 600

    def get_Proxy(self):
        url = 'http://120.27.216.150:5000'
        proxy = requests.get(url, auth=('admin', 'zd123456')).text[0:-6]
        return proxy

    def process_request(self, request, spider):
        if spider.name =="kbb":
            return
        # proxy_ip = self.get_Proxy()
        # proxies = {
        #     "http": "http://%s" % proxy_ip
        # }
        json_str = '{"appCode":%d}' % self.appCode
        if request.url == "http://m.lechebang.com/gateway/maintenance/getCitys":
            res = requests.request("post", request.url, json=json.loads(json_str))
            return HtmlResponse(url=request.url, body=res.text, encoding="utf-8")
        if request.url.find("getAllFirstLevelBrandType") >= 0:
            res = requests.request("post", request.url, json=request.meta)
            return HtmlResponse(url=request.url, body=res.text, encoding="utf-8")
        if request.url.find("getBrandProducerCar") >= 0:
            res = requests.request("post", request.url, json=request.meta)
            return HtmlResponse(url=request.url, body=res.text, encoding="utf-8")
        if request.url.find("getCarTypeDetail") >= 0:
            res = requests.request("post", request.url, json=request.meta)
            return HtmlResponse(url=request.url, body=res.text, encoding="utf-8")
        if request.url.find("getMaintenanceManual") >= 0:
            res = requests.request("post", request.url, json=request.meta)
            return HtmlResponse(url=request.url, body=res.text, encoding="utf-8")
        if request.url.find("getSprayItemInfoCross") >= 0:
            res = requests.request("post", request.url, json=request.meta)
            return HtmlResponse(url=request.url, body=res.text, encoding="utf-8")
        if request.url.find("queryFittingAutoMaintenance") >= 0:
            # print(request.meta)
            res = requests.request("post", request.url, json=request.meta)
            return HtmlResponse(url=request.url, body=res.text, encoding="utf-8")
        if request.url.find("queryBattery") >= 0:
            res = requests.request("post", request.url, json=request.meta)
            return HtmlResponse(url=request.url, body=res.text, encoding="utf-8")


class GangMiddleware(object):
    def __init__(self):

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        }

    def get_Proxy(self):
        url = 'http://120.27.216.150:5000'
        proxy = requests.get(url, auth=('admin', 'zd123456')).text[0:-6]
        return proxy

    def process_request(self, request, spider):
        if spider.name == 'g1_zhaogangwang':
            res = requests.request("post", request.url, json=request.meta, headers=self.headers)
            return HtmlResponse(url=request.url, body=res.text, request=request, encoding="utf-8")