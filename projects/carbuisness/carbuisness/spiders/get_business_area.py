# -*- coding: utf-8 -*-
"""

C2017-40

"""
import scrapy
from carbuisness.items import BusinessAreaItem
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

website='get_business_area_for_geo'

class CarSpider(scrapy.Spider):

    name=website
    start_urls = [
        "http://api.map.baidu.com/library/CityList/1.4/examples/CityList.html",
        # "http://lz.58.com/shangpu/31705810263345x.shtml"
    ]

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

        desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
        desired_capabilities[
            "phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
        desired_capabilities["phantomjs.page.settings.loadImages"] = False
        self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'],
                                           desired_capabilities=desired_capabilities)
        super(CarSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self):
        self.browser.quit()

    def parse(self, response):
        province_list = response.xpath("//*[@id='container']/select[1]/option")[1:]
        for province in province_list:
            province_name = province.xpath("text()").extract_first()
            province_id = province.xpath("@value").extract_first()
            url = "http://api.map.baidu.com/shangquan/forward/?qt=sub_area_list&ext=1&level=1&areacode=%s&business_flag=0" % province_id
            yield scrapy.Request(url=url, meta={"province_name":province_name, "province_id":province_id}, callback=self.parse_subarea)

    def parse_subarea(self, response):
        data_obj = json.loads(response.body)
        if data_obj["content"]["area_type"] == 1:
            subarea_list = data_obj["content"]["sub"]
            for subarea in subarea_list:
                subarea_name = subarea["area_name"]
                subarea_id = subarea["area_code"]
                business_flag = subarea["sup_business_area"] if subarea.has_key("sup_business_area") else 0

                meta = {
                    "subarea_name": subarea_name,
                    "subarea_id": subarea_id,
                }
                meta = dict(meta, **response.meta)

                url = "http://api.map.baidu.com/shangquan/forward/?qt=sub_area_list&ext=1&level=1&areacode=%s&business_flag=%d" % (subarea_id, business_flag)
                yield scrapy.Request(url=url, meta=meta, callback=self.parse_district)
        elif data_obj["content"]["area_type"] == 2:
            district_list = data_obj["content"]["sub"]
            for district in district_list:
                district_name = district["area_name"]
                district_id = district["area_code"]
                business_flag = district["sup_business_area"] if district.has_key("sup_business_area") else 0

                meta = {
                    "district_name": district_name,
                    "district_id": district_id,
                }
                meta = dict(meta, **response.meta)
                url = "http://api.map.baidu.com/shangquan/forward/?qt=sub_area_list&ext=1&level=1&areacode=%s&business_flag=%d" % (district_id, business_flag)
                yield scrapy.Request(url=url, meta=meta, callback=self.parse_data)


    def parse_district(self, response):
        district_obj = json.loads(response.body)
        district_list = district_obj["content"]["sub"]
        for district in district_list:
            district_name = district["area_name"]
            district_id = district["area_code"]
            business_flag = district["sup_business_area"] if district.has_key("sup_business_area") else 0

            meta = {
                "district_name": district_name,
                "district_id": district_id,
            }
            meta = dict(meta, **response.meta)
            url = "http://api.map.baidu.com/shangquan/forward/?qt=sub_area_list&ext=1&level=1&areacode=%s&business_flag=%d" % (
            district_id, business_flag)
            yield scrapy.Request(url=url, meta=meta, callback=self.parse_data)

    def parse_data(self, response):
        data_obj = json.loads(response.body)
        for business_area in data_obj["content"]["sub"]:
            item = BusinessAreaItem()
            item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
            item["url"] = response.url
            item['status'] = response.url + "-" + str(data_obj["content"]["sub"].index(business_area))
            item['province_name'] = response.meta["province_name"]
            item['province_id'] = response.meta["province_id"]
            try:
                item['subarea_name'] = response.meta["subarea_name"]
                item['subarea_id'] = response.meta["subarea_id"]
            except Exception as e:
                pass
            item['district_name'] = response.meta["district_name"]
            item['district_id'] = response.meta["district_id"]
            item['business_area_name'] = business_area["area_name"]
            item['business_area_id'] = business_area["area_code"]
            item['business_geo'] = business_area["business_geo"]
            item['business_type'] = business_area["business_type"]
            item['geo'] = business_area['geo'].split("|")[-1].replace(";", "")
            # print(item)
            yield item




