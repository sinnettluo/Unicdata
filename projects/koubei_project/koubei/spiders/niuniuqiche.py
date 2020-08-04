# # -*- coding: utf-8 -*-
# import scrapy
# from scrapy.http import Request
# import re
# import jpype
# from jpype import *
# from scrapy.conf import settings
# import json
# import time
# from koubei.items import NiuNiuQiCheItem
#
# website = "niuniuqiche"
#
# class EastdaySpiderSpider(scrapy.Spider):
#
#     # s = '\xe9\x9d\x9e\xe6\xb3\x95\xe7\x9a\x84token'
#     # ss = s.encode('raw_unicode_escape')
#     # sss = ss.decode()
#     # print(sss)
#     token = "5e97dd6ffadc69b498aec331ed70361a146f109a"
#     # token = "8af4db6be5224d8bcb6684b847edf64f4981a047"
#     # token = "327925c1afd24dd45404f076f7287fe7043f15ea"
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
#         # params1 = '{"token":"f19f8512c6723ae60683cbf4fac91462113104be","id":"33592876"}'
#         # payload = self.getPayLoad(self.key, params1, self.ext_classpath, self.ext_classpath1)
#         # url = "https://www.niuniuqiche.com/api/v24/posts/resource_detail?payload=%s" % payload
#         # yield scrapy.Request(url=url)
#
#         params1 = '{"token":"%s","from":"resourse"}' % self.token
#         payload = self.getPayLoad(self.key, params1, self.ext_classpath, self.ext_classpath1)
#         url = "https://www.niuniuqiche.com/api/v24/brands/brand_list?payload=%s" % payload
#         yield scrapy.Request(url=url)
#
#     def parse(self, response):
#         print(response.text)
#         # return
#         brands = json.loads(response.text)
#         for brand in brands["data"]:
#             brandname = brand["name"]
#             brandid = brand["id"]
#             params2 = '{"token":"%s","brand_name":"%s"}' % (self.token, brandname)
#             payload = self.getPayLoad(self.key, params2, self.ext_classpath, self.ext_classpath1)
#             url = "https://www.niuniuqiche.com/api/v24/posts/search_brand_filter?payload=%s" % payload
#             meta = {
#                 "brandname": brandname,
#                 "brandid": brandid,
#             }
#             yield scrapy.Request(url=url, meta=meta, callback=self.parse_family)
#
#
#     def parse_family(self, response):
#         factories = json.loads(response.text)
#         for factory in factories["data"]:
#             factoryname = factory["manufacturer"]
#             for family in factory["car_model_names"]:
#                 familyname = family["name"]
#                 total_page = int(int(family["count"])/20) if int(family["count"])%20 == 0 else int(int(family["count"])/20) + 1
#                 for i in range(1, total_page+1):
#                     params3 = '{"car_model_name":"%s","no_spellcheck":"false","page":"%d","token":"%s","brand_name":"%s","firm_name":"%s"}' % (familyname, i, self.token, response.meta["brandname"], factoryname)
#                     payload = self.getPayLoad(self.key, params3, self.ext_classpath, self.ext_classpath1)
#                     url = "https://www.niuniuqiche.com/api/v24/posts/search_resources?payload=%s" % payload
#                     meta = {
#                         "factoryname": factoryname,
#                         "familyname": familyname,
#                         "brandname": response.meta["brandname"],
#                         "brandid": response.meta["brandid"]
#                     }
#                     yield scrapy.Request(url=url, meta=dict(meta, **response.meta), callback=self.parse_list)
#
#
#     def parse_list(self, response):
#         print(response.body)
#         posts = json.loads(response.text)
#         for post in posts["data"]["posts"]:
#             item = NiuNiuQiCheItem()
#             item['url'] = response.url
#             item['status'] = post["id"]
#             item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
#             item['id'] = post["id"]
#             item['user_id'] = post["user_id"]
#             item['user_name'] = post["user_name"]
#             item['title'] = post["title"]
#             item['subtitle'] = post["subtitle"]
#             item['show_price'] = post["show_price"]
#             item['info_price'] = post["info_price"]
#             item['inner_color'] = post["inner_color"]
#             item['outer_color'] = post["outer_color"]
#             item['human_remark'] = post["human_remark"]
#             item['user_level'] = post["user_level"]
#             item['vip_level'] = post["vip_level"]
#             item['is_vip_resource'] = post["is_vip_resource"]
#             item['updated_at'] = post["updated_at"]
#             item['is_deposit'] = post["is_deposit"]
#             item['is_member_price'] = post["is_member_price"]
#             item['user_deal_amount_display'] = post["user_deal_amount_display"]
#             item['extend_info'] = post["extend_info"]
#             item['scheme_url'] = post["scheme_url"]
#             item['post_margin_amount'] = post["post_margin_amount"]
#             item['has_photo'] = post["has_photo"]
#             item['res_promotion_type'] = post["res_promotion_type"]
#             item['is_self_run'] = post["is_self_run"]
#             item["brandid"] = response.meta["brandid"]
#             item["brandname"] = response.meta["brandname"]
#             item["familyname"] = response.meta["familyname"]
#             item["factoryname"] = response.meta["factoryname"]
#
#             yield item
#
#
#
