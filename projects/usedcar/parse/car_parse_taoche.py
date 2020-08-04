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
    website ='taoche'
    params =ParseInit(website)
    #mysql redefine
    params['createsql']="""CREATE TABLE IF NOT EXISTS `taoche` (
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
                                `status` varchar(63) DEFAULT NULL,
                                `statusplus` varchar(127) DEFAULT NULL,
                                `makeyear` varchar(63) DEFAULT NULL,
                                `registerdate` varchar(63) DEFAULT NULL,
                                `years` varchar(63) DEFAULT NULL,
                                `mileage` varchar(63) DEFAULT NULL,
                                `mileperage` varchar(63) DEFAULT NULL,
                                `province` varchar(63) DEFAULT NULL,
                                `city` varchar(63) DEFAULT NULL,
                                `region` varchar(63) DEFAULT NULL,
                                `dealplace` varchar(63) DEFAULT NULL,
                                `registerplace` varchar(63) DEFAULT NULL,
                                `changetimes` varchar(63) DEFAULT NULL,
                                `changedate` varchar(63) DEFAULT NULL,
                                `Insurance1` varchar(63) DEFAULT NULL,
                                `Insurance2` varchar(63) DEFAULT NULL,
                                `yearchecktime` varchar(63) DEFAULT NULL,
                                `check_insurancedesc` varchar(63) DEFAULT NULL,
                                `carokcf` varchar(63) DEFAULT NULL,
                                `carcard` varchar(63) DEFAULT NULL,
                                `carinvoice` varchar(63) DEFAULT NULL,
                                `accident` varchar(63) DEFAULT NULL,
                                `useage` varchar(63) DEFAULT NULL,
                                `telphone` varchar(63) DEFAULT NULL,
                                `dealor` varchar(127) DEFAULT NULL,
                                `brand_name` varchar(63) DEFAULT NULL,
                                `class_name` varchar(63) DEFAULT NULL,
                                `brand` varchar(63) DEFAULT NULL,
                                `series` varchar(63) DEFAULT NULL,
                                `source` varchar(63) DEFAULT NULL,
                                `guideprice` varchar(63) DEFAULT NULL,
                                `guidepricetax` varchar(63) DEFAULT NULL,
                                `tax` varchar(63) DEFAULT NULL,
                                `newcarid` varchar(127) DEFAULT NULL,
                                `geartype` varchar(63) DEFAULT NULL,
                                `output` varchar(63) DEFAULT NULL,
                                `level` varchar(63) DEFAULT NULL,
                                `motorps` varchar(63) DEFAULT NULL,
                                `driveway` varchar(63) DEFAULT NULL,
                                `lengthwh` varchar(63) DEFAULT NULL,
                                `length` varchar(63) DEFAULT NULL,
                                `width` varchar(63) DEFAULT NULL,
                                `height` varchar(63) DEFAULT NULL,
                                `petrol` varchar(63) DEFAULT NULL,
                                `body` varchar(63) DEFAULT NULL,
                                `doors` varchar(63) DEFAULT NULL,
                                `seats` varchar(63) DEFAULT NULL,
                                `bodystyle` varchar(63) DEFAULT NULL,
                                `luggage` varchar(63) DEFAULT NULL,
                                `img_url` varchar(255) DEFAULT NULL,
                                `desc` varchar(511) DEFAULT NULL,
                                PRIMARY KEY  (`id`)
                              ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
    params['mysqltable']='taoche'
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
    caritem['carid'] = str(re.findall('\d+', item["url"])[0])
    caritem['url'] = item["url"]
    caritem['grabtime'] = item["grabtime"]
    caritem['pagetime'] = item["pagetime"]  # new
    caritem['parsetime'] = time.strftime('%Y-%m-%d %X', time.localtime())
    # status
    caritem['status'] = str(re.findall('sale|sold', item["status"])[0])
    caritem['statusplus'] = item["status"]
    #print caritem['url']
    return caritem

def parse_keyinfo(dom):
    # caritem init
    caritem = dict()
    # keyinfro
    caritem['pagetitle'] = dom.xpath('//title/text()').extract_first()  # new
    caritem['title'] = dom.xpath('//div[@class="taoche-details-tit padding-rit0"]/h3/text()').extract_first().strip() \
        if dom.xpath('//div[@class="taoche-details-tit padding-rit0"]/h3/text()') else '-'
    caritem['price1'] = '.'.join(dom.xpath('//div[@class="taoche-details-price"]/strong/text()').re('\d+')) \
        if dom.xpath('//div[@class="taoche-details-price"]/strong/text()') else "-"
    caritem['makeyear'] = re.findall('\d+' + u'\u6b3e' + '|' + u'\u5e74', caritem['title'])[0] \
        if re.findall('\d+' + u'\u6b3e' + '|' + u'\u5e74', caritem['title']) else '-'
    caritem['makeyear'] = re.findall('\d+', caritem['makeyear'])[0] \
        if re.findall('\d+', caritem['makeyear']) else '-'
    return caritem

def parse_baseinfo(dom):
    # caritem init
    caritem = dict()
    # baseinfo
    caritem['registerdate'] =  re.compile(u'\u6708').sub('',re.compile(u'\u5e74').sub('-',''.join(dom.xpath(
            u'//div[@class="row taoche-details-parameter "]/div/p[contains(text(),"\u4e0a\u724c\u65f6\u95f4")]/../text()').extract()).strip()))+"-01" \
        if dom.xpath(u'//div[@class="row taoche-details-parameter "]/div/p[contains(text(),"\u4e0a\u724c\u65f6\u95f4")]/../text()') else "-"
    caritem['years'] = ''.join(dom.xpath(
            u'//div[@class="col-xs-6 information-text"]/p[contains(text(),"\u884c\u9a76\u65f6\u95f4")]/../text()').extract()).strip() \
        if dom.xpath(u'//div[@class="col-xs-6 information-text"]/p[contains(text(),"\u884c\u9a76\u65f6\u95f4")]/../text()') else "-"  # new
    caritem['mileage'] = re.compile(u'\u4e07\u516c\u91cc').sub('',''.join(dom.xpath(
            u'//div[@class="row taoche-details-parameter "]/div/p[contains(text(),"\u884c\u9a76\u91cc\u7a0b")]/../text()').extract()).strip()) \
        if dom.xpath(u'//div[@class="row taoche-details-parameter "]/div/p[contains(text(),"\u884c\u9a76\u91cc\u7a0b")]/../text()') else "-"
    caritem['mileperage'] = "-"  # new
    caritem['geartype'] = ''.join(dom.xpath(
            u'//div[@class="row taoche-details-parameter "]/div/p[contains(text(),"\u53d8\u901f\u7bb1")]/../text()').extract()).strip().replace('/','') \
        if dom.xpath(u'//div[@class="row taoche-details-parameter "]/div/p[contains(text(),"\u53d8\u901f\u7bb1")]/../text()') else "-"
    caritem['region'] = ''.join(dom.xpath(
            u'//div[@class="col-xs-6 information-text"]/p[contains(text(),"\u6240\u5728\u5730")]/../text()').extract()).strip() \
        if dom.xpath(u'//div[@class="col-xs-6 information-text"]/p[contains(text(),"\u6240\u5728\u5730")]/../text()') else "-"
    caritem['province'] = dom.xpath('//meta[@name="location"]/@content').extract_first().split(';')[0].split('=')[1] \
        if dom.xpath('//meta[@name="location"]/@content') else "zero"
    caritem['city'] = dom.xpath('//meta[@name="location"]/@content').extract_first().split(';')[1].split('=')[1] \
        if dom.xpath('//meta[@name="location"]/@content') else "-"
    caritem['dealplace'] = ''.join(dom.xpath(
            u'//div[@class="row taoche-details-parameter "]/div/p[contains(text(),"\u9500\u552e\u57ce\u5e02")]/../text()').extract()).strip() \
        if dom.xpath(u'//div[@class="row taoche-details-parameter "]/div/p[contains(text(),"\u9500\u552e\u57ce\u5e02")]/../text()') else "-"
    caritem['registerplace'] = dom.xpath(
        u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text(),"\u724c\u7167\u6240\u5728\u5730")]/span/a/text()').extract_first().strip() \
        if dom.xpath(u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text(),"\u724c\u7167\u6240\u5728\u5730")]/span/a/text()') else "-"
    caritem['changetimes'] = "-"
    caritem['changedate'] = "-"
    return caritem

def parse_certification(dom):
    # caritem init
    caritem = dict()
    # citification
    caritem['Insurance1'] = re.compile(u'\u6708').sub('',re.compile(u'\u5e74').sub('-',''.join(dom.xpath(
            u'//div[@class="col-xs-6 information-text"]/p[contains(text(),"\u4fdd\u9669\u5230\u671f\u65e5")]/../text()').extract()).strip())) \
        if dom.xpath(u'//div[@class="col-xs-6 information-text"]/p[contains(text(),"\u4fdd\u9669\u5230\u671f\u65e5")]/../text()') else "-"
    caritem['Insurance2'] = "-"
    caritem['yearchecktime'] = re.compile(u'\u6708').sub('',re.compile(u'\u5e74').sub('-',''.join(dom.xpath(
            u'//div[@class="col-xs-6 information-text"]/p[contains(text(),"\u5e74\u68c0\u5230\u671f\u65e5")]/../text()').extract()).strip())) \
        if dom.xpath(u'//div[@class="col-xs-6 information-text"]/p[contains(text(),"\u5e74\u68c0\u5230\u671f\u65e5")]/../text()') else "-"
    caritem['carokcf'] = "-"
    caritem['carcard'] = "-"
    caritem['carinvoice'] = "-"
    caritem['accident'] = "-"  # new
    caritem['useage'] = ''.join(dom.xpath(
            u'//div[@class="col-xs-6 information-text"]/p[contains(text(),"\u4f7f\u7528\u7c7b\u578b")]/../text()').extract()).strip() \
        if dom.xpath(u'//div[@class="col-xs-6 information-text"]/p[contains(text(),"\u4f7f\u7528\u7c7b\u578b")]/../text()') else "-"  # new
    caritem['check_insurancedesc'] = ''.join(dom.xpath(
            u'//div[@class="col-xs-3 details-information-main"]/div/strong[contains(text(),"\u5e74\u68c0")]/text()').extract()).strip() \
        if dom.xpath(u'//div[@class="col-xs-3 details-information-main"]/div/strong[contains(text(),"\u5e74\u68c0")]/text()') else "-"  # new
    return caritem

def parse_dealor(dom):
    # caritem init
    caritem = dict()
    # dealer
    caritem['telphone'] = "-"
    caritem['dealor'] = "-"  # new
    '''
    caritem['dealortype'] = u"\u4e2a\u4eba" \
        if caritem['dealor'].find(u"\u4e2a\u4eba") != -1 else  u"\u8f66\u5546" \
        if caritem['dealor'].find(u"\u8f66\u5546") != -1 else "-"  # new
    caritem['dealorcompany'] = dom.xpath('//div[@class="certdl-det"]/p/b/text()').extract_first() \
        if dom.xpath('//div[@class="certdl-det"]/p/b/text()') else "-"  # new
    caritem['dealorlocation'] = dom.xpath('//ul[@class="vc-dealer"]/li/p/text()').extract_first() \
        if dom.xpath('//ul[@class="vc-dealer"]/li/p/text()') else "-"  # new
    '''
    return caritem

def parse_createinfo(dom,carinfocreate,website,mysqldb):
    '''
    cartitle = dom.xpath('//li[@class ="li01"]/p')
    if bool(cartitle) and carinfocreate == True:
        # carinfo create
        j1 = 0
        carinfocreate = False
        carinfors = []
        for j in range(0, len(cartitle)):
            if cartitle[j].xpath('text()'):
                ii = dict()
                ii = {"carinfo_en": "carinfo" + str(j1),
                      "carinfo_cn": cartitle[j].xpath('text()').extract_first()}
                carinfors.append(ii)
                j1 += 1
        carinforsdf = pandas.DataFrame(carinfors)
        carinforsdf.to_sql(name=website + '_carinfo', con=mysqldb, flavor='mysql',
                           if_exists='replace')
    '''

def parse_carinfo2(dom):
    # caritem init
    caritem = dict()
    #bug
    caritem['brand'] = dom.xpath(
        u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text()[2],"\u54c1\u724c\u578b\u53f7")]/span/a/text()').extract()[0] \
        if len(dom.xpath(u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text()[2],"\u54c1\u724c\u578b\u53f7")]/span/a/text()'))>=1 else "-"
    #bug
    caritem['series'] = dom.xpath(
        u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text()[2],"\u54c1\u724c\u578b\u53f7")]/span/a/text()').extract()[1] \
        if len(dom.xpath(u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text()[2],"\u54c1\u724c\u578b\u53f7")]/span/a/text()'))>=2 else "-"
    caritem['source'] = dom.xpath(
        u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text(),"\u8f66\u8f86\u6765\u6e90")]/span/text()').extract_first().strip() \
        if dom.xpath(u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text(),"\u8f66\u8f86\u6765\u6e90")]/span/text()') else "-"
    caritem['motorps'] = re.compile(u'\u9a6c\u529b').sub('',dom.xpath(
        u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text(),"\u53d1\u52a8\u673a")]/span/text()').extract_first().strip()) \
        if dom.xpath(u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text(),"\u53d1\u52a8\u673a")]/span/text()') else "-"
    caritem['driveway'] = dom.xpath(
        u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text(),"\u9a71\u52a8\u65b9\u5f0f")]/span/text()').extract_first().strip() \
        if dom.xpath(u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text(),"\u9a71\u52a8\u65b9\u5f0f")]/span/text()') else "-"
    caritem['level'] = dom.xpath(
        u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text()[2],"\u8f66\u8f86\u7ea7\u522b")]/span/a/text()').extract_first().strip() \
        if dom.xpath(u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text()[2],"\u8f66\u8f86\u7ea7\u522b")]/span/a/text()') else "-"
    caritem['petrol'] = dom.xpath(
        u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text(),"\u6cb9\u8017")]/span/text()').extract_first().strip() \
        if dom.xpath(u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text(),"\u6cb9\u8017")]/span/text()') else "-"
    caritem['lengthwh'] = dom.xpath(u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text(),"\u957f\u5bbd\u9ad8")]/span/text()').extract_first().strip() \
        if dom.xpath(u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text(),"\u957f\u5bbd\u9ad8")]/span/text()') else "-"
    if caritem['lengthwh']=="-":
        caritem['length'] = "-"
        caritem['width'] = "-"
        caritem['height'] = "-"
    #bug
    elif len(caritem['lengthwh'].split('*'))>=3:
        caritem['length'] = re.compile('mm').sub('',caritem['lengthwh'].split('*')[0])
        caritem['width'] = re.compile('mm').sub('',caritem['lengthwh'].split('*')[1])
        caritem['height'] = re.compile('mm').sub('',caritem['lengthwh'].split('*')[2])
    caritem['body'] = dom.xpath(
        u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text(),"\u8f66\u8eab\u7c7b\u578b")]/span/text()').extract_first().strip() \
        if dom.xpath(u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text(),"\u8f66\u8eab\u7c7b\u578b")]/span/text()') else "-"
    if caritem['body']=="- -":
         caritem['doors'] = "-"
         caritem['seats'] = "-"
         caritem['bodystyle'] = "-"
    else:
         caritem['doors'] = dom.xpath(u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text(),"\u8f66\u8eab\u7c7b\u578b")]/span/text()').extract_first().strip().split(u'\u95e8')[0] \
            if len(dom.xpath(u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text(),"\u8f66\u8eab\u7c7b\u578b")]/span/text()').extract_first().strip().split(u'\u95e8')) > 1 else "-"
         caritem['seats'] = dom.xpath(u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text(),"\u8f66\u8eab\u7c7b\u578b")]/span/text()').extract_first().strip().split(u'\u5ea7')[0][-1] \
            if len(dom.xpath(u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text(),"\u8f66\u8eab\u7c7b\u578b")]/span/text()').extract_first().strip().split(u'\u5ea7')) > 1 else "-"
         caritem['bodystyle'] = dom.xpath(u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text(),"\u8f66\u8eab\u7c7b\u578b")]/span/text()').extract_first().strip().split(u'\u53a2')[0][-1] + u'\u53a2' \
            if len(dom.xpath(u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text(),"\u8f66\u8eab\u7c7b\u578b")]/span/text()').extract_first().strip().split(u'\u53a2')) > 1 else "-"
    caritem['luggage'] = dom.xpath(
        u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text(),"\u540e\u5907\u7bb1\u5bb9\u79ef")]/span/text()').extract_first().strip() \
        if dom.xpath(u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text(),"\u540e\u5907\u7bb1\u5bb9\u79ef")]/span/text()') else "-"
    return caritem
def parse_carinfo1(dom):
    # caritem init
    caritem = dict()
    # carinfo
    title=','.join(dom.xpath('//div[@class="crumbs"]/a/text()').extract()).split(',')
    if len(title)>=3:
        if title[-2]:
            brandlocation = title[-2].find(u'\u4e8c\u624b')
        if title[-1]:
            classlocation = title[-1].find(u'\u4e8c\u624b')
        caritem['brand_name'] = title[-2][brandlocation + 2:] \
            if brandlocation!=-1 else "-"
        caritem['class_name'] = title[-1][classlocation+2:] \
            if classlocation!=-1 else "-"
    caritem['output'] = '.'.join(dom.xpath(
        u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text(),"\u6392\u91cf")]/span/a/text()').re('\d+')) \
        if dom.xpath(u'//div[@class="row parameter-configure margin-md"]/div/ul/li[contains(text(),"\u6392\u91cf")]/span/a/text()') else "-"
    '''
    caritem['gear'] = ''.join(dom.xpath(
            u'//div[@class="row taoche-details-parameter "]/div/p[contains(text(),"\u53d8\u901f\u7bb1")]/../text()').extract()).strip().replace('/','') \
        if dom.xpath(u'//div[@class="row taoche-details-parameter "]/div/p[contains(text(),"\u53d8\u901f\u7bb1")]/../text()') else "-"
    caritem['emission'] = \
        dom.xpath(u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u6392\u653e\u6807\u51c6")]/../text()').extract()[1].strip() \
            if dom.xpath(u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u6392\u653e\u6807\u51c6")]/../text()') else "-"
    caritem['color'] = dom.xpath(
        u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u8f66\u8eab\u989c\u8272")]/../text()').extract_first() \
        if dom.xpath(u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u8f66\u8eab\u989c\u8272")]/../text()') else "-"  # new
    '''
    if re.search(u'\u4e0d\u8be6',dom.xpath('//div[@class="taoche-details-pricebox "]/p/span/text()').extract_first().strip()) > 0:	
        caritem['guidepricetax'] = "0"
        caritem['tax'] = "0"
    else:
        caritem['guidepricetax'] = '.'.join(re.findall('\d+',dom.xpath('//div[@class="taoche-details-pricebox "]/p/span[1]/text()').extract_first().split(u'\uff08')[0])) \
            if dom.xpath('//div[@class="taoche-details-pricebox "]/p/span[1]/text()') else "0"
        caritem['tax'] = '.'.join(re.findall('\d+',dom.xpath('//div[@class="taoche-details-pricebox "]/p/span[1]/text()').extract_first().split(u'\uff08')[1])) \
            if dom.xpath('//div[@class="taoche-details-pricebox "]/p/span[1]/text()') else "0"
    caritem['guideprice'] = float(caritem['guidepricetax'])-float(caritem['tax'])
    '''
    caritem['newcartitle'] = "".join(dom.xpath('//p[@class="pz-param-title"]/text()').extract()).strip() \
        if dom.xpath('//p[@class="pz-param-title"]/text()') else "-"  # new
    num1 = dom.xpath('//p[@class="pz-param-title"]').extract_first().find('http') \
        if dom.xpath('//p[@class="pz-param-title"]') else 0
    num2 = dom.xpath('//p[@class="pz-param-title"]').extract_first().find('target') \
        if dom.xpath('//p[@class="pz-param-title"]') else 100
    '''
    caritem['newcarid'] = dom.xpath('//input[@id="hidCarId"]/@value').extract_first() \
        if dom.xpath('//input[@id="hidCarId"]/@value') else '-'  # new
    return caritem

def parse_otherinfo(dom):
    # caritem init
    caritem = dict()
    '''
    cartitle = dom.xpath('//li[@class ="li01"]/p')
    carinfo = dom.xpath('//li[@class ="li02"]')
    if cartitle:
        # carother infor
        j = 0
        j1 = 0
        for car in carinfo:
            if cartitle[j].xpath('text()'):
                caritem["carinfo" + str(j1)] = car.xpath('text()').extract_first() if car.xpath('text()') else '-'
                j1 += 1
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
    caritem['accidentdesc'] = "-".join(checkdesc) \
        if checkdesc else "-"
    '''
    return caritem

def parse_desc( dom):
    # caritem init
    caritem = dict()
    # emoji_pattern = re.compile("["
    #     u"\U0001F600-\U0001F64F"
    #     u"\U0001F300-\U0001F5FF"
    #     u"\U0001F680-\U0001F6FF"
    #     u"\U0001F1E0-\U0001F1FF"
    #                        "]+", flags=re.UNICODE)
    # more desc
    caritem['desc'] = dom.xpath('//div[@class="margin-md  readme "]/text()').extract_first().strip().encode('gbk','ignore').decode('gbk','ignore') \
        if dom.xpath('//div[@class="margin-md  readme "]/text()') else "-"  # new
    if len(caritem['desc']) > 500:
        caritem['desc'] = caritem['desc'][:500]
    caritem['img_url'] = dom.xpath('//div[@class="taoche-details-piclist-box"]/ul/li/img[@class="zoom_img"]/@src').extract_first() \
        if dom.xpath('//div[@class="taoche-details-piclist-box"]/ul/li/img[@class="zoom_img"]/@src') else "-"  # new
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
        counts +=1
        print counts
        # logging.log(msg="counts:"+str(counts)+','+i['url'], level=logging.INFO)
        #parse original:1
        # caritem init
        # parse original:1
        caritem = parse_original(i)
        # parse keyinfo:2
        content= item['datasave'][1]
        dom = scrapy.selector.Selector(text=content)
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
        caritems=savecar(caritems,mysqltable,mysqldb,savesize)
            #     except:
            #          try:
            #              #save exception
            #              print str(counts)+":" + i["url"]+", parse error."
            #              # logging.log(msg="counts:" + str(counts) + ',' + i['url']+", parse error.", level=logging.ERROR)
            #              saveerror(counts,i['url'],website,mysqldb)
            #              continue
            #          except:
            #              pass
            # else:
            #     print "item duplicated!"
                # logging.log(msg="counts:" + str(counts) + ',' + i['url'] + ", item duplicated!", level=logging.WARNING)
        #final save
    except:
        pass
    savecarfinal(caritems,mysqltable,mysqldb,savesize)
    conclose(mysqldb,mysqldbc)
    # logging.log(msg="counts:" + str(counts) + ',' + ", One group finish!", level=logging.INFO)
    return "One group finish"



#parse(0,200)

# ppexcut(8)






