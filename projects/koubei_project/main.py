from scrapy.cmdline import execute

import sys
import os


website = "tuhu_gongchangdian_2019_fix3"
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", website])


# # -*- coding: utf-8 -*-
# import scrapy
# from scrapy.http import Request
# import re
# import jpype
# import requests
# from jpype import *
# from scrapy.conf import settings
# import json
# import time
# from koubei.items import NiuNiuQiCheItem
#
#
# def getPayLoad(key, params, ext_classpath, ext_classpath1):
#     jvmPath = jpype.getDefaultJVMPath()
#     jvmArg = '-Djava.class.path=%s;%s' % (ext_classpath, ext_classpath1)
#     if not jpype.isJVMStarted():
#         jpype.startJVM(jvmPath, '-ea', jvmArg)
#
#     DateClass = jpype.java.util.Date
#     DateFormatClass = jpype.java.text.SimpleDateFormat
#     DateInstance = DateClass()
#     # print(DateFormatClass("yyyy-MM-dd").format(DateInstance))
#     key = key + DateFormatClass("yyyy-MM-dd").format(DateInstance)
#
#     HmacKeyClass = JClass("org.jose4j.keys.HmacKey")
#     HmacKeyInstance = HmacKeyClass(bytearray(key.encode("utf-8")))
#
#     JWSClass = JClass("org.jose4j.jws.JsonWebSignature")
#     JWSInstance = JWSClass()
#     JWSInstance.setPayload(params)
#     JWSInstance.setAlgorithmHeaderValue("HS512")
#     JWSInstance.setKey(HmacKeyInstance)
#     JWSInstance.setDoKeyValidation(False)
#     payload = JWSInstance.getCompactSerialization()
#     return payload
#     # return
# key = "Ve1BakMFZPKBejt6gdA2-"
# ext_classpath = r'D:/jar/jose4j-0.6.3.jar'
# ext_classpath1 = r'D:/jar/slf4j-api-1.7.25.jar'
# params2 = '{"token":"f19f8512c6723ae60683cbf4fac91462113104be","id":"33592876"}'
# payload = getPayLoad(key=key, params=params2, ext_classpath=ext_classpath, ext_classpath1=ext_classpath1)
# url = "https://www.niuniuqiche.com/api/v24/posts/search_brand_filter?payload=%s" % payload
# print(requests.request(url=url, method="get").text)