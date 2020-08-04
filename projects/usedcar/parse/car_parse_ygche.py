#-*- coding: UTF-8 -*-
import json
import math
import re
import sys
import time

import pandas
import pp
import scrapy
# sys
reload(sys)
sys.setdefaultencoding('utf8')
#load funcs
from Parse_Init import *
from SaveData import *
from PP_Init import *

# basesetting
def Init():
    #params
    website ='ygche'
    params =ParseInit(website)
    #mysql redefine
    params['createsql']="""CREATE TABLE IF NOT EXISTS `ygche` (
                                `id` bigint(20) NOT NULL auto_increment,
                                `website` varchar(63) DEFAULT NULL,
                                `carid` varchar(63) DEFAULT NULL,
                                `title` varchar(127) DEFAULT NULL,
                                `pagetitle` varchar(127) DEFAULT NULL,
                                `url` varchar(127) DEFAULT NULL,
                                `grabtime` varchar(63) DEFAULT NULL,
                                `pagetime` varchar(63) DEFAULT NULL,
                                `parsetime` varchar(63) DEFAULT NULL, 
                                `price1` varchar(63) DEFAULT NULL,
                                `pricetag` varchar(63) DEFAULT NULL,
                                `status` varchar(63) DEFAULT NULL,
                                `statusplus` varchar(127) DEFAULT NULL,
                                `registerdate` varchar(63) DEFAULT NULL,
                                `posttime` varchar(63) DEFAULT NULL,
                                `years` varchar(63) DEFAULT NULL,
                                `mileage` varchar(63) DEFAULT NULL,
                                `color` varchar(63) DEFAULT NULL,
                                `makeyear` varchar(63) DEFAULT NULL,
                                `province` varchar(63) DEFAULT NULL,
                                `city` varchar(63) DEFAULT NULL,
                                `region` varchar(63) DEFAULT NULL,
                                `dealplace` varchar(255) DEFAULT NULL,
                                `ratelevel` varchar(63) DEFAULT NULL,
                                `ratecont` varchar(2000) DEFAULT NULL,
                                `changetimes` varchar(63) DEFAULT NULL,
                                `changedate` varchar(63) DEFAULT NULL,
                                `Insurance1` varchar(63) DEFAULT NULL,
                                `Insurance2` varchar(63) DEFAULT NULL,
                                `yearchecktime` varchar(63) DEFAULT NULL,
                                `carokcf` varchar(63) DEFAULT NULL,
                                `carcard` varchar(63) DEFAULT NULL,
                                `carinvoice` varchar(63) DEFAULT NULL,
                                `accident` varchar(63) DEFAULT NULL,
                                `useage` varchar(63) DEFAULT NULL,
                                `telphone` varchar(63) DEFAULT NULL,
                                `dealor` varchar(127) DEFAULT NULL,
                                `level` varchar(127) DEFAULT NULL,
                                `motor` varchar(127) DEFAULT NULL,
                                `lengthwh` varchar(127) DEFAULT NULL,
                                `weight` varchar(127) DEFAULT NULL,
                                `luggage` varchar(127) DEFAULT NULL,
                                `brand_name` varchar(63) DEFAULT NULL,
                                `class_name` varchar(63) DEFAULT NULL,
                                `guideprice` varchar(63) DEFAULT NULL,
                                `guidepricetax` varchar(63) DEFAULT NULL,
                                `newcartitle` varchar(127) DEFAULT NULL,
                                `newcarurl` varchar(127) DEFAULT NULL,
                                `geartype` varchar(63) DEFAULT NULL,
                                `emission` varchar(63) DEFAULT NULL,
                                `gear` varchar(63) DEFAULT NULL,
                                `body` varchar(63) DEFAULT NULL,
                                 `output` varchar(63) DEFAULT NULL,
                                 `desc` varchar(511) DEFAULT NULL,
                                 `img_url` varchar(255) DEFAULT NULL,
                                 `carinfo1` varchar(127) DEFAULT NULL,
                                 `carinfo2` varchar(127) DEFAULT NULL,
                                 `carinfo3` varchar(127) DEFAULT NULL,
                                 `carinfo4` varchar(127) DEFAULT NULL,
                                 `carinfo5` varchar(127) DEFAULT NULL,
                                 `carinfo6` varchar(127) DEFAULT NULL,
                                 `carinfo7` varchar(127) DEFAULT NULL,
                                 `carinfo8` varchar(127) DEFAULT NULL,
                                 `carinfo9` varchar(127) DEFAULT NULL,
                                 `carinfo10` varchar(127) DEFAULT NULL,
                                 `carinfo11` varchar(127) DEFAULT NULL,
                                 `carinfo12` varchar(127) DEFAULT NULL,
                                 `carinfo13` varchar(127) DEFAULT NULL,
                                 `carinfo14` varchar(127) DEFAULT NULL,
                                 `carinfo15` varchar(127) DEFAULT NULL,
                                 `carinfo16` varchar(127) DEFAULT NULL,
                                 `carinfo17` varchar(127) DEFAULT NULL,
                                 `carinfo18` varchar(127) DEFAULT NULL,
                                 `carinfo19` varchar(127) DEFAULT NULL,
                                 `carinfo20` varchar(127) DEFAULT NULL,
                                 `carinfo21` varchar(127) DEFAULT NULL,
                                 `carinfo22` varchar(127) DEFAULT NULL,
                                 `carinfo23` varchar(127) DEFAULT NULL,
                                 `carinfo24` varchar(127) DEFAULT NULL,
                                 `carinfo25` varchar(127) DEFAULT NULL,
                                 `carinfo26` varchar(127) DEFAULT NULL,
                                 `carinfo27` varchar(127) DEFAULT NULL,
                                 `carinfo28` varchar(127) DEFAULT NULL,
                                 `carinfo29` varchar(127) DEFAULT NULL,
                                 `carinfo30` varchar(127) DEFAULT NULL,
                                 `carinfo31` varchar(127) DEFAULT NULL,
                                 `carinfo32` varchar(127) DEFAULT NULL,
                                 `carinfo33` varchar(127) DEFAULT NULL,
                                 `carinfo34` varchar(127) DEFAULT NULL,
                                 `carinfo35` varchar(127) DEFAULT NULL,
                                 `carinfo36` varchar(127) DEFAULT NULL,
                                 `carinfo37` varchar(127) DEFAULT NULL,
                                 `carinfo38` varchar(127) DEFAULT NULL,
                                 `carinfo39` varchar(127) DEFAULT NULL,
                                 `carinfo40` varchar(127) DEFAULT NULL,
                                 `carinfo41` varchar(127) DEFAULT NULL,
                                 `carinfo42` varchar(127) DEFAULT NULL,
                                 `carinfo43` varchar(127) DEFAULT NULL,
                                 `carinfo44` varchar(127) DEFAULT NULL,
                                 `carinfo45` varchar(127) DEFAULT NULL,
                                 `carinfo46` varchar(127) DEFAULT NULL,
                                 `carinfo47` varchar(127) DEFAULT NULL,
                                 `carinfo48` varchar(127) DEFAULT NULL,
                                 `carinfo49` varchar(127) DEFAULT NULL,
                                 PRIMARY KEY  (`id`)
                              ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
    params['mysqltable']='ygche'
    # params['mysqltable']=params['website']
    # params['mysqlip']="192.168.1.92"
    # params['mysqluser']="root"
    # params['mysqlpasswd']="Datauser@2016"
    # params['mysqldbname']="usedcar"
    # params['mysqlport']=3306

    # mongo redefine
    # params['mongocoll']=params['website']
    # params['mongoip']="192.168.1.92"
    # params['mongoport']=27071
    # params['mongodbname']="usedcar"

    # df redefine
    # params['bfrate']=0.001
    # params['keycol']="statusplus"

    # carinfocreate redefine
    # params['carinfocreate'] = False
    # counts redefine
    # params['counts']=0
    # size redefine
    # params['savesize']=1000
    return params

def parse_original(item):
    # caritem init
    caritem = dict()
    # keyinfro
    caritem['website'] = item['website']
    caritem['carid'] = str(re.findall('\d+', item["url"])[0])
    caritem['url'] = item["url"]
    caritem['grabtime'] = item["grabtime"]
    caritem['pagetime'] = item["pagetime"]  # new
    caritem['parsetime'] = time.strftime('%Y-%m-%d %X', time.localtime())
    # status
    caritem['status'] = str(re.findall('sale|sold', item["status"])[0])  # �?
    caritem['statusplus'] = item["status"]
    return caritem


def parse_keyinfo(dom):
    # caritem init
    caritem = dict()
    # keyinfro
    caritem['pagetitle'] = dom.xpath('//title/text()').extract_first() if dom.xpath('//title/text()') else "-"  # new
    caritem['title'] = dom.xpath('//h1[@class="mb15"]/span/text()').extract_first().strip() \
        if dom.xpath('//h1[@class="mb15"]/span/text()') else "-"
    caritem['makeyear']=re.compile(u'\u6b3e').sub('',dom.xpath('//h1[@class="mb15"]/span/text()').extract_first().strip().split(' ')[0]) \
        if dom.xpath('//h1[@class="mb15"]/span/text()') else "-"
    caritem['price1'] = dom.xpath('//span[@class="price-color"]/em/text()').extract_first() \
        if dom.xpath('//span[@class="price-color"]/em/text()') else "-"
    caritem['pricetag'] = dom.xpath('//div[@class="price-title"]/h5/text()').extract_first() \
        if dom.xpath('//div[@class="price-title"]/h5/text()') else "-"
    caritem['guideprice']='.'.join(dom.xpath('//span[@class="price-color-gray"]/text()').re('\d+\.?\d*'))  \
        if dom.xpath('//span[@class="price-color-gray"]/text()') else "-"
    caritem['guidepricetax']='.'.join(dom.xpath('//i[@class="c9"]/text()').re('\d+\.?\d*')) \
        if dom.xpath('//i[@class="c9"]/text()') else "-"
    return caritem


def parse_baseinfo(dom):
    # caritem init
    caritem = dict()
    # baseinfo
    caritem['registerdate'] =dom.xpath(u'//div[@class="car-detail mb10 pr"]/ul/li[contains(text(),"\u9996\u6b21\u4e0a\u724c")]/span/text()').extract_first()\
        if dom.xpath(u'//div[@class="car-detail mb10 pr"]/ul/li[contains(text(),"\u9996\u6b21\u4e0a\u724c")]/span/text()') else "-"
    caritem['posttime'] = '-'.join(dom.xpath(u'//div[@class="car-detail mb10 pr"]/ul/li[contains(text(),"\u4e0a\u67b6\u65f6\u95f4")]/span/text()').re('\d+')) \
        if dom.xpath(u'//div[@class="car-detail mb10 pr"]/ul/li[contains(text(),"\u4e0a\u67b6\u65f6\u95f4")]/span/text()') else "-"
    caritem['years'] = "-"
    caritem['mileage'] = '.'.join(dom.xpath(u'//div/ul/li[contains(text(),"\u8868\u663e\u91cc\u7a0b")]/span/text()').re('\d+')) \
        if dom.xpath(u'//div/ul/li[contains(text(),"\u8868\u663e\u91cc\u7a0b")]/span/text()') else "-"
    caritem['gear']=dom.xpath(u'//div[@class="car-detail mb10 pr"]/ul/li[contains(text(),"\u9a71\u52a8\u65b9\u5f0f")]/span/text()').extract_first() \
        if dom.xpath(u'//div[@class="car-detail mb10 pr"]/ul/li[contains(text(),"\u9a71\u52a8\u65b9\u5f0f")]/span/text()') else "-"
    caritem['region'] = "-"
    caritem['dealplace'] = dom.xpath(u'//span[contains(text(),"\u770b\u8f66\u5730\u5740")]/following-sibling::*/text()').extract_first() \
        if dom.xpath(u'//span[contains(text(),"\u770b\u8f66\u5730\u5740")]/following-sibling::*/text()') else "-"
    if len(caritem['dealplace'])>255:
        caritem['dealplace']=caritem['dealplace'][0:255]  
    caritem['ratelevel']=dom.xpath('//div[@class="rate"]/a/@class').extract_first() \
        if dom.xpath('//div[@class="rate"]/a/@class') else "-"
    caritem['ratecont']=';'.join(dom.xpath('//div[@class="commend-text"]/ul/li/text()').extract()) \
        if dom.xpath('//div[@class="commend-text"]/ul/li/text()') else "-"

    caritem['province'] = "-"
    caritem['city'] = dom.xpath('//div[@class="current-city fl"]/span[2]/text()').extract_first() \
        if dom.xpath('//div[@class="current-city fl"]/span[2]/text()') else "-"
    caritem['changetimes'] = "-"
    caritem['changedate'] = "-"
    return caritem


def parse_certification(dom):
    # caritem init
    caritem = dict()
    # citification
    caritem['Insurance1'] = dom.xpath(u'//h3[contains(text(),"\u4fdd\u4fee\u5e74\u9650")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u4fdd\u4fee\u5e74\u9650")]/following-sibling::*/i/text()') else "-"
    caritem['Insurance2'] = dom.xpath(u'//h3[contains(text(),"\u4fdd\u9669\u516c\u91cc\u6570")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u4fdd\u9669\u516c\u91cc\u6570")]/following-sibling::*/i/text()') else "-"
    caritem['yearchecktime'] = '-'.join(dom.xpath('//ul[@class="info-ul"]/li[2]/text()').re('\d+')) \
        if dom.xpath('//ul[@class="info-ul"]/li[2]/text()') else "-"
    caritem['carokcf'] = "-"
    caritem['carcard'] = "-"
    caritem['carinvoice'] = "-"
    caritem['accident'] = dom.xpath('//ul[@class="detection-item-img mb30"]/li/em/text()').extract_first() \
        if dom.xpath('//ul[@class="detection-item-img mb30"]/li/em/text()').extract_first() else "-"
    caritem['useage'] = "-"
    return caritem


def parse_dealor(dom):
    # caritem init
    caritem = dict()
    # dealer
    caritem['telphone'] = dom.xpath('//i[@class="phone"]/text()').extract_first() \
            if dom.xpath('//i[@class="phone"]/text()') else "-"
    caritem['dealor'] = "-"  # new

    return caritem


def parse_createinfo(dom, carinfocreate, website, mysqldb):
    caritem = []
    '''
    mycarinfo=[]
    l_mys = dom.xpath('//div[@class="msg fl"]')[:6].xpath('table/tr/td/text()')
    for sel in l_mys:
         l_info=(sel.extract())
         mycarinfo.append(l_info)

    r_mys = dom.xpath('//div[@class="msg fr"]')[:7].xpath('table/tr/td/text()')
    for sel in r_mys:
         r_info=(sel.extract())
         mycarinfo.append(r_info)
    if bool(l_mys) and bool(r_mys) and carinfocreate == True:
        # carinfo create
        j = 0
        carinfocreate = False
        carinfors = []
        ii = dict()
        for i in range(0, len(mycarinfo)-1,2):
            ii = {"carinfo_en": "carinfo" + str(j),
                      "carinfo_cn": mycarinfo[i]}
            carinfors.append(ii)
            j += 1
        carinforsdf = pandas.DataFrame(carinfors)
        carinforsdf.to_sql(name=website + '_carinfo', con=mysqldb, flavor='mysql',
                           if_exists='replace')
    '''


def parse_carinfo2(dom):
    # caritem init
    caritem = dict()
    caritem['level']=dom.xpath(u'//h3[contains(text(),"\u8f66\u8f86\u7ea7\u522b")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u8f66\u8f86\u7ea7\u522b")]/following-sibling::*/i/text()') else "-"
    caritem['motor']=dom.xpath(u'//h3[contains(text(),"\u53d1\u52a8\u673a")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u53d1\u52a8\u673a")]/following-sibling::*/i/text()') else "-"
    caritem['lengthwh']=dom.xpath(u'//h3[contains(text(),"\u8f74\u8ddd")]/following-sibling::*/i/text()').extract_first() \
         if dom.xpath(u'//h3[contains(text(),"\u8f74\u8ddd")]/following-sibling::*/i/text()') else "-"
    caritem['weight']=dom.xpath(u'//h3[contains(text(),"\u6574\u5907\u8d28\u91cf")]/following-sibling::*/i/text()').extract_first() \
         if dom.xpath(u'//h3[contains(text(),"\u6574\u5907\u8d28\u91cf")]/following-sibling::*/i/text()') else "-"
    caritem['luggage']="-"
    caritem['carinfo1'] = dom.xpath(u'//h3[contains(text(),"\u957f\u5ea6(mm)")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u957f\u5ea6(mm)")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo2'] = dom.xpath(
        u'//h3[contains(text(),"\u5bbd\u5ea6(mm)")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u5bbd\u5ea6(mm)")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo3'] = dom.xpath(
        u'//h3[contains(text(),"\u9ad8\u5ea6(mm)")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u9ad8\u5ea6(mm)")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo4'] = dom.xpath(
        u'//h3[contains(text(),"\u8f74\u8ddd(mm)")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u8f74\u8ddd(mm)")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo5'] = dom.xpath(
        u'//h3[contains(text(),"\u524d\u8f6e\u8ddd(mm)")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u524d\u8f6e\u8ddd(mm)")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo6'] = dom.xpath(
        u'//h3[contains(text(),"\u540e\u8f6e\u8ddd(mm)")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u540e\u8f6e\u8ddd(mm)")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo7'] = dom.xpath(
        u'//h3[contains(text(),"\u6700\u5c0f\u79bb\u5730\u95f4\u9699")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u6700\u5c0f\u79bb\u5730\u95f4\u9699")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo8'] = dom.xpath(
        u'//h3[contains(text(),"\u6574\u5907\u8d28\u91cf(kg)")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u6574\u5907\u8d28\u91cf(kg)")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo9'] = dom.xpath(u'//h3[contains(text(),"\u8f66\u8eab\u7ed3\u6784")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u8f66\u8eab\u7ed3\u6784")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo10'] = dom.xpath(
        u'//h3[contains(text(),"\u8f66\u95e8\u6570")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u8f66\u95e8\u6570")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo11'] = dom.xpath(
        u'//h3[contains(text(),"\u8f7d\u5ba2\u6570(\u4eba)")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u8f7d\u5ba2\u6570(\u4eba)")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo12'] = dom.xpath(
        u'//h3[contains(text(),"\u6cb9\u7bb1\u5bb9\u79ef(L)")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u6cb9\u7bb1\u5bb9\u79ef(L)")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo13'] = dom.xpath(
        u'//h3[contains(text(),"\u71c3\u6cb9\u4f9b\u7ed9\u65b9\u5f0f")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u71c3\u6cb9\u4f9b\u7ed9\u65b9\u5f0f")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo14'] = dom.xpath(
        u'//h3[contains(text(),"\u53d1\u52a8\u673a\u7f16\u53f7")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u53d1\u52a8\u673a\u7f16\u53f7")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo15'] = dom.xpath(
        u'//h3[contains(text(),"\u53d1\u52a8\u673a\u6c7d\u7f38\u5bb9\u79ef")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u53d1\u52a8\u673a\u6c7d\u7f38\u5bb9\u79ef")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo16'] = dom.xpath(
        u'//h3[contains(text(),"\u6c7d\u7f38\u6570")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u6c7d\u7f38\u6570")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo17'] = dom.xpath(
        u'//h3[contains(text(),"\u6c14\u95e8\u603b\u6570")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u6c14\u95e8\u603b\u6570")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo18'] = dom.xpath(
        u'//h3[contains(text(),"\u6700\u5927\u529f\u7387")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u6700\u5927\u529f\u7387")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo19'] = dom.xpath(
        u'//h3[contains(text(),"\u6700\u5927\u626d\u77e9")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u6700\u5927\u626d\u77e9")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo20'] = dom.xpath(
        u'//h3[contains(text(),"\u53d1\u52a8\u673a\u7279\u6709\u6280\u672f")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u53d1\u52a8\u673a\u7279\u6709\u6280\u672f")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo21'] = dom.xpath(
        u'//h3[contains(text(),"\u6321\u4f4d\u6570\u91cf")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u6321\u4f4d\u6570\u91cf")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo22'] = dom.xpath(
        u'//h3[contains(text(),"\u524d\u60ac\u6302\u5f62\u5f0f")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u524d\u60ac\u6302\u5f62\u5f0f")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo23'] = dom.xpath(
        u'//h3[contains(text(),"\u540e\u60ac\u6302\u5f62\u5f0f")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u540e\u60ac\u6302\u5f62\u5f0f")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo24'] = dom.xpath(
        u'//h3[contains(text(),"\u52a9\u529b\u8f6c\u5411")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u52a9\u529b\u8f6c\u5411")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo25'] = dom.xpath(
        u'//h3[contains(text(),"\u524d\u5236\u52a8\u5668\u7c7b\u578b")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u524d\u5236\u52a8\u5668\u7c7b\u578b")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo26'] = dom.xpath(
        u'//h3[contains(text(),"\u540e\u5236\u52a8\u5668\u7c7b\u578b")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u540e\u5236\u52a8\u5668\u7c7b\u578b")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo27'] = dom.xpath(
        u'//h3[contains(text(),"\u9a7b\u8f66\u5236\u52a8\u7c7b\u578b")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u9a7b\u8f66\u5236\u52a8\u7c7b\u578b")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo28'] = dom.xpath(
        u'//h3[contains(text(),"\u524d\u8f6e\u89c4\u683c")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u524d\u8f6e\u89c4\u683c")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo29'] = dom.xpath(
        u'//h3[contains(text(),"\u540e\u8f6e\u89c4\u683c")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u540e\u8f6e\u89c4\u683c")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo30'] = dom.xpath(
        u'//h3[contains(text(),"\u4e3b\u9a7e\u9a76\u5b89\u5168\u6c14\u56ca")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u4e3b\u9a7e\u9a76\u5b89\u5168\u6c14\u56ca")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo31'] = dom.xpath(
        u'//h3[contains(text(),"\u526f\u9a7e\u9a76\u5b89\u5168\u6c14\u56ca")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u526f\u9a7e\u9a76\u5b89\u5168\u6c14\u56ca")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo32'] = dom.xpath(
        u'//h3[contains(text(),"\u524d\u6392\u4fa7\u6c14\u56ca")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u524d\u6392\u4fa7\u6c14\u56ca")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo33'] = dom.xpath(
        u'//h3[contains(text(),"\u540e\u6392\u4fa7\u6c14\u56ca")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u540e\u6392\u4fa7\u6c14\u56ca")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo34'] = dom.xpath(
        u'//h3[contains(text(),"\u53d1\u52a8\u673a\u7535\u5b50\u9632\u76d7")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u53d1\u52a8\u673a\u7535\u5b50\u9632\u76d7")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo35'] = dom.xpath(
        u'//h3[contains(text(),"\u9632\u62b1\u6b7b\u5239\u8f66\u7cfb\u7edf")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u9632\u62b1\u6b7b\u5239\u8f66\u7cfb\u7edf")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo36'] = dom.xpath(
        u'//h3[contains(text(),"\u5236\u52a8\u529b\u5206\u914d\u7cfb\u7edf")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u5236\u52a8\u529b\u5206\u914d\u7cfb\u7edf")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo37'] = dom.xpath(
        u'//h3[contains(text(),"\u5236\u52a8\u8f85\u52a9\u7cfb\u7edf")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u5236\u52a8\u8f85\u52a9\u7cfb\u7edf")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo38'] = dom.xpath(
        u'//h3[contains(text(),"\u7275\u5f15\u529b\u63a7\u5236\u7cfb\u7edf")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u7275\u5f15\u529b\u63a7\u5236\u7cfb\u7edf")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo39'] = dom.xpath(
        u'//h3[contains(text(),"\u8f66\u8eab\u7a33\u5b9a\u6027\u63a7\u5236\u7cfb\u7edf")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u8f66\u8eab\u7a33\u5b9a\u6027\u63a7\u5236\u7cfb\u7edf")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo40'] = dom.xpath(
        u'//h3[contains(text(),"\u5929\u7a97")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u5929\u7a97")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo41'] = dom.xpath(
        u'//h3[contains(text(),"\u65b9\u5411\u76d8\u6750\u8d28")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u65b9\u5411\u76d8\u6750\u8d28")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo42'] = dom.xpath(
        u'//h3[contains(text(),"\u5012\u8f66\u96f7\u8fbe")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u5012\u8f66\u96f7\u8fbe")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo43'] = dom.xpath(
        u'//h3[contains(text(),"\u5012\u8f66\u5f71\u50cf")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u5012\u8f66\u5f71\u50cf")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo44'] = dom.xpath(
        u'//h3[contains(text(),"\u5ea7\u6905\u6750\u6599")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u5ea7\u6905\u6750\u6599")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo45'] = dom.xpath(
        u'//h3[contains(text(),"\u5bfc\u822a\u7cfb\u7edf(GPS)")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u5bfc\u822a\u7cfb\u7edf(GPS)")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo46'] = dom.xpath(
        u'//h3[contains(text(),"\u626c\u58f0\u5668\u6570\u91cf")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u626c\u58f0\u5668\u6570\u91cf")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo47'] = dom.xpath(
        u'//h3[contains(text(),"\u624b\u52a8\u7a7a\u8c03")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u624b\u52a8\u7a7a\u8c03")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo48'] = dom.xpath(
        u'//h3[contains(text(),"\u81ea\u52a8\u7a7a\u8c03")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u81ea\u52a8\u7a7a\u8c03")]/following-sibling::*/i/text()') else "-"
    caritem['carinfo49'] = dom.xpath(u'//h3[contains(text(),"\u5382\u5546")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u5382\u5546")]/following-sibling::*/i/text()') else "-"

    return caritem


def parse_carinfo1(dom):
    # caritem init
    caritem = dict()
    # carinfo
    caritem['brand_name'] =dom.xpath('//div[@class="w1200 bread-Crumbs"]/a[2]/text()').extract_first() \
        if dom.xpath('//div[@class="w1200 bread-Crumbs"]/a[2]/text()') else "-"
    caritem['class_name'] = dom.xpath('//div[@class="w1200 bread-Crumbs"]/a[3]/text()').extract_first() \
        if dom.xpath('//div[@class="w1200 bread-Crumbs"]/a[3]/text()') else "-"
    caritem['output']= re.compile('L|T').sub('',dom.xpath(u'//h3[contains(text(),"\u53d1\u52a8\u673a")]/following-sibling::*/i/text()').extract_first().split(' ')[0])\
        if dom.xpath(u'//h3[contains(text(),"\u53d1\u52a8\u673a")]/following-sibling::*/i/text()') else "-"
    caritem['geartype'] =dom.xpath(u'//div[@class="car-detail mb10 pr"]/ul/li[contains(text(),"\u53d8")]/span/text()').extract_first() \
        if dom.xpath(u'//div[@class="car-detail mb10 pr"]/ul/li[contains(text(),"\u53d8")]/span/text()') else "-"

    caritem['emission'] = dom.xpath(u'//h3[contains(text(),"\u6392\u653e\u6807\u51c6")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u6392\u653e\u6807\u51c6")]/following-sibling::*/i/text()') else "-"

    caritem['color'] = dom.xpath(u'//div[@class="car-detail mb10 pr"]/ul/li[contains(text(),"\u5916\u89c2")]/span/text()').extract_first() \
        if dom.xpath(u'//div[@class="car-detail mb10 pr"]/ul/li[contains(text(),"\u5916\u89c2")]/span/text()') else "-"
    caritem['body'] = dom.xpath(
        u'//h3[contains(text(),"\u8f66\u53a2\u5f62\u5f0f")]/following-sibling::*/i/text()').extract_first() \
        if dom.xpath(u'//h3[contains(text(),"\u8f66\u53a2\u5f62\u5f0f")]/following-sibling::*/i/text()') else "-"
    caritem['newcartitle'] = "-"  # new
    caritem['newcarurl'] = '-'  # new
    return caritem


def parse_otherinfo(dom):
    # caritem init
    caritem = dict()
    '''
    mycarinfo=[]
    l_mys = dom.xpath('//div[@class="msg fl"]')[:6].xpath('table/tr/td/text()')
    for sel in l_mys:
         l_info=(sel.extract())
         mycarinfo.append(l_info)

    r_mys = dom.xpath('//div[@class="msg fr"]')[:7].xpath('table/tr/td/text()')
    for sel in r_mys:
         r_info=(sel.extract())
         mycarinfo.append(r_info)

    if bool(l_mys) and bool(r_mys) :
        # carinfo create
        j = 0
        for i in range(0, len(mycarinfo)-1,2):
            caritem["carinfo" + str(j)] = mycarinfo[i+1]
            j += 1
    '''
    return caritem


def parse_checkpoints(dom):
    # caritem init
    caritem = dict()
    '''
    # checkpoints
    descnames = ['accidentdesc', 'outerdesc', 'innerdesc', 'safedesc', 'roaddesc', ]
    scorenames = ['accidentscore', 'outerscore', 'innerscore', 'safescore', 'roadscore', ]
    for j in range(0, 5):
        caritem[scorenames[j]] = 0
        caritem[descnames[j]] = '-'
    checkdesc = dom.xpath('//p[@class="scpci_title"]/text()')
    caritem['totalcheck'] = dom.xpath('//div[@class="sc_info_right"]/p/text()').extract_first() \
        if dom.xpath('//div[@class="sc_info_right"]/p/text()') else "-"
    caritem['accidentdesc'] = "-".join(checkdesc)
        if checkdesc else "-"
    '''
    return caritem


def parse_desc(dom):
    # caritem init
    caritem = dict()
    # more desc
    caritem['desc'] = "-"
    caritem['img_url'] = dom.xpath('//ul[@class="photoswrap"]/li[1]/a/img/@src').extract_first() \
        if dom.xpath('//ul[@class="photoswrap"]/li[1]/a/img/@src').extract_first() else "-"
    return caritem


# car parse control
def parse(item):
    #-*- coding: UTF-8 -*-
    #carinit
    caritems=[]
    #params
    params = Init()
    processparamlist =ParseprocessInit(params)
    website= processparamlist[0]
    carinfocreate=processparamlist[1]
    counts=processparamlist[2]
    savesize=processparamlist[3]
    mysqltable=processparamlist[4]
    # connection=processparamlist[5]
    # collection=processparamlist[6]
    mysqldb=processparamlist[7]
    mysqldbc=processparamlist[8]
    # df=processparamlist[9]
    try:
        # counts += 1
        # print counts
        # parse original:1
        # caritem init
        # parse original:1
        caritem = parse_original(item)
        # parse keyinfo:2
        content = item['datasave'][1]
        dom = scrapy.selector.Selector(text=content)
        # if dom.xpath('//div[not(@id="detail_main_info")]'):
        #     continue
        caritem = dict(caritem, **parse_keyinfo(dom))
        # parse baseinfo:3
        caritem = dict(caritem, **parse_baseinfo(dom))
        # parse certification:4
        caritem = dict(caritem, **parse_certification(dom))
        # parse dealor:5
        caritem = dict(caritem, **parse_dealor(dom))
        # parse createinfo:6
        # parse_createinfo(dom,carinfocreate,website,mysqldb)
        # parse carinfo:7
        caritem = dict(caritem, **parse_carinfo2(dom))
        caritem = dict(caritem, **parse_carinfo1(dom))
        # caritem = dict(caritem, **parse_otherinfo(dom))
        # parse checkpoints:8
        # caritem = dict(caritem, **parse_checkpoints(dom))
        # parse desc:9
        caritem = dict(caritem, **parse_desc(dom))

        # add
        caritems.append(caritem)
        # save to sql
        caritems = savecar(caritems, savesize, website, mysqldb)
        # except:
        #             try:
        #                 # save exception
        #                 print str(counts) + ":" + i["url"] + ", parse error."
        #                 saveerror(counts, i['url'], website, mysqldb)
        #                 continue
        #             except:
        #                 pass
        #     else:
        #         print "item duplicated!"
        # final save
    except:
        pass
    savecarfinal(caritems,mysqltable,mysqldb,savesize)
    conclose(mysqldb,mysqldbc)
    return "One group finish"





#parse(0, 200)
# ppexcut(8)






