# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import QuanguoMonthItem
import time
# from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re
import random
import hashlib
from hashlib import md5
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
# from scrapy.conf import settings
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from lxml import etree
import requests
import pymongo

website='province_year_05'

class CarSpider(scrapy.Spider):

    name=website
    # start_urls = ["http://data.stats.gov.cn/easyquery.htm?cn=E0103"]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(self.settings)
        self.counts=0
        self.carnum=800000
        self.provs = {
            "北京市":"110000",
            "天津市": "120000",
            "河北省": "130000",
            "山西省": "140000",
            "内蒙古自治区": "150000",
            "辽宁省": "210000",
            "吉林省": "220000",
            "黑龙江省": "230000",
            "上海市": "310000",
            "江苏省": "320000",
            "浙江省": "330000",
            "安徽省": "340000",
            "福建省": "350000",
            "江西省": "360000",
            "山东省": "370000",
            "河南省": "410000",
            "湖北省": "420000",
            "湖南省": "430000",
            "广东省": "440000",
            "广西壮族自治区": "450000",
            "海南省": "460000",
            "重庆市": "500000",
            "四川省": "510000",
            "贵州省": "520000",
            "云南省": "530000",
            "西藏自治区": "540000",
            "陕西省": "610000",
            "甘肃省": "620000",
            "青海省": "630000",
            "宁夏回族自治区": "640000",
            "新疆维吾尔自治区": "650000",
        }
        self.settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        self.settings.set('MONGODB_DB','koubei',priority='cmdline')
        self.settings.set('MONGODB_COLLECTION',website,priority='cmdline')




    #     self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
    #     # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
    #     # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
    #     super(CarSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self):
    #     self.browser.quit()


    def start_requests(self):
        url = "http://data.stats.gov.cn/easyquery.htm"
        data = {
            "id":"zb",
            "dbcode":"fsnd",
            "wdcode":"zb",
            "m":"getTree",
        }
        cookies = {
            "_trs_uv": "juc2v5n9_6_4ntj",
            "JSESSIONID": "17ACADC5DB37386BAAF8B178BF92853B",
            "u": "5",
            "wzws_cid":"a40acbc8f89455ed7f76e71a45cc78dbfd97275c5e276a3ab14b89bd2526bf0c81bee1b22ef5202dddecf152a724a0c99368a6b596b569ff020322204a0aa621"
        }
        headers = {
            'Referer':'http://data.stats.gov.cn/WZWSREL2Vhc3lxdWVyeS5odG0/Y249RTAxMDM=?wzwschallenge=V1pXU19DT05GSVJNX1BSRUZJWF9MQUJFTDYxNTE4NzI=',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
            "cookies":'_trs_uv=juc2v5n9_6_4ntj; JSESSIONID=17ACADC5DB37386BAAF8B178BF92853B; u=5; wzws_cid=a40acbc8f89455ed7f76e71a45cc78dbfd97275c5e276a3ab14b89bd2526bf0c81bee1b22ef5202dddecf152a724a0c99368a6b596b569ff020322204a0aa621',
        }
        return [scrapy.FormRequest(method="post", url=url, headers=headers, cookies=cookies, formdata=data)]

    def parse(self, response):
        level1s = json.loads(response.text)
        for level1 in level1s:
            id = level1["id"]
            name = level1["name"]
            data = {
                "id": id,
                "dbcode": "fsnd",
                "wdcode": "zb",
                "m": "getTree",
            }
            meta = {
                "level1_name":name,
                "level1_id":id,
            }
            yield scrapy.FormRequest(method="post", url="http://data.stats.gov.cn/easyquery.htm", meta=meta, formdata=data, callback=self.parse_level2)

    def parse_level2(self, response):

        level2s = json.loads(response.text)
        for level2 in level2s:
            id = level2["id"]
            name = level2["name"]
            data = {
                "id": id,
                "dbcode": "fsnd",
                "wdcode": "zb",
                "m": "getTree",
            }
            meta = {
                "level2_name": name,
                "level2_id": id,
            }
            meta = dict(meta, **response.meta)
            if level2["isParent"]:
                yield scrapy.FormRequest(method="post", url="http://data.stats.gov.cn/easyquery.htm", meta=meta, formdata=data, callback=self.parse_level3)
            else:
                for prov in self.provs:
                    rstr = '[{"wdcode":"reg","valuecode":"%s"}]' % self.provs[prov]
                    qstr = '[{"wdcode":"zb","valuecode":"%s"},{"wdcode":"sj","valuecode":"LAST36"}]' % id
                    meta2 = {
                        "provincename":prov,
                        "provinceid":self.provs[prov]
                    }
                    meta = dict(meta, **meta2)
                    url = "http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=zb&colcode=sj&wds=%s&dfwds=%s" % (rstr, qstr)
                    yield scrapy.Request(url=url, meta=meta, callback=self.parse_list)

    def parse_level3(self, response):
        level3s = json.loads(response.text)
        for level3 in level3s:
            id = level3["id"]
            name = level3["name"]
            data = {
                "id": id,
                "dbcode": "fsnd",
                "wdcode": "zb",
                "m": "getTree",
            }
            meta = {
                "level3_name": name,
                "level3_id": id,
            }
            meta = dict(meta, **response.meta)
            if level3["isParent"]:
                pass
            else:
                for prov in self.provs:
                    rstr = '[{"wdcode":"reg","valuecode":"%s"}]' % self.provs[prov]
                    qstr = '[{"wdcode":"zb","valuecode":"%s"},{"wdcode":"sj","valuecode":"LAST36"}]' % id
                    meta2 = {
                        "provincename":prov,
                        "provinceid":self.provs[prov]
                    }
                    meta = dict(meta, **meta2)
                    url = "http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=fsnd&rowcode=zb&colcode=sj&wds=%s&dfwds=%s" % (rstr, qstr)
                    yield scrapy.Request(url=url, meta=meta, callback=self.parse_list)

    def parse_list(self, response):
        res = json.loads(response.text)
        # print(res)
        for d in res['returndata']['datanodes']:
            item = QuanguoMonthItem()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['data'] = d['data']['data']
            item['time'] = d['wds'][2]['valuecode']
            categoryid = d['wds'][0]['valuecode']
            for category in res['returndata']['wdnodes'][0]["nodes"]:
                if category["code"] == categoryid:
                    item["categoryname"] = category["cname"] + "(" + category["unit"] + ")"
            item['status'] = d['code']
            item['level1_name'] = response.meta['level1_name']
            item['level1_id'] = response.meta['level1_id']
            item['level2_name'] = response.meta['level2_name']
            item['level2_id'] = response.meta['level2_id']
            item['provincename'] = response.meta['provincename']
            item['provinceid'] = response.meta['provinceid']
            item['level3_name'] = response.meta['level3_name'] if "level3_name" in response.meta else "-"
            item['level3_id'] = response.meta['level3_id'] if "level3_id" in response.meta else "-"
            # print(item)
            yield item