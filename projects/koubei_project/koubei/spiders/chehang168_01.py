# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from koubei.items import Chehang168Item
import time
# from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re
import csv
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
import random
import redis

website='chehang168_new'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = []
    custom_settings = {
        'DOWNLOAD_DELAY': 5,
        'CONCURRENT_REQUESTS': 1,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
    }

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(self.settings)
        self.counts=0
        self.carnum=800000
        self.cookies = {
            "soucheAnalytics_usertag" : "WjKeC56Vpf",
            "DEVICE_ID" : "1156331fbfb00c34d8cc46f39cb5716c",
        "_uab_collina"  : "155531505872406790895702",
        "U"  : "1495168_8ad4212494c76c922d965f13636a8a83",
        }
        self.settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        self.settings.set('MONGODB_DB','koubei',priority='cmdline')
        self.settings.set('MONGODB_COLLECTION',website,priority='cmdline')
        self.r =redis.Redis(host=self.settings["REDIS_SERVER"],port=self.settings["REDIS_PORT"],db=0)
    #     self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
    #     # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
    #     # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
    #     super(CarSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self):
    #     self.browser.quit()


    def start_requests(self):
        # try:
        #     with open("/root/familyname_log.txt", "r") as f:
        #         res = f.readlines()
        #         f.close()
        # except Exception as e:
        #     pass
        cookie = self.r.get("che168").decode("utf-8")
        headers ={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",

        }
        cookie={i.split("=")[0].strip(""):i.split("=")[1].strip("")for i in cookie.split(";")}
        return [scrapy.Request(url="http://www.chehang168.com/index.php?c=index&m=carData", headers=headers,cookies=cookie)]

    def parse(self, response):
        print(response.request.headers)
        #
        # res = ""
        #
        # try:
        #     with open("familyname_log.txt", "r") as f:
        #         res = f.read()
        #         f.close()
        # except Exception as e:
        #     pass

        # family_list = res.split("\n")
        print(response.text)
        # logging.log(msg=str(family_list), level=logging.INFO)
        res = json.loads(response.text.replace("var carData = ", ""))
        # book = csv.reader(open("chehang168_0418.csv", "r", encoding="utf-8"))
        # with open("./chehang168_0418.txt","r",encoding="utf-8")as f:
        #     book=f.readlines()
        # book = list(book)
        # # random.shuffle(book)
        book =['轩逸', '逍客', '奇骏', '劲客', '荣威eRX5', '荣威RX5', '唐新能源', '宋新能源', '秦新能源', '秦', '宋', '唐', 'POLO', '朗逸', '途观', '途观L', '途观L新能源', '丰田RAV4', '卡罗拉', '普拉多', '兰德酷路泽', '柯斯达', '腾势', '宝骏310', '宝骏530', '宝骏630', '宝骏730', '宝马1系', '宝马3系', '宝马5系', '宝马X1', '宝马X3', '艾力绅', '本田CR-V', '思铂睿', '思域', '本田UR-V', '飞度', '奥德赛', '冠道', '凌派', '雅阁', '锋范', '缤智', '宋MAX新能源', '比亚迪S7', '比亚迪S6', '比亚迪M6', '比亚迪G6', '比亚迪F0', '速锐', '奔驰A级', '奔驰C级', '奔驰E级', '奔驰GLA', '奔驰GLC', 'VELITE 5', '昂科拉', '昂科威', '别克GL6', '别克GL8', '君威', '君越', '凯越', '威朗', '英朗', '阅朗', '宝来', '高尔夫', '迈腾', '速腾', '捷达', '探岳', '大众CC', '途昂', '途安', '桑塔纳', '朗逸', '凌渡', '帕萨特', '朗境', '朗行', '辉昂', 'V5菱致', '东南DX3', '东南DX7', '东南DX3新能源', '东南A5翼舞', '帕萨特新能源', '上汽大众T-Cross', '途岳', 'T-ROC探歌', '高尔夫·嘉旅', '蔚领', 'LANNIA蓝鸟', '骊威', '楼兰', '骐达', '天籁', '西玛', '轩逸·纯电', '阳光', '途达', '奥迪A3', '奥迪A4L', '奥迪A6L', '奥迪A6L新能源', '奥迪Q2L', '奥迪Q3', '奥迪Q5', '奥迪Q5L', 'VELITE 6', '凯迪拉克ATS-L', '凯迪拉克CT6', '凯迪拉克XT4', '凯迪拉克XT5', '凯迪拉克XTS', '创酷', '科鲁泽', '科鲁兹', '科帕奇', '科沃兹', '乐风RV', '迈锐宝', '迈锐宝XL', '赛欧', '探界者', '沃兰多', '荣威350', '荣威360', '荣威550', '荣威950', '荣威e950', '荣威Ei5', '荣威ei6', '荣威i5', '荣威i6', '荣威MARVEL X', '荣威RX3', '荣威RX8', '比亚迪e1', '比亚迪e5', '比亚迪e6', '比亚迪F3', '比亚迪G5', '宋MAX', '元', '电咖·EV10', '威马EX5', '蔚来ES8', 'MODEL 3', 'MODEL S', 'MODEL X', 'EC系列', 'EU系列', 'EV系列', 'EX系列', '北汽新能源EX3', '北汽新能源EX5', '零跑S01', 'INSPIRE', '本田XR-V', 'YARiS L 致炫', '威驰', '雷凌', '凯美瑞', '丰田C-HR', '汉兰达', '福克斯', '福睿斯', '蒙迪欧', '翼虎', '锐界', '撼路者', '悦纳', '领动', '途胜', '北京现代ix35', '现代ix25', '马自达CX-4', '马自达CX-5', '五十铃MU-X', '哈弗H9', '奕歌', '欧蓝德', '威驰FS', '帝豪新能源', '轩逸']
        for row in book:
            if book.index(row) < 64:

                for brand in res:
                    for brandid in res[brand]["brand"]:
                        brandcode = brandid
                        brandname = res[brand]["brand"][brandid]["name"]
                        for familyid in res[brand]["brand"][brandid]["pserise"]:
                            familycode = familyid
                            familyidname = res[brand]["brand"][brandid]["pserise"][familyid]["name"]
                            # if row[0] == familyidname:
                                # if familyidname not in family_list:
                            # if familyidname in ["轩逸", "逍客", "奇骏", "劲客", "荣威eRX5", "荣威RX5", "唐新能源", "宋新能源", "秦新能源", "秦", "宋", "唐", "POLO", "朗逸", "途观", "途观L", "途观L新能源"]:
                            meta = {
                                "brandcode":brandcode,
                                "brandname":brandname,
                                "familycode":familycode,
                                "familyname":familyidname,
                                "count":1,
                            }
                            url = "http://www.chehang168.com/index.php?c=index&m=series&psid=%s" % (familycode.replace("'",""))
                            logging.log(msg=str(url), level=logging.INFO)
                            yield scrapy.Request(url=url, meta=meta, cookies=self.cookies, callback=self.parse_list)

    def parse_list(self, response):
        print(1)
        # print(response.text)
        # next = response.xpath("//a[contains(text(), '下一页')]")
        # if next and response.meta["count"] < 2:
        #     response.meta["count"] = response.meta["count"] + 1
        #     yield scrapy.Request(url=response.urljoin(next.xpath("@href").extract_first()), meta=response.meta, callback=self.parse_list)

        cars = response.xpath("//*[@class='ch_carlistv3']/li")
        if cars:
            with open("familyname_log.txt", "a") as f:
                f.write(response.meta["familyname"] + "\n")
            f.close()
        for car in cars:
            item = Chehang168Item()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['brandname'] = response.meta["brandname"]
            item['brandcode'] = response.meta["brandcode"]
            item['familyname'] = response.meta["familyname"]
            item['familycode'] = response.meta["familycode"]
            item['title'] = car.xpath("div/h3/a/text()").extract_first()
            item['guideprice'] = car.xpath("div/h3/b/text()").extract_first()
            item['price'] = car.xpath("div/span/b/text()").extract_first().replace("万", "")
            item['store'] = car.xpath("p[@class='c3']/a/text()").extract_first()

            item['desc1'] = car.xpath("p[@class='c1']/text()[1]").extract_first()
            item['desc2'] = car.xpath("p[@class='c2']/text()").extract_first()
            item['time'] = car.xpath("p[@class='c3']/cite[1]/text()").extract_first()
            item['desc3_2'] = car.xpath("p[@class='c3']/cite[2]/text()").extract_first()
            item['desc3_3'] = car.xpath("p[@class='c3']/cite[3]/text()").extract_first()
            item['status'] = item["title"] + "-" + item["desc1"] + "-" + item["store"]

            print(item)
            # yield item
