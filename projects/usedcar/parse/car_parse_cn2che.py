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


#basesetting
def Init():
    #params
    website ='cn2che'
    params =ParseInit(website)
    #mysql redefine
    params['createsql']="""CREATE TABLE IF NOT EXISTS `cn2che` (
                                `id` bigint(20) NOT NULL auto_increment,
                                `website` varchar(63) DEFAULT NULL,
                                `carid` varchar(63) DEFAULT NULL,
                                `title` varchar(127) DEFAULT NULL,
                                `pagetitle` varchar(127) DEFAULT NULL,
                                `url` varchar(127) DEFAULT NULL,
                                `grabtime` varchar(63) DEFAULT NULL,
                                `pagetime` varchar(63) DEFAULT NULL,
                                `posttime` varchar(63) DEFAULT NULL,
                                `parsetime` varchar(63) DEFAULT NULL,
                                `price1` varchar(63) DEFAULT NULL,
                                `pricetag` varchar(63) DEFAULT NULL,
                                `status` varchar(63) DEFAULT NULL,
                                `statusplus` varchar(127) DEFAULT NULL,
                                `registerdate` varchar(63) DEFAULT NULL,
                                `years` varchar(63) DEFAULT NULL,
                                `mileage` varchar(63) DEFAULT NULL,
                                `color` varchar(63) DEFAULT NULL,
                                `province` varchar(63) DEFAULT NULL,
                                `city` varchar(63) DEFAULT NULL,
                                `region` varchar(63) DEFAULT NULL,
                                `dealplace` varchar(63) DEFAULT NULL,
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
                                `dealtype` varchar(127) DEFAULT NULL,
                                `dealcounts` varchar(127) DEFAULT NULL,
                                `dealcompany` varchar(127) DEFAULT NULL,
                                `dealmail` varchar(127) DEFAULT NULL,
                                `garage` varchar(127) DEFAULT NULL,
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
                                 `desc` varchar(551) DEFAULT NULL,
                                 `img_url` varchar(255) DEFAULT NULL,
                                 `carinfo0` varchar(255) DEFAULT NULL,
                                 `carinfo1` varchar(255) DEFAULT NULL,
                                 `carinfo2` varchar(255) DEFAULT NULL,
                                 `carinfo3` varchar(255) DEFAULT NULL,
                                 `carinfo4` varchar(255) DEFAULT NULL,
                                 `carinfo5` varchar(255) DEFAULT NULL,
                                 `carinfo6` varchar(255) DEFAULT NULL,
                                 `carinfo7` varchar(255) DEFAULT NULL,
                                 `carinfo8` varchar(255) DEFAULT NULL,
                                 `carinfo9` varchar(255) DEFAULT NULL,
                                 `carinfo10` varchar(255) DEFAULT NULL,
                                 `carinfo11` varchar(255) DEFAULT NULL,
                                 `carinfo12` varchar(255) DEFAULT NULL,
                                 `carinfo13` varchar(255) DEFAULT NULL,
                                 `carinfo14` varchar(255) DEFAULT NULL,
                                 `carinfo15` varchar(255) DEFAULT NULL,
                                 `carinfo16` varchar(255) DEFAULT NULL,
                                 `carinfo17` varchar(255) DEFAULT NULL,
                                 `carinfo18` varchar(255) DEFAULT NULL,
                                 `carinfo19` varchar(255) DEFAULT NULL,
                                 `carinfo20` varchar(255) DEFAULT NULL,
                                 `carinfo21` varchar(255) DEFAULT NULL,
                                 `carinfo22` varchar(255) DEFAULT NULL,
                                 `carinfo23` varchar(255) DEFAULT NULL,
                                 `carinfo24` varchar(255) DEFAULT NULL,
                                 `carinfo25` varchar(255) DEFAULT NULL,
                                 `carinfo26` varchar(255) DEFAULT NULL,
                                 `carinfo27` varchar(255) DEFAULT NULL,
                                 `carinfo28` varchar(255) DEFAULT NULL,
                                 `carinfo29` varchar(255) DEFAULT NULL,
                                 `carinfo30` varchar(255) DEFAULT NULL,
                                 `carinfo31` varchar(255) DEFAULT NULL,
                                 `carinfo32` varchar(255) DEFAULT NULL,
                                 `carinfo33` varchar(255) DEFAULT NULL,
                                 `carinfo34` varchar(255) DEFAULT NULL,
                                 `carinfo35` varchar(255) DEFAULT NULL,
                                 `carinfo36` varchar(255) DEFAULT NULL,
                                 `carinfo37` varchar(255) DEFAULT NULL,
                                 `carinfo38` varchar(255) DEFAULT NULL,
                                 `carinfo39` varchar(255) DEFAULT NULL,
                                 `carinfo40` varchar(255) DEFAULT NULL,
                                 `carinfo41` varchar(255) DEFAULT NULL,
                                 `carinfo42` varchar(255) DEFAULT NULL,
                                 `carinfo43` varchar(255) DEFAULT NULL,
                                 `carinfo44` varchar(255) DEFAULT NULL,
                                 `carinfo45` varchar(255) DEFAULT NULL,
                                 `carinfo46` varchar(255) DEFAULT NULL,
                                 PRIMARY KEY  (`id`)
                              ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
    params['mysqltable']='cn2che'
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
    #caritem init
    caritem = dict()
    # keyinfro
    caritem['website'] = item['website']
    caritem['carid'] = str(re.findall('\d+', item["url"])[1])
    caritem['url'] = item["url"]
    caritem['grabtime'] = item["grabtime"]
    caritem['pagetime'] = item["pagetime"]  # new
    caritem['parsetime'] = time.strftime('%Y-%m-%d %X', time.localtime())
    # status
    caritem['status'] = str(re.findall('sale|sold', item["status"])[0])
    caritem['statusplus'] = item["status"]
    return caritem

def parse_keyinfo(dom):
    # caritem init
    caritem = dict()
    # keyinfro
    caritem['pagetitle'] = dom.xpath('//title/text()').extract_first() if dom.xpath('//title/text()') else "-"
    caritem['title'] = dom.xpath('//p[@class="vice"]/a/text()').extract_first() if dom.xpath('//p[@class="vice"]/a/text()') else "-"
    caritem['price1'] = '.'.join(dom.xpath('//strong[@id="price"]/text()').re('\d+\.?\d*') ) \
        if dom.xpath('//strong[@id="price"]/text()') else "-"
    caritem['pricetag'] = "-"
    return caritem

def parse_baseinfo(dom):
    # caritem init
    caritem = dict()
    # baseinfo
    caritem['registerdate'] = (dom.xpath(u'//li[contains(text(),"\u4e0a\u724c\u65f6\u95f4")]/text()').extract_first().split(u'\uff1a')[1]+'-1') \
        if dom.xpath(u'//li[contains(text(),"\u4e0a\u724c\u65f6\u95f4")]') else "-"
    caritem['posttime'] = dom.xpath('//li[@class="sendtime"]/text()').extract_first().split(u'\uff1a')[1].split(' ')[0] \
        if dom.xpath('//li[@class="sendtime"]/text()') else "-"
    caritem['years'] = "-"  # new
    caritem['mileage'] = '.'.join(dom.xpath(u'//li[contains(text(),"\u884c\u9a76\u91cc\u7a0b")]/text()').re('\d+\.?\d*')) \
        if dom.xpath(u'//li[contains(text(),"\u884c\u9a76\u91cc\u7a0b")]') else "-"
    caritem['gear'] = dom.xpath(u'//table/tr/td[contains(text(),"\u9a71\u52a8\u65b9\u5f0f")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u9a71\u52a8\u65b9\u5f0f")]/following-sibling::*/text()') else "-"
    caritem['region'] = dom.xpath(u'//li[contains(text(),"\u4ea4\u6613\u5730\u533a")]/text()').extract_first().split(u'\uff1a')[1] \
        if dom.xpath(u'//li[contains(text(),"\u4ea4\u6613\u5730\u533a")]/text()').extract_first() else "-"
    if caritem['region'] != "-" and caritem["region"] != "":
        if "-" in caritem['region']:
            caritem['province'] = caritem['region'].split('-')[0]
            caritem['city'] = caritem['region'].split('-')[1]
        else:
            caritem['province'] = caritem['region']
            caritem['city'] = "-"
    else:
        caritem['province'] = "-"
        caritem['city'] = "-"
    caritem['dealplace'] = dom.xpath('//dd[@id="address"]/text()').extract_first() \
        if dom.xpath('//dd[@id="address"]/text()') else "-"
    caritem['changetimes'] = "-"
    caritem['changedate'] = "-"
    return caritem

def parse_certification(dom):
    # caritem init
    caritem = dict()
    # citification
    caritem['Insurance1'] = dom.xpath(u'//table/tr/td[contains(text(),"\u4fdd \u9669")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u4fdd \u9669")]/following-sibling::*/text()') else "-"
    caritem['Insurance2'] = "-"

    caritem['yearchecktime'] =dom.xpath(u'//table/tr/td[contains(text(),"\u5e74 \u68c0")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u5e74 \u68c0")]/following-sibling::*/text()') else "-"
    caritem['carokcf'] = "-"
    caritem['carcard'] = dom.xpath('//span[@id="carid"]/text()').extract_first() \
        if dom.xpath('//span[@id="carid"]') else "-"
    caritem['carinvoice'] = "-"
    caritem['accident'] = "-"  # new
    caritem['useage'] ="-"
    return caritem

def parse_dealor(dom):
    # caritem init
    caritem = dict()
    # dealer
    caritem['telphone'] =dom.xpath('//dd[@class="The"]/b[@id="phone"]/text()').extract_first() \
        if dom.xpath('//dd[@class="The"]/b[@id="phone"]/text()') else "-"
    caritem['dealor']=dom.xpath('//dt[@id="linkman"]/text()').extract_first() \
        if dom.xpath('//dt[@id="linkman"]/text()') else '-'
    dealtypeifro=dom.xpath('//h2[@id="caruser"]/text()').extract_first()
    if dom.xpath('//h2[@id="caruser"]/text()'):
        if dealtypeifro.find(u'\u4f1a\u5458\u4fe1\u606f')!=-1:
            caritem['dealtype']=u'\u4e2a\u4eba'
        else:
            if dealtypeifro.find(u'\u8f66\u5546\u4fe1\u606f')!=-1:
                caritem['dealtype']=u'\u5546\u5bb6'
            else:
                caritem['dealtype'] = "-"
    else:
        caritem['dealtype'] = "-"
    caritem['dealcounts']=dom.xpath('//dl/dd/strong[@id="carcount"]/text()').extract_first() \
        if dom.xpath('//dl/dd/strong[@id="carcount"]/text()') else "-"
    caritem['dealcompany']=dom.xpath('//dl/dd[@id="shopname"]/text()').extract_first() \
        if dom.xpath('//dl/dd[@id="shopname"]/text()') else "-"
    caritem['dealmail']=dom.xpath('//dl/dd[@id="email"]/text()').extract_first() \
        if dom.xpath('//dl/dd[@id="email"]/text()') else "-"
    caritem['garage']=dom.xpath('//dl/dd[@id="memberurl"]/text()').extract_first() \
        if dom.xpath('//dl/dd[@id="memberurl"]/text()') else "-"
    return caritem

def parse_createinfo(dom,carinfocreate,website,mysqldb):
    mycarinfo=[]
    '''
    l_mys = dom.xpath('//div[@class="list"]')[1:6].xpath('table/tr/td[not(@class="table03")]/text()')
    for sel in l_mys:
         l_info=(sel.extract())
         mycarinfo.append(l_info)
    if bool(l_mys) and carinfocreate == True:
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
    caritem['carinfo0']=dom.xpath(u'//table/tr/td[contains(text(),"\u7efc\u5408\u5de5\u51b5")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u7efc\u5408\u5de5\u51b5")]/following-sibling::*/text()') else "-"
    caritem['carinfo1']=dom.xpath(u'//table/tr/td[contains(text(),"\u8f6c\u5f2f\u534a\u5f84")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u8f6c\u5f2f\u534a\u5f84")]/following-sibling::*/text()') else "-"
    caritem['carinfo2']='.'.join(dom.xpath(u'//table/tr/td[contains(text(),"\u4e58\u5458\u4eba\u6570")]/following-sibling::td[1]/text()').re('\d+\.?\d*')).strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u4e58\u5458\u4eba\u6570")]/following-sibling::td[1]/text()') else "-"
    caritem['carinfo3']='.'.join(dom.xpath(u'//table/tr/td[contains(text(),"\u6574\u5907\u8d28\u91cf")]/following-sibling::td[1]/text()').re('\d+\.?\d*')).strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u6574\u5907\u8d28\u91cf")]/following-sibling::*/text()') else "-"
    caritem['carinfo4']='.'.join(dom.xpath(u'//table/tr/td[contains(text(),"\u6700\u5927\u627f\u8f7d\u8d28\u91cf")]/following-sibling::*/text()').re('\d+\.?\d*')).strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u6700\u5927\u627f\u8f7d\u8d28\u91cf")]/following-sibling::*/text()') else "-"
    caritem['carinfo5']=dom.xpath(u'//table/tr/td[contains(text(),"\u52a0\u901f\u65f6\u95f4")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u52a0\u901f\u65f6\u95f4")]/following-sibling::*/text()') else "-"
    caritem['carinfo6'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u6700\u9ad8\u8f66\u901f")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u6700\u9ad8\u8f66\u901f")]/following-sibling::*/text()') else "-"
    caritem['carinfo7'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u8f66\u95e8\u6570")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u8f66\u95e8\u6570")]/following-sibling::*/text()') else "-"
    caritem['carinfo8'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u8f66\u8eab\u578b\u5f0f")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u8f66\u8eab\u578b\u5f0f")]/following-sibling::*/text()') else "-"
    caritem['carinfo9'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u8f66\u9876\u578b\u5f0f")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u8f66\u9876\u578b\u5f0f")]/following-sibling::*/text()') else "-"
    caritem['carinfo10'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u5929\u7a97\u578b\u5f0f")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u5929\u7a97\u578b\u5f0f")]/following-sibling::*/text()') else "-"
    caritem['carinfo11'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u5929\u7a97\u5f00\u5408\u65b9\u5f0f")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u5929\u7a97\u5f00\u5408\u65b9\u5f0f")]/following-sibling::*/text()') else "-"
    caritem['carinfo12'] = '.'.join(dom.xpath(
        u'//table/tr/td[contains(text(),"\u957f")]/following-sibling::td[1]/text()').re('\d+\.?\d*')).strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u957f")]/following-sibling::*/text()') else "-"
    caritem['carinfo13'] = '.'.join(dom.xpath(
        u'//table/tr/td[contains(text(),"\u5bbd")]/following-sibling::td[1]/text()').re('\d+\.?\d*')).strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u5bbd")]/following-sibling::*/text()') else "-"
    caritem['carinfo14'] = '.'.join(dom.xpath(
        u'//table/tr/td[contains(text(),"\u5bbd")]/following-sibling::td[3]/text()').re('\d+\.?\d*')).strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u5bbd")]/following-sibling::td[3]/text()') else "-"
    caritem['carinfo15'] = '.'.join(dom.xpath(
        u'//table/tr/td[contains(text(),"\u8f74\u8ddd")]/following-sibling::td[1]/text()').re('\d+\.?\d*')).strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u8f74\u8ddd")]/following-sibling::td[1]/text()') else "-"
    caritem['carinfo16'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u63a5\u8fd1\u89d2")]/following-sibling::td[1]/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u63a5\u8fd1\u89d2")]/following-sibling::td[1]/text()') else "-"
    caritem['carinfo17'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u79bb\u53bb\u89d2")]/following-sibling::td[1]/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u79bb\u53bb\u89d2")]/following-sibling::td[1]/text()') else "-"
    caritem['carinfo18'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u884c\u674e\u7bb1\u5bb9\u79ef")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u884c\u674e\u7bb1\u5bb9\u79ef")]/following-sibling::*/text()') else "-"
    caritem['carinfo19'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u71c3\u6cb9\u7bb1\u5bb9\u79ef")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u71c3\u6cb9\u7bb1\u5bb9\u79ef")]/following-sibling::*/text()') else "-"
    caritem['carinfo20'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u71c3\u6599\u7c7b\u578b")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u71c3\u6599\u7c7b\u578b")]/following-sibling::*/text()') else "-"
    caritem['carinfo21'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u4f9b\u6cb9\u65b9\u5f0f")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u4f9b\u6cb9\u65b9\u5f0f")]/following-sibling::*/text()') else "-"
    caritem['carinfo22'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u6700\u5927\u529f\u7387-\u529f\u7387\u503c")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u6700\u5927\u529f\u7387-\u529f\u7387\u503c")]/following-sibling::*/text()') else "-"
    caritem['carinfo23'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u6700\u5927\u529f\u7387-\u8f6c\u901f")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u6700\u5927\u529f\u7387-\u8f6c\u901f")]/following-sibling::*/text()') else "-"
    caritem['carinfo24'] = '.'.join(dom.xpath(
        u'//table/tr/td[contains(text(),"\u6700\u5927\u626d\u77e9-\u626d\u77e9\u503c")]/following-sibling::td[1]/text()').re('\d+\.?\d*')).strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u6700\u5927\u626d\u77e9-\u626d\u77e9\u503c")]/following-sibling::td[1]/text()') else "-"
    caritem['carinfo25'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u6c14\u7f38\u6392\u5217\u578b\u5f0f")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u6c14\u7f38\u6392\u5217\u578b\u5f0f")]/following-sibling::*/text()') else "-"
    caritem['carinfo26'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u53d1\u52a8\u673a\u4f4d\u7f6e")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u53d1\u52a8\u673a\u4f4d\u7f6e")]/following-sibling::*/text()') else "-"
    caritem['carinfo27'] = '.'.join(dom.xpath(
        u'//table/tr/td[contains(text(),"\u6700\u5927\u9a6c\u529b")]/following-sibling::td[1]/text()').re('\d+\.?\d*')).strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u6700\u5927\u9a6c\u529b")]/following-sibling::*/text()') else "-"
    caritem['carinfo28'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u8fdb\u6c14\u578b\u5f0f")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u8fdb\u6c14\u578b\u5f0f")]/following-sibling::*/text()') else "-"
    caritem['carinfo29'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u51f8\u8f6e\u8f74")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u51f8\u8f6e\u8f74")]/following-sibling::*/text()') else "-"
    caritem['carinfo30'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u6c7d\u7f38\u6570")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u6c7d\u7f38\u6570")]/following-sibling::*/text()') else "-"
    caritem['carinfo31'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u7f38\u5f84")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u7f38\u5f84")]/following-sibling::*/text()') else "-"
    caritem['carinfo32'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u884c\u7a0b")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u884c\u7a0b")]/following-sibling::*/text()') else "-"
    caritem['carinfo33'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u6bcf\u7f38\u6c14\u95e8\u6570")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u6bcf\u7f38\u6c14\u95e8\u6570")]/following-sibling::*/text()') else "-"
    caritem['carinfo34'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u538b\u7f29\u6bd4")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u538b\u7f29\u6bd4")]/following-sibling::*/text()') else "-"
    caritem['carinfo35'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u524d\u8f6e\u80ce\u89c4\u683c")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u524d\u8f6e\u80ce\u89c4\u683c")]/following-sibling::*/text()') else "-"
    caritem['carinfo36'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u540e\u8f6e\u80ce\u89c4\u683c")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u540e\u8f6e\u80ce\u89c4\u683c")]/following-sibling::*/text()') else "-"
    caritem['carinfo37'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u96e8\u5237\u4f20\u611f\u5668")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u96e8\u5237\u4f20\u611f\u5668")]/following-sibling::*/text()') else "-"
    caritem['carinfo38'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u65b9\u5411\u76d8\u8868\u9762\u6750\u6599")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u65b9\u5411\u76d8\u8868\u9762\u6750\u6599")]/following-sibling::*/text()') else "-"
    caritem['carinfo39'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u5b9a\u901f\u5de1\u822a\u7cfb\u7edf")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u5b9a\u901f\u5de1\u822a\u7cfb\u7edf")]/following-sibling::*/text()') else "-"
    caritem['carinfo40'] = dom.xpath(
        u'//table/tr/td[contains(text(),"GPS\u7535\u5b50\u5bfc\u822a")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"GPS\u7535\u5b50\u5bfc\u822a")]/following-sibling::*/text()') else "-"
    caritem['carinfo41'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u5012\u8f66\u96f7\u8fbe")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u5012\u8f66\u96f7\u8fbe")]/following-sibling::*/text()') else "-"
    caritem['carinfo42'] = dom.xpath(
        u'//table/tr/td[contains(text(),"ABS(\u5239\u8f66")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"ABS(\u5239\u8f66")]/following-sibling::*/text()') else "-"
    caritem['carinfo43'] = dom.xpath(
        u'//table/tr/td[contains(text(),"DSC(\u52a8\u6001")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"DSC(\u52a8\u6001")]/following-sibling::*/text()') else "-"
    caritem['carinfo44'] = dom.xpath(
        u'//table/tr/td[contains(text(),"EBA/EVA(\u7d27\u6025")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"EBA/EVA(\u7d27\u6025")]/following-sibling::*/text()') else "-"
    caritem['carinfo45'] = dom.xpath(
        u'//table/tr/td[contains(text(),"EBD/EBV(\u7535\u5b50")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"EBD/EBV(\u7535\u5b50")]/following-sibling::*/text()') else "-"
    caritem['carinfo46'] = dom.xpath(
        u'//table/tr/td[contains(text(),"\u9a7e\u9a76\u4f4d\u5b89\u5168\u6c14\u56ca")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u9a7e\u9a76\u4f4d\u5b89\u5168\u6c14\u56ca")]/following-sibling::*/text()') else "-"
    return caritem
def parse_carinfo1(dom):
    # caritem init
    caritem = dict()
    # carinfo
    caritem['brand_name'] = dom.xpath(u'//li[contains(text(),"\u8f66\u8f86\u54c1\u724c")]/text()').extract_first().split(u'\uff1a')[1] \
        if dom.xpath(u'//li[contains(text(),"\u8f66\u8f86\u54c1\u724c")]') else "-"
    caritem['class_name'] =dom.xpath(u'//li[contains(text(),"\u8f66\u8f86\u7cfb\u5217")]/text()').extract_first().split(u'\uff1a')[1] \
        if dom.xpath(u'//li[contains(text(),"\u8f66\u8f86\u7cfb\u5217")]') else "-"
    dataoutput=dom.xpath(u'//table/tr/td[contains(text(),"\u6392\u91cf")]/following-sibling::td[1]/text()').extract_first().strip()
    if dom.xpath(u'//table/tr/td[contains(text(),"\u6392\u91cf")]/following-sibling::td[1]/text()'):
        if dataoutput=="":
            caritem['output'] = "-"
        else:
            dataout = float(re.compile('mL|L').sub('', dataoutput))
            if dataout>10:
                caritem['output'] =round(dataout/1000,1)
            else:
                caritem['output'] = round(dataout,1)
    else:
        caritem['output'] = "-"
    caritem['geartype'] =  dom.xpath(u'//table/tr/td[contains(text(),"\u53d8 \u901f \u5668")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u53d8 \u901f \u5668")]/following-sibling::*/text()') else "-"
    caritem['emission'] = dom.xpath(u'//table/tr/td[contains(text(),"\u73af\u4fdd\u6807\u51c6")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u73af\u4fdd\u6807\u51c6")]/following-sibling::*/text()') else "-"
    caritem['color'] =dom.xpath(u'//table/tr/td[contains(text(),"\u6c7d\u8f66\u989c\u8272")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//table/tr/td[contains(text(),"\u6c7d\u8f66\u989c\u8272")]/following-sibling::*/text()') else "-"
    caritem['body'] = "-"
    caritem['guideprice'] = "-"
    caritem['guidepricetax'] = '-'
    caritem['newcartitle'] = "-"
    caritem['newcarurl'] = '-'
    return caritem

def parse_otherinfo(dom):
    # caritem init
    caritem = dict()
    '''
    mycarinfo=[]
    l_mys = dom.xpath('//div[@class="list"]')[1:6].xpath('table/tr/td[not(@class="table03")]/text()')
    for sel in l_mys:
         l_info=(sel.extract())
         mycarinfo.append(l_info)

    if bool(l_mys)  :
        # carinfo create
        j = 0
        for i in range(0, len(mycarinfo)-1,2):            
            caritem["carinfo" + str(j)] = mycarinfo[i+1]
            j += 1
    '''
    return caritem

def parse_checkpoints( dom):
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
    caritem['totalcheck'] = dom.xpath('//div[@class="sc_info_right"]/p/text()').extract_first()
        if dom.xpath('//div[@class="sc_info_right"]/p/text()') else "-"
    caritem['accidentdesc'] = "-".join(checkdesc)
        if checkdesc else "-"
    '''
    return caritem

def parse_desc( dom):
    # caritem init
    caritem = dict()
    # more desc
    caritem['desc'] = dom.xpath('//span[@class="describe"]/text()').extract_first() \
        if dom.xpath('//span[@class="describe"]/text()') else "-"
    if len(caritem['desc'])>551:
        caritem['desc']=caritem['desc'][:551]
    caritem['img_url'] = dom.xpath('//ul[@id="chepic"]/li[1]/a/img/@src').extract_first() \
        if dom.xpath('//ul[@id="chepic"]/li[1]/a/img/@src') else "-"  # new
    return caritem


#car parse control
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

    # for i in collection.find().skip(start).limit(step):
    #     returndf=bloom_check(i['status'],df)
    #     if not returndf:
    #         try:
    try:
        # counts += 1
        # print counts
        #parse original:1
        # caritem init
        # parse original:1
        caritem = parse_original(item)
        # parse keyinfo:2
        content= item['datasave'][1]
        dom = scrapy.selector.Selector(text=content)
        # if dom.xpath(u'//title[contains(text(),"\u60a8\u8bbf\u95ee\u7684\u9875\u9762\u51fa\u9519\u4e86")]'):
        #     continue
        caritem = dict(caritem, **parse_keyinfo(dom))

        # parse baseinfo:3
        caritem = dict(caritem, **parse_baseinfo(dom))
        # parse certification:4
        caritem = dict(caritem, **parse_certification(dom))
        # parse dealor:5
        caritem = dict(caritem, **parse_dealor(dom))
        # parse createinfo:6
        #parse_createinfo(dom,carinfocreate,website,mysqldb)
        # parse carinfo:7
        caritem = dict(caritem, **parse_carinfo1(dom))
        caritem = dict(caritem, **parse_carinfo2(dom))
        #caritem = dict(caritem, **parse_otherinfo(dom))
        # parse checkpoints:8
        #caritem = dict(caritem, **parse_checkpoints(dom))
        # parse desc:9
        caritem = dict(caritem, **parse_desc(dom))

        #add
        caritems.append(caritem)
        #save to sql
        caritems=savecar(caritems,savesize,website,mysqldb)
    #         except:
        #              try:
        #                  #save exception
        #                  print str(counts)+":" + i["url"]+", parse error."
        #                  saveerror(counts,i['url'],website,mysqldb)
        #                  continue
        #              except:
        #                  pass
        #     else:
        #         print "item duplicated!"
        # #final save
    except:
        pass
    savecarfinal(caritems,mysqltable,mysqldb,savesize)
    conclose(mysqldb,mysqldbc)
    return "One group finish"


# parse(0,200)
#ppexcut(8)






