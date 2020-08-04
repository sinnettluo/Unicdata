# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import re
# import jpype
# from jpype import *
from scrapy.utils.project import get_project_settings
settings = get_project_settings()
import json
import time
from koubei.items import NiuNiuQiCheItem
import json

website = "zhejiang_echong"

class EastdaySpiderSpider(scrapy.Spider):

    # s = '\xe9\x9d\x9e\xe6\xb3\x95\xe7\x9a\x84token'
    # ss = s.encode('raw_unicode_escape')
    # sss = ss.decode()
    # print(sss)


    name = website
    start_urls = ["https://zjec.evshine.cn/ast/api/v0.1/charging-stations?city=&county=&stationName=&operId=&positionLon=121.504475&positionLat=31.286683&orderType=&freeFlag=0&elecMode=&gunType=&autoModel="]
    key = "Ve1BakMFZPKBejt6gdA2-"
    ext_classpath = r'D:/jar/jose4j-0.6.3.jar'
    ext_classpath1 = r'D:/jar/slf4j-api-1.7.25.jar'

    def __init__(self, **kwargs):
        super(EastdaySpiderSpider, self).__init__(**kwargs)

        self.carnum = 1000000
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'koubei', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    def getPayLoad(self, key, params, ext_classpath, ext_classpath1):
        # jvmPath = jpype.getDefaultJVMPath()
        # jvmArg = '-Djava.class.path=%s;%s' % (ext_classpath, ext_classpath1)
        # if not jpype.isJVMStarted():
        #     jpype.startJVM(jvmPath,'-ea',jvmArg)
        #
        # DateClass = jpype.java.util.Date
        # DateFormatClass = jpype.java.text.SimpleDateFormat
        # DateInstance = DateClass()
        # # print(DateFormatClass("yyyy-MM-dd").format(DateInstance))
        # key = key + DateFormatClass("yyyy-MM-dd").format(DateInstance)
        #
        # HmacKeyClass = JClass("org.jose4j.keys.HmacKey")
        # HmacKeyInstance = HmacKeyClass(bytearray(key.encode("utf-8")))
        #
        # JWSClass = JClass("org.jose4j.jws.JsonWebSignature")
        # JWSInstance = JWSClass()
        # JWSInstance.setPayload(params)
        # JWSInstance.setAlgorithmHeaderValue("HS512")
        # JWSInstance.setKey(HmacKeyInstance)
        # JWSInstance.setDoKeyValidation(False)
        # payload = JWSInstance.getCompactSerialization()
        # return payload
        return

    # def spider_close(self):
    #     jpype.shutdownJVM()

    # def start_requests(self):
    #     pass

    def parse(self, response):
        # print(response.body)
        json_obj = json.loads(response.text)

        count = 0
        print(len(json_obj["chcGroupList"]))
        for group in json_obj["chcGroupList"]:
            for list in group["chcList"]:
                count += len(list)

        print(count)