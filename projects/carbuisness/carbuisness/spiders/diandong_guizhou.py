# -*- coding: utf-8 -*-
"""

C2017-39


"""
import scrapy
from carbuisness.items import DiandongGuizhouItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re
import random
import hashlib
from hashlib import md5
from carbuisness.getip import getProxy
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.conf import settings
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

website='diandong_guizhou'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = []


    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

        # options = webdriver.ChromeOptions()
        # options.add_argument(
        #     'user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"')
        # self.browser = webdriver.Chrome(executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe",
        #                            chrome_options=options)

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
        # self.browser = webdriver.Firefox(executable_path=settings['FIREFOX_PATH'], firefox_profile=profile)

        # desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        # desired_capabilities[
        #     "phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
        # desired_capabilities["phantomjs.page.settings.loadImages"] = False
        # self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'], desired_capabilities=desired_capabilities)


        # super(CarSpider, self).__init__()
        # dispatcher.connect(self.spider_closed, signals.spider_closed)

    # def spider_closed(self):
    #     self.browser.quit()

    def start_requests(self):
        return [scrapy.FormRequest(method="post", url="http://www.gzevc.cn/webservice/services/StationWebService/getStationPFIncreData?response=application%2Fjson", formdata={"secretkey":"1", "date_time":str(int(time.time()*1000))})]

    def parse(self, response):
        ids = re.findall("\d{24}", response.body, re.S)
        print(ids)
        for id in ids:
            url = "http://www.gzevc.cn/webservice/services/StationWebService/getStationById2?response=application%2Fjson"
            yield scrapy.FormRequest(method="post", url=url, formdata={"staId":id}, callback=self.parse_details, dont_filter=True)

    def parse_details(self, response):
        json_str = json.loads(response.text)["return"]
        json_obj = json.loads(json_str)
        # print(json_obj)

        z = json_obj["station"]
        item = DiandongGuizhouItem()
        item["id"] = z["id"] if "id" in z else "-"
        item["name"] = z["name"] if "name" in z else "-"
        item["lon"] = z["lon"] if "lon" in z else "-"
        item["lat"] = z["lat"] if "lat" in z else "-"
        item["distance"] = z["distance"] if "distance" in z else "-"
        item["staType"] = z["staType"] if "staType" in z else "-"
        item["facConf"] = z["facConf"] if "facConf" in z else "-"
        item["conPerson"] = z["conPerson"] if "conPerson" in z else "-"
        item["telephone"] = z["telephone"] if "telephone" in z else "-"
        item["addr"] = z["addr"] if "addr" in z else "-"
        item["status3"] = z["status"] if "status" in z else "-"
        item["orgName"] = z["orgName"] if "orgName" in z else "-"
        item["staIcon"] = z["staIcon"] if "staIcon" in z else "-"
        polelist = z["polelist"] if "polelist" in z else None
        if polelist:
            for p in polelist:
                item["id2"] = p["id"]
                item["name2"] = p["name"]
                item["poleType"] = p["poleType"]
                item["installSite"] = p["installSite"]
                item["powerRating"] = p["powerRating"]
                item["nomVol"] = p["nomVol"]
                item["nomCurrent"] = p["nomCurrent"]
                item["lon2"] = p["lon"]
                item["lat2"] = p["lat"]
                item["status2"] = p["status"]
                item["isBesp"] = p["isBesp"]
                item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
                item["url"] = response.url

                item["status"] = str(item["id"]) + "-" + str(item["id2"]) + "-" + time.strftime('%Y-%m-%d %H:%M', time.localtime()) + "-" + str(item["status2"])
                # print(item)
                yield item
        else:
            item["status"] = item["id"]
            # print(item)
            yield item