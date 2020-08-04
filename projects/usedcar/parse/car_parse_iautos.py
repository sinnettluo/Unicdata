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
    website ='iautos'
    params =ParseInit(website)
    #mysql redefine
    params['createsql']="""CREATE TABLE IF NOT EXISTS `iautos` (
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
                                `brand_name` varchar(63) DEFAULT NULL,
                                `class_name` varchar(63) DEFAULT NULL,
                                `guideprice` varchar(63) DEFAULT NULL,
                                `tax` varchar(63) DEFAULT NULL,
                                `guidepricetax` varchar(63) DEFAULT NULL,
                                `newcartitle` varchar(127) DEFAULT NULL,
                                `newcarurl` varchar(127) DEFAULT NULL,
                                `body` varchar(63) DEFAULT NULL,
                                `level` varchar(63) DEFAULT NULL,
                                `motor` varchar(63) DEFAULT NULL,
                                `motorps` varchar(63) DEFAULT NULL,
                                `driveway` varchar(63) DEFAULT NULL,
                                `nm` varchar(63) DEFAULT NULL,
                                `lengthwh` varchar(63) DEFAULT NULL,
                                `length` varchar(63) DEFAULT NULL,
                                `width` varchar(63) DEFAULT NULL,
                                `height` varchar(63) DEFAULT NULL,
                                `petrol` varchar(63) DEFAULT NULL,
                                `wheelbase` varchar(63) DEFAULT NULL,
                                `fueltype` varchar(63) DEFAULT NULL,
                                `geartype` varchar(63) DEFAULT NULL,
                                `emission` varchar(63) DEFAULT NULL,
                                `output` varchar(63) DEFAULT NULL,
                                `brandid` varchar(63) DEFAULT NULL,
                                `seriesid` varchar(63) DEFAULT NULL,
                                `factoryid` varchar(63) DEFAULT NULL,
                                `modelid` varchar(63) DEFAULT NULL,
                                `desc` varchar(511) DEFAULT NULL,
                                `img_url` varchar(511) DEFAULT NULL,
                                PRIMARY KEY  (`id`)
                              ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
    params['mysqltable']='iautos'
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
    return caritem

def parse_keyinfo(dom):
    # caritem init
    caritem = dict()
    # keyinfro
    caritem['pagetitle'] = dom.xpath('//title/text()').extract_first()  # new
    caritem['title'] = dom.xpath('//h2[@class="title de-drei-col"]/span/text()').extract_first().strip() \
        if dom.xpath('//h2[@class="title de-drei-col"]/span/text()') else '-'
    caritem['price1'] = dom.xpath('//div[@class="price clean"]/div/span/strong/text()').extract_first() \
        if dom.xpath('//div[@class="price clean"]/div/span/strong/text()') else "-"
    caritem['makeyear'] = re.compile(u'\u6b3e').sub('',re.findall('\d+'+u'\u6b3e'+'|'+u'\u5e74',caritem['title'])[0]) \
        if re.findall('\d+'+u'\u6b3e'+'|'+u'\u5e74',caritem['title']) else "-"
    return caritem

def parse_baseinfo(dom):
    # caritem init
    caritem = dict()
    # baseinfo
    caritem['registerdate'] = dom.xpath(u'//ul[@class="others clean"]/li/h6[contains(text(),"\u9996\u6b21\u4e0a\u724c")]/../p/text()').extract_first() \
        if dom.xpath(u'//ul[@class="others clean"]/li/h6[contains(text(),"\u9996\u6b21\u4e0a\u724c")]/../p/text()') else "-"
    caritem['years'] = "-"  # new
    caritem['mileage'] = re.compile(u'\u4e07\u516c\u91cc').sub('',dom.xpath(u'//ul[@class="others clean"]/li/h6[contains(text(),"\u91cc\u7a0b")]/../p/text()').extract_first()) \
        if dom.xpath(u'//ul[@class="others clean"]/li/h6[contains(text(),"\u91cc\u7a0b")]/../p/text()') else "-"
    caritem['mileperage'] = "-"  # new
    caritem['geartype'] = dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-l"]/tbody/tr/th[contains(text(),"\u53d8\u901f\u7bb1")]/../td/text()').extract_first() \
        if dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-l"]/tbody/tr/th[contains(text(),"\u53d8\u901f\u7bb1")]/../td/text()') else "-"
    caritem['region'] = dom.xpath('//input[@id="carArea"]/@value').extract_first() \
        if dom.xpath('//input[@id="carArea"]/@value') else "-"
    caritem['province'] = dom.xpath('//meta[@name="location"]/@content').extract_first().split(';')[0].split('=')[1] \
        if dom.xpath('//meta[@name="location"]/@content') else "zero"
    caritem['city'] = dom.xpath('//meta[@name="location"]/@content').extract_first().split(';')[1].split('=')[1] \
        if dom.xpath('//meta[@name="location"]/@content') else "-"
    caritem['dealplace'] = dom.xpath(u'//ul[@class="others clean"]/li/h6[contains(text(),"\u6240\u5728\u5730")]/../p/text()').extract_first() \
        if dom.xpath(u'//ul[@class="others clean"]/li/h6[contains(text(),"\u6240\u5728\u5730")]/../p/text()') else "-"
    caritem['changetimes'] = "-"
    caritem['changedate'] = "-"
    return caritem

def parse_certification(dom):
    # caritem init
    caritem = dict()
    # citification
    caritem['Insurance1'] = "-"
    caritem['Insurance2'] = "-"
    caritem['yearchecktime'] = "-"
    caritem['carokcf'] = "-"
    caritem['carcard'] = "-"
    caritem['carinvoice'] = "-"
    caritem['accident'] = "-"  # new
    caritem['useage'] = dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-l"]/tbody/tr/th[contains(text(),"\u4f7f\u7528\u6027\u8d28")]/../td/text()').extract_first() \
        if dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-l"]/tbody/tr/th[contains(text(),"\u4f7f\u7528\u6027\u8d28")]/../td/text()') else "-"  # new
    return caritem

def parse_dealor(dom):
    # caritem init
    caritem = dict()
    # dealer
    caritem['telphone'] = dom.xpath('//div[@class="num de-btn-ico single"]/span/text()').extract_first() \
        if dom.xpath('//div[@class="num de-btn-ico single"]/span/text()') else "-"
    caritem['dealor'] = dom.xpath('//div[@class="address"]/span/i/text()').extract_first() \
        if dom.xpath('//div[@class="address"]/span/i/text()') else "-"    # new
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
    caritem['driveway'] = dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-l"]/tbody/tr/th[contains(text(),"\u9a71\u52a8\u65b9\u5f0f")]/../td/text()').extract_first() \
        if dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-l"]/tbody/tr/th[contains(text(),"\u9a71\u52a8\u65b9\u5f0f")]/../td/text()') else "-"
    caritem['motor'] = dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-l"]/tbody/tr/th[contains(text(),"\u53d1\u52a8\u673a")]/../td/text()').extract_first() \
        if dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-l"]/tbody/tr/th[contains(text(),"\u53d1\u52a8\u673a")]/../td/text()') else "-"
    caritem['motorps'] = re.compile(u'\u9a6c\u529b'+'.+').sub('',dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-r"]/tbody/tr/th[contains(text(),"\u53d1\u52a8\u673a\u529f\u7387")]/../td/text()').extract_first()) \
        if dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-r"]/tbody/tr/th[contains(text(),"\u53d1\u52a8\u673a\u529f\u7387")]/../td/text()') else "-"
    caritem['nm'] = re.compile('\s|N-m').sub('',dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-r"]/tbody/tr/th[contains(text(),"\u626d\u77e9")]/../td/text()').extract_first()) \
        if dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-r"]/tbody/tr/th[contains(text(),"\u626d\u77e9")]/../td/text()') else "-"
    caritem['lengthwh'] = dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-r"]/tbody/tr/th[contains(text(),"\u957f\u5bbd\u9ad8")]/../td/text()').extract_first() \
        if dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-r"]/tbody/tr/th[contains(text(),"\u957f\u5bbd\u9ad8")]/../td/text()') else "-"
    if caritem['lengthwh']=="- -" or caritem['lengthwh']=="-":
        caritem['length'] = "-"
        caritem['width'] = "-"
        caritem['height'] = "-"
    elif len(caritem['lengthwh'].split('*'))>=3:
        caritem['length'] = caritem['lengthwh'].split('*')[0]
        caritem['width'] = caritem['lengthwh'].split('*')[1]
        caritem['height'] = caritem['lengthwh'].split('*')[2]
    caritem['wheelbase'] = re.compile('\s|mm').sub('',dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-r"]/tbody/tr/th[contains(text(),"\u8f74\u8ddd")]/../td/text()').extract_first()) \
        if dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-r"]/tbody/tr/th[contains(text(),"\u8f74\u8ddd")]/../td/text()') else "-"
    caritem['petrol'] = dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-r"]/tbody/tr/th[contains(text(),"\u5b98\u65b9\u8017\u6cb9")]/../td/text()').extract_first() \
        if dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-r"]/tbody/tr/th[contains(text(),"\u5b98\u65b9\u8017\u6cb9")]/../td/text()') else "-"
    caritem['fueltype'] = dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-r"]/tbody/tr/th[contains(text(),"\u71c3\u6599\u7c7b\u578b")]/../td/text()').extract_first() \
        if dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-r"]/tbody/tr/th[contains(text(),"\u71c3\u6599\u7c7b\u578b")]/../td/text()') else "-"
    caritem['level'] = dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-l"]/tbody/tr/th[contains(text(),"\u8f66\u8f86\u7ea7\u522b")]/../td/text()').extract_first() \
        if dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-l"]/tbody/tr/th[contains(text(),"\u8f66\u8f86\u7ea7\u522b")]/../td/text()') else "-"
    return caritem

def parse_carinfo1(dom):
    # caritem init
    caritem = dict()
    # carinfo
    title=','.join(dom.xpath('//div[@class="bread-crumbs de-twelve-font"]/a/text()').extract()).split(',')
    if len(title)>=3:
        if title[-1]:
            brandlocation = title[-1].find(u'\u4e8c\u624b')
    caritem['brand_name'] = title[-1][brandlocation + 2:] \
            if brandlocation!=-1 else "-"
    caritem['class_name'] = dom.xpath('//input[@id="seriesName"]/@value').extract_first() \
        if dom.xpath('//input[@id="seriesName"]/@value') else "-"
    caritem['brand_name'] = re.compile(caritem['class_name']).sub('',caritem['brand_name'])
    caritem['output'] = '.'.join(dom.xpath(u'//ul[@class="others clean"]/li/h6[contains(text(),"\u6392\u91cf")]/../p/text()').re('\d+')) \
        if dom.xpath(u'//ul[@class="others clean"]/li/h6[contains(text(),"\u6392\u91cf")]/../p/text()') else "-"
    caritem['emission'] = dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-l"]/tbody/tr/th[contains(text(),"\u73af\u4fdd\u6807\u51c6")]/../td/text()').extract_first() \
        if dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-l"]/tbody/tr/th[contains(text(),"\u73af\u4fdd\u6807\u51c6")]/../td/text()') else "-"
    caritem['color'] = dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-l"]/tbody/tr/th[contains(text(),"\u989c\u8272")]/../td/text()').extract_first() \
        if dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-l"]/tbody/tr/th[contains(text(),"\u989c\u8272")]/../td/text()') else "-"  # new
    caritem['body'] = re.compile(u'\u8f66').sub('',dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-r"]/tbody/tr/th[contains(text(),"\u8f66\u8eab\u7ed3\u6784")]/../td/text()').extract_first()) \
        if dom.xpath(u'//div[@class="table-wrap clean"]/table[@class="table-r"]/tbody/tr/th[contains(text(),"\u8f66\u8eab\u7ed3\u6784")]/../td/text()') else "-"
    caritem['guideprice'] = dom.xpath('//span[@class="original-price de-circul-corn"]/i/text()').extract()[0] \
        if dom.xpath('//span[@class="original-price de-circul-corn"]/i/text()') else "-"
    caritem['tax'] = dom.xpath('//span[@class="original-price de-circul-corn"]/i/text()').extract()[1] \
        if dom.xpath('//span[@class="original-price de-circul-corn"]/i/text()') else "-"
    caritem['guidepricetax'] = dom.xpath('//span[@class="original-price de-circul-corn"]/i/text()').extract()[2] \
        if dom.xpath('//span[@class="original-price de-circul-corn"]/i/text()') else "-"
    caritem['brandid'] = dom.xpath('//input[@id="brandId"]/@value').extract_first() \
        if dom.xpath('//input[@id="brandId"]/@value') else "-"  # new
    caritem['seriesid'] = dom.xpath('//input[@id="seriesId"]/@value').extract_first() \
        if dom.xpath('//input[@id="seriesId"]/@value') else "-"  # new
    caritem['factoryid'] = dom.xpath('//input[@id="mfrsId"]/@value').extract_first() \
        if dom.xpath('//input[@id="mfrsId"]/@value') else "-"  # new
    caritem['modelid'] = dom.xpath('//input[@id="modelId"]/@value').extract_first() \
        if dom.xpath('//input[@id="modelId"]/@value') else "-"  # new
    caritem['newcartitle'] = "-"  # new
    caritem['newcarurl'] = '-'  # new
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

def parse_desc(dom):
    # caritem init
    caritem = dict()
    # more desc
    caritem['desc'] = "-"  # new
    caritem['img_url'] = dom.xpath('//div[@class="header-main clean"]/div/a/img[@class="de-circul-corn"]/@src').extract_first() \
        if dom.xpath('//div[@class="header-main clean"]/div/a/img[@class="de-circul-corn"]/@src') else "-"  # new
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
        # counts +=1
        # print counts
        # logging.log(msg="counts:"+str(counts)+','+i['url'], level=logging.INFO)
        #parse original:1
        # caritem init
        # parse original:1
        caritem = parse_original(item)
        # parse keyinfo:2
        content = item['datasave'][1]
        dom = scrapy.selector.Selector(text=content)
        # if dom.xpath('//div[@class="sold-main"]'):
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


#parse(0,100)
# ppexcut(8)







