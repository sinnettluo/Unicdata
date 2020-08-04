# -*- coding: utf-8 -*-
"""

C2017-40

"""
import os
import scrapy
from carbuisness.items import JzgPriceItem
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
from lxml import etree
import requests
import MySQLdb
import pymongo
import datetime
import pytesseract
from PIL import Image

website='jzg_price_test_img_2019'


class CarSpider(scrapy.Spider):

    name=website
    start_urls = []

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000
        self.city_count = 0

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','residual_value',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

        # self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])
        # self.browser = webdriver.PhantomJS(executable_path="/usr/local/phantomjs/bin/phantomjs")
        # self.browser = webdriver.PhantomJS(executable_path="/root/home/phantomjs")
        # super(CarSpider, self).__init__()
        # dispatcher.connect(self.spider_closed, signals.spider_closed)

    # def spider_closed(self):
    #     self.browser.quit()
    def start_requests(self):
        yield scrapy.FormRequest(method="post", url="http://common.jingzhengu.com/area/getProvList")

    def parse(self, response):
        provs = json.loads(response.text)
        for prov in provs["list"]:
            yield scrapy.FormRequest(url='http://common.jingzhengu.com/area/getCityListByProvId', formdata={"provId":str(prov["areaId"])}, callback=self.parse_city)

    def parse_city(self, response):
        mysqlconnection = MySQLdb.connect("192.168.1.94", "root", "Datauser@2017", 'people_zb', 3306)
        dbc = mysqlconnection.cursor()
        mysqlconnection.set_character_set('utf8')
        dbc.execute('SET NAMES utf8;')
        dbc.execute('SET CHARACTER SET utf8;')
        dbc.execute('SET character_set_connection=utf8;')

        sql = "select cityname from jingzhengu_city"
        dbc.execute(sql)
        res = dbc.fetchall()
        dbc.close()
        mysqlconnection.close()

        citylist = []
        for row in res:
            citylist.append(row[0])

        cities = json.loads(response.text)
        final_city_list = {}
        for city in cities["list"]:
            if city["areaName"] in citylist:
                final_city_list[city["areaId"]] = city["areaName"]

        self.city_count += len(final_city_list)
        # print(self.city_count)
        # print(final_city_list)

        connection = pymongo.MongoClient("192.168.1.94", 27017)
        db = connection["residual_value"]
        collection = db["jzg_modellist2"]

        data = collection.find()
        for model in data:

            min_year = int(model["make_year"]) - 1
            if int(model["next_year"]) == int(time.strftime('%Y', time.localtime())):
                max_year = int(model["next_year"])
            elif int(model["next_year"]) == int(time.strftime('%Y', time.localtime())) - 1:
                max_year = int(model["next_year"]) + 1
            else:
                max_year = int(model["next_year"]) + 2
            month = datetime.datetime.now().month
            # month = str(time.strftime('%m', time.localtime()))
            # if int(month) < 10:
            #     month = str(0) + str(month)
            # print(max_year)
            for i in range(min_year, max_year):
                mile = 2 * (int(time.strftime('%Y', time.localtime()))-i)
                # print(mile)
                final_city_list = {"2401":u"上海"}
                # for c in {"2401":u"上海"}:
                for c in final_city_list:
                    formdata = {
                        "sourcetype": "3",
                        "regdate": "%s-%s-1" % (str(i), month),
                        "cityname": final_city_list[c],
                        "CityId": str(c),
                        "styleid": str(model["modelid"]),
                        "uid": "0",
                        "op": "GetValuationInfo",
                        "mileage": str(mile*10000),
                        # "sign": "27B900C60B10581444D6F55126074414"
                    }
                    # print(formdata)
                    url_sell = "http://appraise.jingzhengu.com/sale-s%s-r%s-m%s-c%s-y-j-h" % (formdata['styleid'], formdata['regdate'], formdata['mileage'], formdata['CityId'])
                    url_buy = "http://appraise.jingzhengu.com/buy-s%s-r%s-m%s-c%s-y-j-h" % (formdata['styleid'], formdata['regdate'], formdata['mileage'], formdata['CityId'])
                    # print(url)
                    yield scrapy.Request(url=url_sell, meta=dict({"type":"sell"}, **formdata), callback=self.parse_price)
                    yield scrapy.Request(url=url_buy, meta=dict({"type":"buy"}, **formdata), callback=self.parse_price)


                    # yield scrapy.FormRequest(url="http://ptvapi.guchewang.com/APPV5/SellCarAppraiseResultv1.ashx", formdata=formdata, callback=self.parse_price)


    def parse_img(self, url, status):

        date_str = time.strftime('%Y-%m-%d', time.localtime())


        img_res = requests.request("get", url=url, headers={
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"})
        with open("blm/img_temp/%s.jpg" % (status), "ab") as f:
            f.write(img_res.content)
            f.close()

        try:
            img = Image.open("blm/img_temp/%s.jpg" % (status))
            img_str = pytesseract.image_to_string(img)
            os.remove("blm/img_temp/%s.jpg" % status)
        except Exception as e:
            logging.log(msg=str(e), level=logging.INFO)
            os.remove("blm/img_temp/%s.jpg" % status)
            return 0
        return re.findall("^\d+\.\d{2}", img_str)[0]



    def parse_price(self, response):

        # print(response.text)
        # res = json.loads(response.text)
        item = JzgPriceItem()
        item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
        item["url"] = response.url
        # item['brandid'] = res["MakeId"]
        # item['familyid'] = res["ModelId"]
        item['modelid'] = response.meta["styleid"]
        # item['brandname'] = res["MakeName"]
        # item['familyname'] = res["ModelName"]
        # item['model_full_name'] = res["ModelFullName"]
        # item['HBBZ'] = res["HBBZ"]
        # item['RegDateTime'] = res["RegDateTime"]
        item['RegDate'] = response.meta["regdate"]
        # item['MarketMonthNum'] = res["MarketMonthNum"]
        item['Mileage'] = response.meta["mileage"]
        # item['ProvId'] = res["ProvId"]
        # item['ProvName'] = res["ProvName"]
        item['CityId'] = response.meta["CityId"]
        item['CityName'] = response.meta["cityname"]
        # item['NowMsrp'] = res["NowMsrp"]
        # item['C2BALowPrice'] = res["C2BALowPrice"]
        # item['C2BAMidPrice'] = res["C2BAMidPrice"]
        # item['C2BAUpPrice'] = res["C2BAUpPrice"]
        # item['C2BBLowPrice'] = res["C2BBLowPrice"]
        # item['C2BBMidPrice'] = res["C2BBMidPrice"]
        # item['C2BBUpPrice'] = res["C2BBUpPrice"]
        # item['C2BCLowPrice'] = res["C2BCLowPrice"]
        # item['C2BCMidPrice'] = res["C2BCMidPrice"]
        # item['C2BCUpPrice'] = res["C2BCUpPrice"]
        # item['C2CALowPrice'] = res["C2CALowPrice"]
        # item['C2CAMidPrice'] = res["C2CAMidPrice"]
        # item['C2CAUpPrice'] = res["C2CAUpPrice"]
        # item['C2CBLowPrice'] = res["C2CBLowPrice"]
        # item['C2CBMidPrice'] = res["C2CBMidPrice"]
        # item['C2CBUpPrice'] = res["C2CBUpPrice"]
        # item['C2CCLowPrice'] = res["C2CCLowPrice"]
        # item['C2CCMidPrice'] = res["C2CCMidPrice"]
        # item['C2CCUpPrice'] = res["C2CCUpPrice"]
        # item['PriceLevel'] = res["PriceLevel"]
        # item['BaoZhilvRank'] = res["BaoZhilvRank"]
        # item['BaoZhilvCityId'] = res["BaoZhilvCityId"]
        # item['BaoZhilvCityName'] = res["BaoZhilvCityName"]
        # item['BaoZhilvLevel'] = res["BaoZhilvLevel"]
        # item['BaoZhilvLevelName'] = res["BaoZhilvLevelName"]
        # item['BaoZhilvPercentage ']= res["BaoZhilvPercentage"]
        # item['maxPrice'] = res["maxPrice"]
        # item['minLoanRate'] = res["minLoanRate"]
        # item['ShareUrl'] = res["ShareUrl"]
        # item['PlatNumber'] = res["PlatNumber"]
        item['type'] = response.meta['type']

        item["status"] = item["RegDate"] + "-" + item["Mileage"] + "-" + item["CityId"] + "-" + item["modelid"] + "-" + \
                         item['type'] + "-" + time.strftime('%Y-%m', time.localtime())

        if item['type'] == "sell":
            item['C2BMidPrice_sell'] = response.xpath("//*[@class='w_carpricinfobox clearfix']/div[1]/ul/li[2]/input[@id='hdC2BMidPrice']/@value").extract_first()

            item['C2BLowPrice_sell_img'] = response.urljoin(response.xpath("//*[@class='w_carpricinfobox clearfix']/div[1]/ul/li[1]/span[3]/img/@src").extract_first().replace("2_2", "2_1"))
            item['C2BLowPrice_sell_img'] = self.parse_img(item['C2BLowPrice_sell_img'],
                                                      item['status'] + "-" + "C2BLowPrice_sell_img")
            item['C2BUpPrice_sell_img'] = response.urljoin(response.xpath("//*[@class='w_carpricinfobox clearfix']/div[1]/ul/li[3]/span[3]/img/@src").extract_first().replace("2_2", "2_1"))
            item['C2BUpPrice_sell_img'] = self.parse_img(item['C2BUpPrice_sell_img'],
                                                      item['status'] + "-" + "C2BUpPrice_sell_img")
            item['C2CMidPrice_sell_img'] = response.urljoin(response.xpath("//*[@class='w_carpricinfobox clearfix']/div[2]/ul/li[2]/span[3]/img/@src").extract_first().replace("2_2", "2_1"))
            item['C2CMidPrice_sell_img'] = self.parse_img(item['C2CMidPrice_sell_img'],
                                                      item['status'] + "-" + "C2CMidPrice_sell_img")
            item['C2CLowPrice_sell_img'] = response.urljoin(response.xpath("//*[@class='w_carpricinfobox clearfix']/div[2]/ul/li[1]/span[3]/img/@src").extract_first().replace("2_2", "2_1"))
            item['C2CLowPrice_sell_img'] = self.parse_img(item['C2CLowPrice_sell_img'],
                                                      item['status'] + "-" + "C2CLowPrice_sell_img")
            item['C2CUpPrice_sell_img'] = response.urljoin(response.xpath("//*[@class='w_carpricinfobox clearfix']/div[2]/ul/li[3]/span[3]/img/@src").extract_first().replace("2_2", "2_1"))
            item['C2CUpPrice_sell_img'] = self.parse_img(item['C2CUpPrice_sell_img'],
                                                      item['status'] + "-" + "C2CUpPrice_sell_img")
        else:
            item['B2CMidPrice_buy_img'] = response.urljoin(response.xpath(
                "//*[@class='w_carpricinfobox clearfix']/div[1]/ul/li[2]/span[3]/img/@src").extract_first().replace("1_1", "2_1"))
            item['B2CMidPrice_buy_img'] = self.parse_img(item['B2CMidPrice_buy_img'],
                                                         item['status'] + "-" + "B2CMidPrice_buy_img")
            item['B2CLowPrice_buy_img'] = response.urljoin(response.xpath(
                "//*[@class='w_carpricinfobox clearfix']/div[1]/ul/li[1]/span[3]/img/@src").extract_first().replace("2_2", "2_1"))
            item['B2CLowPrice_buy_img'] = self.parse_img(item['B2CLowPrice_buy_img'],
                                                         item['status'] + "-" + "B2CLowPrice_buy_img")
            item['B2CUpPrice_buy_img'] = response.urljoin(response.xpath(
                "//*[@class='w_carpricinfobox clearfix']/div[1]/ul/li[3]/span[3]/img/@src").extract_first().replace("2_2", "2_1"))
            item['B2CUpPrice_buy_img'] = self.parse_img(item['B2CUpPrice_buy_img'],
                                                         item['status'] + "-" + "B2CUpPrice_buy_img")
            item['C2CMidPrice_buy_img'] = response.urljoin(response.xpath(
                "//*[@class='w_carpricinfobox clearfix']/div[2]/ul/li[2]/span[3]/img/@src").extract_first().replace("2_2", "2_1"))
            item['C2CMidPrice_buy_img'] = self.parse_img(item['C2CMidPrice_buy_img'],
                                                         item['status'] + "-" + "C2CMidPrice_buy_img")
            item['C2CLowPrice_buy_img'] = response.urljoin(response.xpath(
                "//*[@class='w_carpricinfobox clearfix']/div[2]/ul/li[1]/span[3]/img/@src").extract_first().replace("2_2", "2_1"))
            item['C2CLowPrice_buy_img'] = self.parse_img(item['C2CLowPrice_buy_img'],
                                                         item['status'] + "-" + "C2CLowPrice_buy_img")
            item['C2CUpPrice_buy_img'] = response.urljoin(response.xpath(
                "//*[@class='w_carpricinfobox clearfix']/div[2]/ul/li[3]/span[3]/img/@src").extract_first().replace("2_2", "2_1"))
            item['C2CUpPrice_buy_img'] = self.parse_img(item['C2CUpPrice_buy_img'],
                                                         item['status'] + "-" + "C2CUpPrice_buy_img")

        # print(item)
        yield item

