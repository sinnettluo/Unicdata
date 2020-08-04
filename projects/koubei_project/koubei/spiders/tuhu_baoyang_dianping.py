# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from koubei.items import TuhuBaoyangDianPingItem
# from scrapy.conf import settings
import logging
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import urllib.parse

website ='tuhu_baoyang_dianping3'

class KoubeiSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['www.bitauto.com']
    start_urls = ['https://item.tuhu.cn/Car/GetCarBrands2?callback=__GetCarBrands__']

    def __init__(self, **kwargs):
        super(KoubeiSpider, self).__init__(**kwargs)
        self.carnum = 1000000
        self.settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        self.settings.set('MONGODB_DB', 'koubei', priority='cmdline')
        self.settings.set('MONGODB_COLLECTION', website, priority='cmdline')

        # self.browser = webdriver.PhantomJS(executable_path=settings['PHANTOMJS_PATH'])

        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        #     'Cookie': 'JSESSIONID=010BF80058C18D15F9C4B03B20406117',
        #     'Referer': 'http://xzqh.mca.gov.cn/defaultQuery?shengji=%B1%B1%BE%A9%CA%D0%28%BE%A9%29&diji=%B1%B1%BE%A9%CA%D0&xianji=-1',
        #     'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # }
        # for key in headers:
        #     webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = headers[key]
    #     self.browser = webdriver.PhantomJS(executable_path="D:/phantomjs.exe")
    #     super(KoubeiSpider, self).__init__()
    #     dispatcher.connect(self.spider_closed, signals.spider_closed)
    #
    # def spider_closed(self):
    #     self.browser.quit()

    # def start_requests(self):
    #     for i in range(1, 20):
    #         yield scrapy.Request(url="https://api.touchev.com:83/api/0190/index/index.do?jpushId=1507bfd3f79851701fd&deviceId=869622035270223&userId=&sss=b235a2d3468dd22be9a071cbf1016978&idx=0&first=no&appName=%E7%AC%AC%E4%B8%80%E7%94%B5%E5%8A%A8&lng=121.510961&network=wifi&naviId=12&networkOperator=CMCC&imei=869622035270223&deviceOsVer=7.0&deviceOs=android&appVer=1.9.2&tpToken=&page=" + str(i) + "&lat=31.292386&channel=yingyongbao&appToken=&limit=20&deviceSysVar=RNE-AL00%7CHUAWEI")

    def parse(self, response):
        res = json.loads(response.text.replace("__GetCarBrands__(", "").replace(")", ""))
        for i in range(65,91):
            try:
                brandList = res[chr(i)]
            except Exception as e:
                print(e)
                continue
            for brand in brandList:
                brandStr = brand["Brand"].replace(" ", "+")
                url = "https://item.tuhu.cn/Car/SelOneBrand?callback=__GetCarBrands__&Brand=%s" % brandStr
                meta = {"brand":brandStr}
                yield scrapy.Request(url=url, meta=meta, callback=self.parse_family)


    def parse_family(self, response):
        res = json.loads(response.text.replace("__GetCarBrands__(", "").replace(")", ""))
        for family in res["OneBrand"]:
            url = "https://item.tuhu.cn/Car/SelectVehicle?callback=__GetCarBrands__&VehicleID=%s" % family["ProductID"]
            meta = dict({"familyID":family["ProductID"], "familyName":family["CarName"]}, **response.meta)
            yield scrapy.Request(url=url, meta=meta, callback=self.parse_pailiang)

    def parse_pailiang(self, response):
        res = json.loads(response.text.replace("__GetCarBrands__(", "").replace(")", ""))
        for pailiang in res["PaiLiang"]:
            url = "https://item.tuhu.cn/Car/SelectVehicle?callback=__GetCarBrands__&VehicleID=%s&PaiLiang=%s" % (pailiang["Key"], pailiang["Value"])
            meta = dict({"pailiang":pailiang["Value"]}, **response.meta)
            yield scrapy.Request(url=url, meta=meta, callback=self.parse_year)

    def parse_year(self, response):
        res = json.loads(response.text.replace("__GetCarBrands__(", "").replace(")", ""))
        for year in res["Nian"]:
            url = "/SPages/GetPropertyByVehicleForBattery.aspx?vehicleId=%s&paiLiang=%s&nian=%s" % (year["Key"], response.meta["pailiang"], year["Value"])
            meta = dict({"nian": year["Value"]}, **response.meta)
            yield scrapy.Request(url="https://www.tuhu.cn" + url, meta=meta, headers={"referer": "https://www.tuhu.cn", "cookie": "_um_deti=f932950d26514e1ab709e663d8552daf7"}, callback=self.parse_model)

    def parse_model(self, response):

        province = {
            "上海市":1,
            "北京市":2,
            "天津市":19,
            "重庆市": 20,
            "四川省": 23,
            "贵州省": 24,
            "云南省": 25,
            "西藏自治区": 26,
            "陕西省": 27,
            "甘肃省": 28,
            "青海省": 29,
            "宁夏回族自治区": 30,
            "新疆维吾尔自治区": 31,
            "浙江省": 90,
            "山东省": 334,
            "安徽省": 407,
            "河北省": 712,
            "江苏省": 723,
            "吉林省": 724,
            "广东省": 831,
            "内蒙古自治区": 832,
            "广西壮族自治区": 978,
            "海南省": 979,
            "河南省": 1060,
            "湖南省": 1182,
            "福建省": 1404,
            "湖北省": 1561,
            "江西省": 1676,
            "辽宁省": 1847,
            "山西省": 1848,
            "黑龙江省":2344,
        }

        res = json.loads(response.text)

        meta = dict()

        if res["data"] is not None:
            for model in res["data"]["Values"]:
                modelname = model["DisplayValue"]
                modelid = model["Key"]
                for p in province:
                    provinceName = p
                    meta = {
                        "provinceName":provinceName,
                        "provinceid":province[p],
                        "modelname":modelname,
                        "modelid":modelid,
                    }
                    meta = dict(meta, **response.meta)
                    yield scrapy.Request(url=response.urljoin("/Region/GetRegions.aspx?regionId=%d&type=city" % province[p]), meta=meta, dont_filter=True, callback=self.parse_city)
        else:
            for p in province:
                provinceName = p
                meta = {
                    "provinceName": provinceName,
                    "provinceid": province[p],
                }
                meta = dict(meta, **response.meta)
                yield scrapy.Request(url=response.urljoin("/Region/GetRegions.aspx?regionId=%d&type=city" % province[p]),
                                     meta=meta, dont_filter=True, callback=self.parse_city)

    def parse_city(self, response):
        print(response.text)
        res = json.loads(response.text)
        if "RegionId" in res:
            cityname = res["RegionName"]
            cityid = res["RegionId"]
            meta = {
                "cityname":cityname,
                "cityid":cityid,
                "citymark":1
            }
            meta = dict(meta, **response.meta)
            url = "/Region/GetRegions.aspx?regionId=%s&type=district" % str(res["RegionId"])
            yield scrapy.Request(url=response.urljoin(url), meta=meta, dont_filter=True, callback=self.parse_district)
        else:
            for city in res:
                cityname = city["RegionName"]
                cityid = city["RegionId"]
                meta = {
                    "cityname": cityname,
                    "cityid": cityid,
                    "citymark":2
                }
                meta = dict(meta, **response.meta)
                url = "/Region/GetRegions.aspx?regionId=%s&type=district" % str(city["RegionId"])
                yield scrapy.Request(url=response.urljoin(url), meta=meta, dont_filter=True, callback=self.parse_district)

    def parse_district(self, response):
        print(response.meta)
        res = json.loads(response.text)
        for district in res:
            districtname = district["RegionName"]
            districtid = district["RegionId"]
            meta = {
                "districtname":districtname,
                "districtid":districtid
            }
            meta = dict(meta, **response.meta)
            if "modelid" in response.meta:
                url = "/SPages/GetBatteryProducts.aspx?vehicleId=%s&paiLiang=%s&nian=%s&tid=%s&regionId=%s" % (response.meta["familyID"], response.meta["pailiang"], response.meta["nian"], response.meta["modelid"], districtid)
                yield scrapy.Request(url=response.urljoin(url), headers={"referer": "https://www.tuhu.cn/"}, meta=meta, callback=self.parse_product)
            else:
                url = "/SPages/GetBatteryProducts.aspx?vehicleId=%s&paiLiang=%s&nian=%s&regionId=%s" % (
                response.meta["familyID"], response.meta["pailiang"], response.meta["nian"], districtid)
                yield scrapy.Request(url=response.urljoin(url), headers={"referer": "https://www.tuhu.cn/"}, meta=meta, callback=self.parse_product)

    def parse_product(self, response):
        # print(response.text)
        res = json.loads(response.text)
        for product in res:
            item = TuhuBaoyangDianPingItem()
            item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
            item["url"] = response.url
            item['brand'] = response.meta["brand"]
            item['familyID'] = response.meta["familyID"]
            item['familyName'] = response.meta["familyName"]
            item['pailiang'] = response.meta["pailiang"]
            item['nian'] = response.meta["nian"]
            item['provinceName'] = response.meta["provinceName"]
            item['provinceid'] = response.meta["provinceid"]
            item['modelname'] = response.meta["modelname"] if "modelname" in response.meta else "-"
            item['modelid'] = response.meta["modelid"] if "modelid" in response.meta else "-"
            item['cityname'] = response.meta["cityname"]
            item['cityid'] = response.meta["cityid"]
            item['districtname'] = response.meta["districtname"]
            item['districtid'] = response.meta["districtid"]
            item['oid'] = product["Oid"]
            item['ProductId'] = product["ProductId"]
            item['DisplayName'] = product["DisplayName"]
            item['price'] = product["Price"]
            item['shuxing1'] = product["ShuXing1"]
            item['shuxing2'] = product["ShuXing2"]
            item['shuxing3'] = product["ShuXing3"]
            item['shuxing4'] = product["ShuXing4"]
            item['shuxing5'] = product["ShuXing5"]
            item['PartNo'] = product["PartNo"]
            item['p_brand'] = product["Brand"]

            item['status'] = str(response.meta["brand"]) + str(response.meta["familyID"]) + str(response.meta["pailiang"]) + str(response.meta["nian"]) + str(item['modelid']) + str(response.meta["provinceid"]) + str(response.meta["cityid"]) + str(response.meta["districtid"]) + str(product["Oid"]) + str(product["ProductId"])

            # print(item)
            yield item