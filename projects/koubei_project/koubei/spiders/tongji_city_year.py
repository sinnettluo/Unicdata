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

website='city_year_05'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = ["http://data.stats.gov.cn/easyquery.htm?cn=E0105"]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(self.settings)
        self.counts=0
        self.carnum=800000
        self.citydict = {}
        self.citystr = '<ul><li node="{&quot;code&quot;:&quot;&quot;,&quot;name&quot;:&quot;序列&quot;,&quot;sort&quot;:&quot;4&quot;}" style="border-bottom: 1px solid rgb(170, 170, 170);">序列</li><li node="{&quot;code&quot;:&quot;110000&quot;,&quot;name&quot;:&quot;北京&quot;,&quot;sort&quot;:&quot;1&quot;}" code="110000" title="北京" style="border-bottom: 1px solid rgb(170, 170, 170);">北京</li><li node="{&quot;code&quot;:&quot;120000&quot;,&quot;name&quot;:&quot;天津&quot;,&quot;sort&quot;:&quot;1&quot;}" code="120000" title="天津" style="border-bottom: 1px solid rgb(170, 170, 170);">天津</li><li node="{&quot;code&quot;:&quot;130100&quot;,&quot;name&quot;:&quot;石家庄&quot;,&quot;sort&quot;:&quot;1&quot;}" code="130100" title="石家庄" style="border-bottom: 1px solid rgb(170, 170, 170);">石家庄</li><li node="{&quot;code&quot;:&quot;130200&quot;,&quot;name&quot;:&quot;唐山&quot;,&quot;sort&quot;:&quot;1&quot;}" code="130200" title="唐山" style="border-bottom: 1px solid rgb(170, 170, 170);">唐山</li><li node="{&quot;code&quot;:&quot;130300&quot;,&quot;name&quot;:&quot;秦皇岛&quot;,&quot;sort&quot;:&quot;1&quot;}" code="130300" title="秦皇岛" style="border-bottom: 1px solid rgb(170, 170, 170);">秦皇岛</li><li node="{&quot;code&quot;:&quot;140100&quot;,&quot;name&quot;:&quot;太原&quot;,&quot;sort&quot;:&quot;1&quot;}" code="140100" title="太原" style="border-bottom: 1px solid rgb(170, 170, 170);">太原</li><li node="{&quot;code&quot;:&quot;150100&quot;,&quot;name&quot;:&quot;呼和浩特&quot;,&quot;sort&quot;:&quot;1&quot;}" code="150100" title="呼和浩特" style="border-bottom: 1px solid rgb(170, 170, 170);">呼和浩特</li><li node="{&quot;code&quot;:&quot;150200&quot;,&quot;name&quot;:&quot;包头&quot;,&quot;sort&quot;:&quot;1&quot;}" code="150200" title="包头" style="border-bottom: 1px solid rgb(170, 170, 170);">包头</li><li node="{&quot;code&quot;:&quot;210100&quot;,&quot;name&quot;:&quot;沈阳&quot;,&quot;sort&quot;:&quot;1&quot;}" code="210100" title="沈阳" style="border-bottom: 1px solid rgb(170, 170, 170);">沈阳</li><li node="{&quot;code&quot;:&quot;210200&quot;,&quot;name&quot;:&quot;大连&quot;,&quot;sort&quot;:&quot;1&quot;}" code="210200" title="大连" style="border-bottom: 1px solid rgb(170, 170, 170);">大连</li><li node="{&quot;code&quot;:&quot;210600&quot;,&quot;name&quot;:&quot;丹东&quot;,&quot;sort&quot;:&quot;1&quot;}" code="210600" title="丹东" style="border-bottom: 1px solid rgb(170, 170, 170);">丹东</li><li node="{&quot;code&quot;:&quot;210700&quot;,&quot;name&quot;:&quot;锦州&quot;,&quot;sort&quot;:&quot;1&quot;}" code="210700" title="锦州" style="border-bottom: 1px solid rgb(170, 170, 170);">锦州</li><li node="{&quot;code&quot;:&quot;220100&quot;,&quot;name&quot;:&quot;长春&quot;,&quot;sort&quot;:&quot;1&quot;}" code="220100" title="长春" style="border-bottom: 1px solid rgb(170, 170, 170);">长春</li><li node="{&quot;code&quot;:&quot;220200&quot;,&quot;name&quot;:&quot;吉林&quot;,&quot;sort&quot;:&quot;1&quot;}" code="220200" title="吉林" style="border-bottom: 1px solid rgb(170, 170, 170);">吉林</li><li node="{&quot;code&quot;:&quot;230100&quot;,&quot;name&quot;:&quot;哈尔滨&quot;,&quot;sort&quot;:&quot;1&quot;}" code="230100" title="哈尔滨" style="border-bottom: 1px solid rgb(170, 170, 170);">哈尔滨</li><li node="{&quot;code&quot;:&quot;231000&quot;,&quot;name&quot;:&quot;牡丹江&quot;,&quot;sort&quot;:&quot;1&quot;}" code="231000" title="牡丹江" style="border-bottom: 1px solid rgb(170, 170, 170);">牡丹江</li><li node="{&quot;code&quot;:&quot;310000&quot;,&quot;name&quot;:&quot;上海&quot;,&quot;sort&quot;:&quot;1&quot;}" code="310000" title="上海" style="border-bottom: 1px solid rgb(170, 170, 170);">上海</li><li node="{&quot;code&quot;:&quot;320100&quot;,&quot;name&quot;:&quot;南京&quot;,&quot;sort&quot;:&quot;1&quot;}" code="320100" title="南京" style="border-bottom: 1px solid rgb(170, 170, 170);">南京</li><li node="{&quot;code&quot;:&quot;320200&quot;,&quot;name&quot;:&quot;无锡&quot;,&quot;sort&quot;:&quot;1&quot;}" code="320200" title="无锡" style="border-bottom: 1px solid rgb(170, 170, 170);">无锡</li><li node="{&quot;code&quot;:&quot;320300&quot;,&quot;name&quot;:&quot;徐州&quot;,&quot;sort&quot;:&quot;1&quot;}" code="320300" title="徐州" style="border-bottom: 1px solid rgb(170, 170, 170);">徐州</li><li node="{&quot;code&quot;:&quot;321000&quot;,&quot;name&quot;:&quot;扬州&quot;,&quot;sort&quot;:&quot;1&quot;}" code="321000" title="扬州" style="border-bottom: 1px solid rgb(170, 170, 170);">扬州</li><li node="{&quot;code&quot;:&quot;330100&quot;,&quot;name&quot;:&quot;杭州&quot;,&quot;sort&quot;:&quot;1&quot;}" code="330100" title="杭州" style="border-bottom: 1px solid rgb(170, 170, 170);">杭州</li><li node="{&quot;code&quot;:&quot;330200&quot;,&quot;name&quot;:&quot;宁波&quot;,&quot;sort&quot;:&quot;1&quot;}" code="330200" title="宁波" style="border-bottom: 1px solid rgb(170, 170, 170);">宁波</li><li node="{&quot;code&quot;:&quot;330300&quot;,&quot;name&quot;:&quot;温州&quot;,&quot;sort&quot;:&quot;1&quot;}" code="330300" title="温州" style="border-bottom: 1px solid rgb(170, 170, 170);">温州</li><li node="{&quot;code&quot;:&quot;330700&quot;,&quot;name&quot;:&quot;金华&quot;,&quot;sort&quot;:&quot;1&quot;}" code="330700" title="金华" style="border-bottom: 1px solid rgb(170, 170, 170);">金华</li><li node="{&quot;code&quot;:&quot;340100&quot;,&quot;name&quot;:&quot;合肥&quot;,&quot;sort&quot;:&quot;1&quot;}" code="340100" title="合肥" style="border-bottom: 1px solid rgb(170, 170, 170);">合肥</li><li node="{&quot;code&quot;:&quot;340300&quot;,&quot;name&quot;:&quot;蚌埠&quot;,&quot;sort&quot;:&quot;1&quot;}" code="340300" title="蚌埠" style="border-bottom: 1px solid rgb(170, 170, 170);">蚌埠</li><li node="{&quot;code&quot;:&quot;340800&quot;,&quot;name&quot;:&quot;安庆&quot;,&quot;sort&quot;:&quot;1&quot;}" code="340800" title="安庆" style="border-bottom: 1px solid rgb(170, 170, 170);">安庆</li><li node="{&quot;code&quot;:&quot;350100&quot;,&quot;name&quot;:&quot;福州&quot;,&quot;sort&quot;:&quot;1&quot;}" code="350100" title="福州" style="border-bottom: 1px solid rgb(170, 170, 170);">福州</li><li node="{&quot;code&quot;:&quot;350200&quot;,&quot;name&quot;:&quot;厦门&quot;,&quot;sort&quot;:&quot;1&quot;}" code="350200" title="厦门" style="border-bottom: 1px solid rgb(170, 170, 170);">厦门</li><li node="{&quot;code&quot;:&quot;350500&quot;,&quot;name&quot;:&quot;泉州&quot;,&quot;sort&quot;:&quot;1&quot;}" code="350500" title="泉州" style="border-bottom: 1px solid rgb(170, 170, 170);">泉州</li><li node="{&quot;code&quot;:&quot;360100&quot;,&quot;name&quot;:&quot;南昌&quot;,&quot;sort&quot;:&quot;1&quot;}" code="360100" title="南昌" style="border-bottom: 1px solid rgb(170, 170, 170);">南昌</li><li node="{&quot;code&quot;:&quot;360400&quot;,&quot;name&quot;:&quot;九江&quot;,&quot;sort&quot;:&quot;1&quot;}" code="360400" title="九江" style="border-bottom: 1px solid rgb(170, 170, 170);">九江</li><li node="{&quot;code&quot;:&quot;360700&quot;,&quot;name&quot;:&quot;赣州&quot;,&quot;sort&quot;:&quot;1&quot;}" code="360700" title="赣州" style="border-bottom: 1px solid rgb(170, 170, 170);">赣州</li><li node="{&quot;code&quot;:&quot;370100&quot;,&quot;name&quot;:&quot;济南&quot;,&quot;sort&quot;:&quot;1&quot;}" code="370100" title="济南" style="border-bottom: 1px solid rgb(170, 170, 170);">济南</li><li node="{&quot;code&quot;:&quot;370200&quot;,&quot;name&quot;:&quot;青岛&quot;,&quot;sort&quot;:&quot;1&quot;}" code="370200" title="青岛" style="border-bottom: 1px solid rgb(170, 170, 170);">青岛</li><li node="{&quot;code&quot;:&quot;370600&quot;,&quot;name&quot;:&quot;烟台&quot;,&quot;sort&quot;:&quot;1&quot;}" code="370600" title="烟台" style="border-bottom: 1px solid rgb(170, 170, 170);">烟台</li><li node="{&quot;code&quot;:&quot;370800&quot;,&quot;name&quot;:&quot;济宁&quot;,&quot;sort&quot;:&quot;1&quot;}" code="370800" title="济宁" style="border-bottom: 1px solid rgb(170, 170, 170);">济宁</li><li node="{&quot;code&quot;:&quot;410100&quot;,&quot;name&quot;:&quot;郑州&quot;,&quot;sort&quot;:&quot;1&quot;}" code="410100" title="郑州" style="border-bottom: 1px solid rgb(170, 170, 170);">郑州</li><li node="{&quot;code&quot;:&quot;410300&quot;,&quot;name&quot;:&quot;洛阳&quot;,&quot;sort&quot;:&quot;1&quot;}" code="410300" title="洛阳" style="border-bottom: 1px solid rgb(170, 170, 170);">洛阳</li><li node="{&quot;code&quot;:&quot;410400&quot;,&quot;name&quot;:&quot;平顶山&quot;,&quot;sort&quot;:&quot;1&quot;}" code="410400" title="平顶山" style="border-bottom: 1px solid rgb(170, 170, 170);">平顶山</li><li node="{&quot;code&quot;:&quot;420100&quot;,&quot;name&quot;:&quot;武汉&quot;,&quot;sort&quot;:&quot;1&quot;}" code="420100" title="武汉" style="border-bottom: 1px solid rgb(170, 170, 170);">武汉</li><li node="{&quot;code&quot;:&quot;420500&quot;,&quot;name&quot;:&quot;宜昌&quot;,&quot;sort&quot;:&quot;1&quot;}" code="420500" title="宜昌" style="border-bottom: 1px solid rgb(170, 170, 170);">宜昌</li><li node="{&quot;code&quot;:&quot;420600&quot;,&quot;name&quot;:&quot;襄阳&quot;,&quot;sort&quot;:&quot;1&quot;}" code="420600" title="襄阳" style="border-bottom: 1px solid rgb(170, 170, 170);">襄阳</li><li node="{&quot;code&quot;:&quot;430100&quot;,&quot;name&quot;:&quot;长沙&quot;,&quot;sort&quot;:&quot;1&quot;}" code="430100" title="长沙" style="border-bottom: 1px solid rgb(170, 170, 170);">长沙</li><li node="{&quot;code&quot;:&quot;430600&quot;,&quot;name&quot;:&quot;岳阳&quot;,&quot;sort&quot;:&quot;1&quot;}" code="430600" title="岳阳" style="border-bottom: 1px solid rgb(170, 170, 170);">岳阳</li><li node="{&quot;code&quot;:&quot;430700&quot;,&quot;name&quot;:&quot;常德&quot;,&quot;sort&quot;:&quot;1&quot;}" code="430700" title="常德" style="border-bottom: 1px solid rgb(170, 170, 170);">常德</li><li node="{&quot;code&quot;:&quot;440100&quot;,&quot;name&quot;:&quot;广州&quot;,&quot;sort&quot;:&quot;1&quot;}" code="440100" title="广州" style="border-bottom: 1px solid rgb(170, 170, 170);">广州</li><li node="{&quot;code&quot;:&quot;440200&quot;,&quot;name&quot;:&quot;韶关&quot;,&quot;sort&quot;:&quot;1&quot;}" code="440200" title="韶关" style="border-bottom: 1px solid rgb(170, 170, 170);">韶关</li><li node="{&quot;code&quot;:&quot;440300&quot;,&quot;name&quot;:&quot;深圳&quot;,&quot;sort&quot;:&quot;1&quot;}" code="440300" title="深圳" style="border-bottom: 1px solid rgb(170, 170, 170);">深圳</li><li node="{&quot;code&quot;:&quot;440800&quot;,&quot;name&quot;:&quot;湛江&quot;,&quot;sort&quot;:&quot;1&quot;}" code="440800" title="湛江" style="border-bottom: 1px solid rgb(170, 170, 170);">湛江</li><li node="{&quot;code&quot;:&quot;441300&quot;,&quot;name&quot;:&quot;惠州&quot;,&quot;sort&quot;:&quot;1&quot;}" code="441300" title="惠州" style="border-bottom: 1px solid rgb(170, 170, 170);">惠州</li><li node="{&quot;code&quot;:&quot;450100&quot;,&quot;name&quot;:&quot;南宁&quot;,&quot;sort&quot;:&quot;1&quot;}" code="450100" title="南宁" style="border-bottom: 1px solid rgb(170, 170, 170);">南宁</li><li node="{&quot;code&quot;:&quot;450300&quot;,&quot;name&quot;:&quot;桂林&quot;,&quot;sort&quot;:&quot;1&quot;}" code="450300" title="桂林" style="border-bottom: 1px solid rgb(170, 170, 170);">桂林</li><li node="{&quot;code&quot;:&quot;450500&quot;,&quot;name&quot;:&quot;北海&quot;,&quot;sort&quot;:&quot;1&quot;}" code="450500" title="北海" style="border-bottom: 1px solid rgb(170, 170, 170);">北海</li><li node="{&quot;code&quot;:&quot;460100&quot;,&quot;name&quot;:&quot;海口&quot;,&quot;sort&quot;:&quot;1&quot;}" code="460100" title="海口" style="border-bottom: 1px solid rgb(170, 170, 170);">海口</li><li node="{&quot;code&quot;:&quot;460200&quot;,&quot;name&quot;:&quot;三亚&quot;,&quot;sort&quot;:&quot;1&quot;}" code="460200" title="三亚" style="border-bottom: 1px solid rgb(170, 170, 170);">三亚</li><li node="{&quot;code&quot;:&quot;500000&quot;,&quot;name&quot;:&quot;重庆&quot;,&quot;sort&quot;:&quot;1&quot;}" code="500000" title="重庆" style="border-bottom: 1px solid rgb(170, 170, 170);">重庆</li><li node="{&quot;code&quot;:&quot;510100&quot;,&quot;name&quot;:&quot;成都&quot;,&quot;sort&quot;:&quot;1&quot;}" code="510100" title="成都" style="border-bottom: 1px solid rgb(170, 170, 170);">成都</li><li node="{&quot;code&quot;:&quot;510500&quot;,&quot;name&quot;:&quot;泸州&quot;,&quot;sort&quot;:&quot;1&quot;}" code="510500" title="泸州" style="border-bottom: 1px solid rgb(170, 170, 170);">泸州</li><li node="{&quot;code&quot;:&quot;511300&quot;,&quot;name&quot;:&quot;南充&quot;,&quot;sort&quot;:&quot;1&quot;}" code="511300" title="南充" style="border-bottom: 1px solid rgb(170, 170, 170);">南充</li><li node="{&quot;code&quot;:&quot;520100&quot;,&quot;name&quot;:&quot;贵阳&quot;,&quot;sort&quot;:&quot;1&quot;}" code="520100" title="贵阳" style="border-bottom: 1px solid rgb(170, 170, 170);">贵阳</li><li node="{&quot;code&quot;:&quot;520300&quot;,&quot;name&quot;:&quot;遵义&quot;,&quot;sort&quot;:&quot;1&quot;}" code="520300" title="遵义" style="border-bottom: 1px solid rgb(170, 170, 170);">遵义</li><li node="{&quot;code&quot;:&quot;530100&quot;,&quot;name&quot;:&quot;昆明&quot;,&quot;sort&quot;:&quot;1&quot;}" code="530100" title="昆明" style="border-bottom: 1px solid rgb(170, 170, 170);">昆明</li><li node="{&quot;code&quot;:&quot;532900&quot;,&quot;name&quot;:&quot;大理&quot;,&quot;sort&quot;:&quot;1&quot;}" code="532900" title="大理" style="border-bottom: 1px solid rgb(170, 170, 170);">大理</li><li node="{&quot;code&quot;:&quot;610100&quot;,&quot;name&quot;:&quot;西安&quot;,&quot;sort&quot;:&quot;1&quot;}" code="610100" title="西安" style="border-bottom: 1px solid rgb(170, 170, 170);">西安</li><li node="{&quot;code&quot;:&quot;620100&quot;,&quot;name&quot;:&quot;兰州&quot;,&quot;sort&quot;:&quot;1&quot;}" code="620100" title="兰州" style="border-bottom: 1px solid rgb(170, 170, 170);">兰州</li><li node="{&quot;code&quot;:&quot;630100&quot;,&quot;name&quot;:&quot;西宁&quot;,&quot;sort&quot;:&quot;1&quot;}" code="630100" title="西宁" style="border-bottom: 1px solid rgb(170, 170, 170);">西宁</li><li node="{&quot;code&quot;:&quot;640100&quot;,&quot;name&quot;:&quot;银川&quot;,&quot;sort&quot;:&quot;1&quot;}" code="640100" title="银川" style="border-bottom: 1px solid rgb(170, 170, 170);">银川</li><li node="{&quot;code&quot;:&quot;650100&quot;,&quot;name&quot;:&quot;乌鲁木齐&quot;,&quot;sort&quot;:&quot;1&quot;}" code="650100" title="乌鲁木齐" style="border-bottom: none;">乌鲁木齐</li></ul>'
        selector = etree.fromstring(self.citystr)
        cities = selector.xpath("//li")
        for city in cities[1:]:
            cityname = city.xpath("text()")[0]
            cityid = json.loads(city.xpath("@node")[0])["code"]
            self.citydict[cityid] = cityname


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
            "dbcode":"csnd",
            "wdcode":"zb",
            "m":"getTree",
        }
        return [scrapy.FormRequest(method="post", url=url, formdata=data, callback=self.parse_level2)]

    def parse(self, response):
        # print(response.text)
        level1s = json.loads(response.text)
        for level1 in level1s:
            id = level1["id"]
            name = level1["name"]
            data = {
                "id": id,
                "dbcode": "csnd",
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
                "dbcode": "csnd",
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
                for city in self.citydict:
                    rstr = '[{"wdcode":"reg","valuecode":"%s"}]' % city
                    qstr = '[{"wdcode":"zb","valuecode":"%s"},{"wdcode":"sj","valuecode":"LAST36"}]' % id
                    meta2 = {
                        "cityname":self.citydict[city],
                        "cityid":city
                    }
                    meta = dict(meta, **meta2)
                    url = "http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=csnd&rowcode=zb&colcode=sj&wds=%s&dfwds=%s" % (rstr, qstr)
                    yield scrapy.Request(url=url, meta=meta, callback=self.parse_list)

    def parse_level3(self, response):
        level3s = json.loads(response.text)
        for level3 in level3s:
            id = level3["id"]
            name = level3["name"]
            data = {
                "id": id,
                "dbcode": "csnd",
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
                for city in self.citydict:
                    rstr = '[{"wdcode":"reg","valuecode":"%s"}]' % city
                    qstr = '[{"wdcode":"zb","valuecode":"%s"},{"wdcode":"sj","valuecode":"LAST36"}]' % id
                    meta2 = {
                        "cityname":self.citydict[city],
                        "cityid":city
                    }
                    meta = dict(meta, **meta2)
                    url = "http://data.stats.gov.cn/easyquery.htm?m=QueryData&dbcode=csnd&rowcode=zb&colcode=sj&wds=%s&dfwds=%s" % (rstr, qstr)
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
            item['level1_name'] = response.meta['level1_name'] if "level1_name" in response.meta else "-"
            item['level1_id'] = response.meta['level1_id'] if "level1_name" in response.meta else "-"
            item['level2_name'] = response.meta['level2_name']
            item['level2_id'] = response.meta['level2_id']
            item['cityname'] = response.meta['cityname']
            item['cityid'] = response.meta['cityid']
            item['level3_name'] = response.meta['level3_name'] if "level3_name" in response.meta else "-"
            item['level3_id'] = response.meta['level3_id'] if "level3_id" in response.meta else "-"
            # print(item)
            yield item