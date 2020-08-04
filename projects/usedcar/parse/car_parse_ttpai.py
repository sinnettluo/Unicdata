
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
    website ='ttpai'
    params =ParseInit(website)

    #mysql redefine
    params['createsql']="""CREATE TABLE IF NOT EXISTS `ttpai_test` (
                                `id` bigint(20) NOT NULL auto_increment,
                                `website` varchar(63) DEFAULT NULL,
                                `carid` varchar(63) DEFAULT NULL,
                                `title` varchar(200) DEFAULT NULL,
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
                                `dealplace` varchar(551) DEFAULT NULL,
                                `changetimes` varchar(63) DEFAULT NULL,
                                `changedate` varchar(63) DEFAULT NULL,
                                `Insurance1` varchar(63) DEFAULT NULL,
                                `Insurance2` varchar(63) DEFAULT NULL,
                                `yearchecktime` varchar(63) DEFAULT NULL,
                                `carmakeyear` varchar(63) DEFAULT NULL,
                                `caringname` varchar(63) DEFAULT NULL,
                                `carcard` varchar(63) DEFAULT NULL,
                                `cargood` varchar(63) DEFAULT NULL,
                                `checkstate` varchar(63) DEFAULT NULL,
                                `carmiantain` varchar(63) DEFAULT NULL,
                                `carlabel` varchar(127) DEFAULT NULL,
                                `dealtype` varchar(63) DEFAULT NULL,
                                `carinvoice` varchar(63) DEFAULT NULL,
                                `accident` varchar(63) DEFAULT NULL,
                                `useage` varchar(63) DEFAULT NULL,
                                `telphone` varchar(63) DEFAULT NULL,
                                `dealor` varchar(127) DEFAULT NULL,
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
                                 PRIMARY KEY  (`id`)
                              ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
    params['mysqltable'] = 'ttpai_test'
    # params['mysqltable']=params['website']
    # params['mysqlip']="192.168.1.92"
    # params['mysqluser']="root"
    # params['mysqlpasswd']="Datauser@2016"
    # params['mysqldbname']="usedcar"
    # params['mysqlport']=3306

    #mongo redefine
    # params['mongocoll']=params['website']
    # params['mongoip']="192.168.1.92"
    # params['mongoport']=27071
    # params['mongodbname']="usedcar"

    #df redefine
    # params['bfrate']=0.001
    # params['keycol']="statusplus"

    #carinfocreate redefine
    # params['carinfocreate'] = False
    #counts redefine
    # params['counts']=0
    #size redefine
    # params['savesize']=1000
    return params

def parse_original(item):
    #caritem init
    caritem = dict()
    # keyinfro
    caritem['website'] = item['website']
    caritem['carid'] = (re.findall('\d+', item["url"].split('.')[-2]))
    caritem['url'] = item["url"]
    caritem['grabtime'] = item["grabtime"]
    caritem['pagetime'] = item["pagetime"]  # new
    caritem['parsetime'] = time.strftime('%Y-%m-%d %X', time.localtime())
    caritem['posttime'] =item["grabtime"]
    # status
    caritem['status'] = str(re.findall('sale|sold', item["status"])[0])
    caritem['statusplus'] = item["status"]
    return caritem

def parse_keyinfo(dom):
    # caritem init
    caritem = dict()
    # keyinfro
    caritem['pagetitle'] = dom.xpath('//title/text()').extract_first().strip() if dom.xpath('//title/text()') else "-"  # new
    caritem['title'] =dom.xpath('//h1[@class="un-title"]/text()').extract_first().strip() \
        if dom.xpath('//h1[@class="un-title"]/text()') else "-"
    caritem['price1']=''.join(dom.xpath('//strong[@class="s-orange"]/text()').re('\d+\.?\d*')) \
        if dom.xpath('//strong[@class="s-orange"]/text()') else "-"
    return caritem

def parse_baseinfo(dom):
    # caritem init
    caritem = dict()
    # baseinfo
    caritem['registerdate']="-".join(dom.xpath('//span/i[@class="icon icon-clock"]/../text()').re('\d+'))+"-01" \
        if dom.xpath('//span/i[@class="icon icon-clock"]/../text()') else "-"
    caritem['mileage']=''.join(dom.xpath('//span/i[@class="icon icon-stopwatch"]/../text()').re('\d+\.?\d*'))
    caritem['geartype'] = dom.xpath(u'//dl/dt[contains(text(),"\u6392\u6321")]/following-sibling::*/text()').extract_first() \
        if dom.xpath(u'//dl/dt[contains(text(),"\u6392\u6321")]/following-sibling::*/text()') else "-"
    caritem['region'] = "-"
    caritem['dealplace'] ="-"
    caritem['province'] = "-"
    caritem['city'] = dom.xpath('//span/i[@class="icon icon-address"]/../text()').extract()[1].strip() \
        if dom.xpath('//span/i[@class="icon icon-address"]/../text()') else "-"
    caritem['changetimes'] = dom.xpath(u'//tr/th[contains(text(),"\u8fc7\u6237\u6b21\u6570")]/following-sibling::*/text()').extract_first() \
        if dom.xpath(u'//tr/th[contains(text(),"\u8fc7\u6237\u6b21\u6570")]/following-sibling::*/text()') else "-"
    caritem['changedate'] = dom.xpath(u'//tr/th[contains(text(),"\u8fc7\u6237\u65e5\u671f")]/following-sibling::*/text()').extract_first() \
        if dom.xpath(u'//tr/th[contains(text(),"\u8fc7\u6237\u65e5\u671f")]/following-sibling::*/text()') else "-"
    caritem['years'] = "-"
    return caritem

def parse_certification(dom):
    # caritem init
    caritem = dict()
    # citification
    caritem['yearchecktime']=dom.xpath(u'//dl/dt[contains(text(),"\u5e74\u68c0\u6709\u6548\u671f")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//dl/dt[contains(text(),"\u5e74\u68c0\u6709\u6548\u671f")]/following-sibling::*/text()') else "-"
    caritem['Insurance1']=dom.xpath(u'//dl/dt[contains(text(),"\u4ea4\u5f3a\u9669\u4fdd\u5355")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//dl/dt[contains(text(),"\u4ea4\u5f3a\u9669\u4fdd\u5355")]/following-sibling::*/text()') else "-"
    caritem['Insurance2'] ="-"
    caritem['licence']=dom.xpath(u'//dl/dt[contains(text(),"\u73b0\u6709\u8f66\u724c")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//dl/dt[contains(text(),"\u73b0\u6709\u8f66\u724c")]/following-sibling::*/text()') else "-"
    caritem['first_owner']=dom.xpath(u'//dl/dt[contains(text(),"\u662f\u5426\u4e00\u624b\u8f66")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//dl/dt[contains(text(),"\u662f\u5426\u4e00\u624b\u8f66")]/following-sibling::*/text()') else "-"
    caritem['produceyear']=dom.xpath(u'//tr/th[contains(text(),"\u51fa\u5382\u65e5\u671f")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//tr/th[contains(text(),"\u51fa\u5382\u65e5\u671f")]/following-sibling::*/text()') else "-"
    caritem['carinvoice'] = "-"
    caritem['accident'] = "-"  # new
    caritem['useage'] = dom.xpath(u'//dl/dt[contains(text(),"\u4f7f\u7528\u6027\u8d28")]/following-sibling::*/text()').extract_first().strip() \
        if dom.xpath(u'//dl/dt[contains(text(),"\u4f7f\u7528\u6027\u8d28")]/following-sibling::*/text()') else "-"

    return caritem

def parse_dealor(dom):
    # caritem init
    caritem = dict()
    # dealer
    caritem['telphone'] = dom.xpath('//div[@class="main_tel"]/p/strong/text()').extract_first() \
        if dom.xpath('//div[@class="main_tel"]/p/strong/text()') else "-"
    caritem['dealor'] = "-"
    caritem['dealtype']=dom.xpath('//span[@class="badge" or @class="badge badge-orange"]/text()').extract_first() \
        if dom.xpath('//span[@class="badge" or @class="badge badge-orange"]/text()') else "-"



    return caritem

def parse_carinfo1(dom):
    # caritem init
    caritem = dict()
    # carinfo
    caritem['brand_name'] =dom.xpath('//div[@class="left"]/a[4]/text()').extract_first().split(u'\u4e8c\u624b')[-1] \
        if dom.xpath('//div[@class="left"]/a[4]/text()') \
        else dom.xpath('//div[@class="bread pn1 mt20f"]/a[4]/text()').extract_first().split(u'\u4e8c\u624b')[-1] \
            if dom.xpath('//div[@class="bread pn1 mt20f"]/a[4]/text()') else "-"
    caritem['class_name'] =dom.xpath('//div[@class="left"]/a[5]/text()').extract_first().split(u'\u4e8c\u624b')[-1] \
        if dom.xpath('//div[@class="left"]/a[5]/text()') \
        else dom.xpath('//div[@class="bread pn1 mt20f"]/a[5]/text()').extract_first().split(u'\u4e8c\u624b')[-1] \
            if dom.xpath('//div[@class="bread pn1 mt20f"]/a[5]/text()') else "-"

    caritem['gear'] ="-"
    caritem['emission'] =dom.xpath('//li[@class="last"]/dl/dd/strong/text()').extract_first() \
        if dom.xpath('//li[@class="last"]/dl/dd/strong/text()') \
        else dom.xpath(u'//div[contains(text(),"\u6392\u653e\u6807\u51c6")]/following-sibling::*/text()').extract_first() \
            if dom.xpath(u'//div[contains(text(),"\u6392\u653e\u6807\u51c6")]/following-sibling::*/text()') else "-"
    caritem['color'] =dom.xpath(u'//li/label[contains(text(),"\u8f66\u8eab\u989c\u8272")]/../text()').extract_first() \
        if dom.xpath(u'//li/label[contains(text(),"\u8f66\u8eab\u989c\u8272")]/../text()').extract_first() else "-"
    caritem['body'] =dom.xpath(u'//li/label[contains(text(),"\u8f66\u8eab\u7ed3\u6784")]/../text()').extract_first()\
        if dom.xpath(u'//li/label[contains(text(),"\u8f66\u8eab\u7ed3\u6784")]/../text()') else "-"

    caritem['guideprice'] =''.join(dom.xpath('//span[@class="parti"]/strong[1]/text()').re('\d+\.?\d*')) \
        if dom.xpath('//span[@class="parti"]/strong[1]/text()') \
        else '.'.join(dom.xpath('//div[@class="price_area"]/p[2]/strong[1]/text()').re('\d+\.?\d*')) \
            if dom.xpath('//div[@class="price_area"]/p[2]/strong[1]/text()') else "-"

    caritem['guidepricetax'] =''.join(dom.xpath('//span[@class="parti"]/strong[2]/text()').re('\d+\.?\d*')) \
        if  dom.xpath('//span[@class="parti"]/strong[2]/text()') \
        else '.'.join(dom.xpath('//div[@class="price_area"]/p[2]/strong[2]/text()').re('\d+\.?\d*')) \
            if dom.xpath('//div[@class="price_area"]/p[2]/strong[2]/text()') else "-"

    caritem['newcartitle'] = "-"
    caritem['newcarurl'] = '-'
    return caritem

def parse_desc( dom):
    # caritem init
    caritem = dict()
    # more desc
    caritem['desc'] = dom.xpath('//div[@class="consul-reco"]/div[@class="con"]/p/text()').extract_first() \
        if dom.xpath('//div[@class="consul-reco"]/div[@class="con"]/p/text()') \
        else dom.xpath('//div[@class="con_rec"]/div[@class="sub_content"]/p/text()').extract_first() \
            if dom.xpath('//div[@class="con_rec"]/div[@class="sub_content"]/p/text()') else "-"
    if len(caritem['desc'])>551:
        caritem['desc']=caritem['desc'][0:551]

    caritem['img_url'] =dom.xpath('//li[@id="big-pic-1"]/img/@src').extract_first() \
        if dom.xpath('//li[@id="big-pic-1"]/img/@src') \
        else dom.xpath('//div[@class="car-photo"]/div[@class="bd"]/ul/li[1]/img/@data-src').extract_first() \
            if dom.xpath('//div[@class="car-photo"]/div[@class="bd"]/ul/li[1]/img/@data-src') else "-"
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
    try:
        counts +=1
        #parse original:1
        # caritem init
        # parse original:1
        caritem = parse_original(item)
        # parse keyinfo:2
        content = item['datasave'][1]
        dom = scrapy.selector.Selector(text=content)
        # if dom.xpath(u'//div[@class="tips_shelfl"]/strong[contains(text(),"\u975e\u5e38\u62b1\u6b49\uff0c\u8be5\u8f66\u8f86\u5df2\u4e0b\u67b6")]'):
        #     continue
        caritem = dict(caritem, **parse_keyinfo(dom))
        caritem = dict(caritem, **parse_baseinfo(dom))
        caritem = dict(caritem, **parse_certification(dom))
        caritem = dict(caritem, **parse_dealor(dom))
        caritem = dict(caritem, **parse_carinfo1(dom))
        caritem = dict(caritem, **parse_desc(dom))

        #add
        caritems.append(caritem)
        #save to sql
        caritems=savecar(caritems,mysqltable,mysqldb,savesize)
    except:
         try:
             #save exception
             print str(counts)+":" + i["url"]+", parse error."
             saveerror(counts,i['url'],website,mysqldb)
         except:
             pass
        # else:
        #     print "item duplicated!"
    #final save
    savecarfinal(caritems,mysqltable,mysqldb,savesize)
    conclose(mysqldb,mysqldbc)
    return "One group finish"



#parse(0,100)
# ppexcut(8)






