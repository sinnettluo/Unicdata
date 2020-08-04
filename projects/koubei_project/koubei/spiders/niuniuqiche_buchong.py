# # -*- coding: utf-8 -*-
# import scrapy
# from scrapy.http import Request
# import re
# import jpype
# from jpype import *
# from scrapy.conf import settings
# import json
# import time
# from koubei.items import NiuNiuBuChongItem
# import pymysql
#
# website = "niuniuqiche_buchong"
#
# class EastdaySpiderSpider(scrapy.Spider):
#
#     # s = '\xe9\x9d\x9e\xe6\xb3\x95\xe7\x9a\x84token'
#     # ss = s.encode('raw_unicode_escape')
#     # sss = ss.decode()
#     # print(sss)
#     token = "562e24c7508fddfd5636e31a805e71f9f516fbd6"
#     # token = "f215dd8007f29ffb7bdcc21ae2c1d3431ed452be"
#     # token = "8af4db6be5224d8bcb6684b847edf64f4981a047"
#     # token = "f19f8512c6723ae60683cbf4fac91462113104be"
#     name = website
#     key = "Ve1BakMFZPKBejt6gdA2-"
#     ext_classpath = r'D:/jar/jose4j-0.6.3.jar'
#     ext_classpath1 = r'D:/jar/slf4j-api-1.7.25.jar'
#
#     def __init__(self, **kwargs):
#         super(EastdaySpiderSpider, self).__init__(**kwargs)
#
#         self.carnum = 1000000
#         settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
#         settings.set('MONGODB_DB', 'koubei', priority='cmdline')
#         settings.set('MONGODB_COLLECTION', website, priority='cmdline')
#
#     def getPayLoad(self, key, params, ext_classpath, ext_classpath1):
#         jvmPath = jpype.getDefaultJVMPath()
#         jvmArg = '-Djava.class.path=%s;%s' % (ext_classpath, ext_classpath1)
#         if not jpype.isJVMStarted():
#             jpype.startJVM(jvmPath,'-ea',jvmArg)
#
#         DateClass = jpype.java.util.Date
#         DateFormatClass = jpype.java.text.SimpleDateFormat
#         DateInstance = DateClass()
#         # print(DateFormatClass("yyyy-MM-dd").format(DateInstance))
#         key = key + DateFormatClass("yyyy-MM-dd").format(DateInstance)
#
#         HmacKeyClass = JClass("org.jose4j.keys.HmacKey")
#         HmacKeyInstance = HmacKeyClass(bytearray(key.encode("utf-8")))
#
#         JWSClass = JClass("org.jose4j.jws.JsonWebSignature")
#         JWSInstance = JWSClass()
#         JWSInstance.setPayload(params)
#         JWSInstance.setAlgorithmHeaderValue("HS512")
#         JWSInstance.setKey(HmacKeyInstance)
#         JWSInstance.setDoKeyValidation(False)
#         payload = JWSInstance.getCompactSerialization()
#         return payload
#         # return
#
#     # def spider_close(self):
#     #     jpype.shutdownJVM()
#
#     def start_requests(self):
#
#         # 连接数据库
#         db = pymysql.connect("192.168.1.94", "root", "Datauser@2017", "koubei")
#
#         # 使用cursor()方法创建一个游标对象
#         cursor = db.cursor()
#
#         # 使用execute()方法执行SQL语句
#         cursor.execute("SELECT distinct(id) FROM niuniuqiche")
#
#         # 使用fetall()获取全部数据
#         ids = cursor.fetchall()
#
#         # for item in data:
#         #     print(item)
#         for id in ids:
#             params1 = '{"token":"%s","id":"%s"}' % (self.token, str(id[0]))
#             payload = self.getPayLoad(self.key, params1, self.ext_classpath, self.ext_classpath1)
#             url = "https://www.niuniuqiche.com/api/v24/posts/resource_detail?payload=%s" % payload
#             yield scrapy.Request(url=url)
#
#         # params1 = '{"token":"f19f8512c6723ae60683cbf4fac91462113104be","from":"resourse"}'
#         # payload = self.getPayLoad(self.key, params1, self.ext_classpath, self.ext_classpath1)
#         # url = "https://www.niuniuqiche.com/api/v24/brands/brand_list?payload=%s" % payload
#         # yield scrapy.Request(url=url)
#
#     def parse(self, response):
#         print(response.text)
#         details = json.loads(response.text)
#         show_price = details["data"]["post"]["show_price"] if "show_price" in details["data"]["post"] else "-"
#         take_car_area = details["data"]["post"]["take_car_area"] if "take_car_area" in details["data"]["post"] else "-"
#         car_in_area = details["data"]["post"]["car_in_area"] if "car_in_area" in details["data"]["post"] else "-"
#         meta = {
#             "show_price": show_price,
#             "take_car_area": take_car_area,
#             "car_in_area": car_in_area,
#             "post_id": str(details["data"]["post"]["id"])
#         }
#
#         params1 = '{"token":"%s","id":"%s"}' % (self.token, str(details["data"]["post"]["id"]))
#         payload = self.getPayLoad(self.key, params1, self.ext_classpath, self.ext_classpath1)
#         url = "https://www.niuniuqiche.com/api/v24/posts/car_parameter?payload=%s" % payload
#         yield scrapy.Request(url=url, meta=meta, callback=self.parse_car_parameter)
#
#     def parse_car_parameter(self, response):
#         parameters = json.loads(response.text)
#         item = NiuNiuBuChongItem()
#         item['url'] = response.url
#         item['status'] = response.meta["post_id"]
#         item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
#         item['post_id'] = response.meta["post_id"]
#         item['car_in_area'] = response.meta["car_in_area"]
#         item['take_car_area'] = response.meta["take_car_area"]
#         item['show_price'] = response.meta["show_price"]
#         for cs in parameters["data"]["items"]:
#             if cs["group_name"] == "基本参数":
#                 for value in cs["values"]:
#                     if value["name"] == "发动机":
#                         item["fadongji"] = value["val"]
#                     if value["name"] == "变速箱":
#                         item["biansuxiang"] = value["val"]
#                     if value["name"] == "长*宽*高(mm)":
#                         item["lwh"] = value["val"]
#                     if value["name"] == "车身结构":
#                         item["cheshenjiegou"] = value["val"]
#                     if value["name"] == "发动机":
#                         item["fadongji"] = value["val"]
#             if cs["group_name"] == "车身":
#                 for value in cs["values"]:
#                     if value["name"] == "车门数(个)":
#                         item["chemenshu"] = value["val"]
#                     if value["name"] == "座位数(个)":
#                         item["zuoweishu"] = value["val"]
#             if cs["group_name"] == "发动机":
#                 for value in cs["values"]:
#                     if value["name"] == "排量(L)":
#                         item["pailiang"] = value["val"]
#                     if value["name"] == "进气形式":
#                         item["jinqifangshi"] = value["val"]
#             if cs["group_name"] == "电动机":
#                 for value in cs["values"]:
#                     if value["name"] == "能源类型":
#                         item["nengyuanleixing"] = value["val"]
#             if cs["group_name"] == "变速箱":
#                 for value in cs["values"]:
#                     if value["name"] == "简称":
#                         item["biansuxiang_jiancheng"] = value["val"]
#             if cs["group_name"] == "底盘转向":
#                 for value in cs["values"]:
#                     if value["name"] == "驱动方式":
#                         item["qudongfangshi"] = value["val"]
#         print(item)
#         yield item
#
