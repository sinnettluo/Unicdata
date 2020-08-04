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
    website ='youche'
    params =ParseInit(website)
    #mysql redefine
    params['createsql']="""CREATE TABLE IF NOT EXISTS `youche_new` (
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
                                `province` varchar(63) DEFAULT NULL,
                                `city` varchar(63) DEFAULT NULL,
                                `region` varchar(63) DEFAULT NULL,
                                `dealtype` varchar(250) DEFAULT NULL,
                                `dealplace` varchar(250) DEFAULT NULL,
                                `changetimes` varchar(63) DEFAULT NULL,
                                `changedate` varchar(63) DEFAULT NULL,
                                `Insurance1` varchar(63) DEFAULT NULL,
                                `Insurance2` varchar(63) DEFAULT NULL,
                                `yearchecktime` varchar(63) DEFAULT NULL,
                                `carokcf` varchar(63) DEFAULT NULL,
                                `carcard` varchar(63) DEFAULT NULL,
                                `carproduct` varchar(63) DEFAULT NULL,
                                `carprecedure` varchar(63) DEFAULT NULL,
                                `carbearing` varchar(63) DEFAULT NULL,
                                `carstate` varchar(63) DEFAULT NULL,
                                `carinvoice` varchar(63) DEFAULT NULL,
                                `accident` varchar(63) DEFAULT NULL,
                                `useage` varchar(63) DEFAULT NULL,
                                `telphone` varchar(63) DEFAULT NULL,
                                `dealor` varchar(127) DEFAULT NULL,
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
                                 `carinfo0` varchar(127) DEFAULT NULL,
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
                                 `carinfo50` varchar(127) DEFAULT NULL,
                                 `carinfo51` varchar(127) DEFAULT NULL,
                                 `carinfo52` varchar(127) DEFAULT NULL,
                                 `carinfo53` varchar(127) DEFAULT NULL,
                                 `carinfo54` varchar(127) DEFAULT NULL,
                                 `carinfo55` varchar(127) DEFAULT NULL,
                                 `carinfo56` varchar(127) DEFAULT NULL,
                                 `carinfo57` varchar(127) DEFAULT NULL,
                                 `carinfo58` varchar(127) DEFAULT NULL,
                                 `carinfo59` varchar(127) DEFAULT NULL,
                                 `carinfo60` varchar(127) DEFAULT NULL,
                                 `carinfo61` varchar(127) DEFAULT NULL,
                                 PRIMARY KEY  (`id`)
                              ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
    params['mysqltable']='youche_new'
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
    caritem['status'] = str(re.findall('sale|sold', item["status"])[0])  # ？
    caritem['statusplus'] = item["status"]
    return caritem


def parse_keyinfo(dom):
    # caritem init
    caritem = dict()
    # keyinfro
    caritem['pagetitle'] = dom.xpath('//title/text()').extract_first() if dom.xpath('//title/text()') else "-"  # new
    caritem['title'] =dom.xpath('//div[@class="carTitleInfo"]/h1/text()').extract_first() \
        if dom.xpath('//div[@class="carTitleInfo"]/h1/text()') else "-"
    caritem['price1'] = dom.xpath('//div[@class="newCarPrice"]/span[2]/text()').extract_first() \
        if dom.xpath('//div[@class="newCarPrice"]/span[2]/text()') else "-"
    caritem['pricetag'] = "-"
    caritem['guideprice']=dom.xpath('//div[@class="oldCarPrice"]/s/text()').extract_first() \
        if dom.xpath('//div[@class="oldCarPrice"]/s/text()') else "-"

    caritem['guidepricetax']="-"
    return caritem


def parse_baseinfo(dom):
    # caritem init
    caritem = dict()
    # baseinfo
    caritem['registerdate'] =( '-'.join(dom.xpath('//div[@class="carTextList"]/span[1]/text()').re('\d+'))+"-"+"1") \
        if dom.xpath('//div[@class="carTextList"]/span[1]/text()') else "-"
    caritem['posttime'] ="-"
    caritem['years'] = "-"
    caritem['mileage'] = '.'.join(dom.xpath('//div[@class="carTextList"]/span[2]/text()').re('\d+\.?\d*')) \
        if dom.xpath('//div[@class="carTextList"]/span[2]/text()') else "-"
    caritem['gear']="-"
    caritem['region'] = "-"
    caritem['province'] = "-"
    caritem['city'] = dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u5f52\u5c5e\u5730")]/following-sibling::*/text()').extract_first() \
        if dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u5f52\u5c5e\u5730")]/following-sibling::*/text()') else "-"
    caritem['changetimes'] =''.join(dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u8fc7\u6237\u6b21\u6570")]/following-sibling::*/text()').re('\d+')) \
        if dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u8fc7\u6237\u6b21\u6570")]/following-sibling::*/text()') else "-"
    caritem['changedate'] = "-"
    caritem['luggage']="-"
    return caritem


def parse_certification(dom):
    # caritem init
    caritem = dict()
    # citification
    caritem['Insurance1'] = dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u4ea4\u5f3a\u9669\u65e5\u671f")]/following-sibling::*/text()').extract_first() \
        if dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u4ea4\u5f3a\u9669\u65e5\u671f")]/following-sibling::*/text()') else "-"
    caritem['Insurance2'] = "-"
    caritem['yearchecktime'] = dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u5e74\u68c0\u6709\u6548\u671f\u81f3")]/following-sibling::*/text()').extract_first()\
        if dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u5e74\u68c0\u6709\u6548\u671f\u81f3")]/following-sibling::*/text()') else "-"
    caritem['carokcf'] = "-"
    caritem['carcard'] = "-"
    caritem['carinvoice'] = "-"
    caritem['accident'] = "-"
    caritem['useage'] = "-"
    return caritem


def parse_dealor(dom):
    # caritem init
    caritem = dict()
    # dealer
    caritem['telphone'] = dom.xpath('//span[@class="changeTel"]/text()').extract_first() \
        if dom.xpath('//span[@class="changeTel"]/text()') else "-"
    caritem['dealor'] = dom.xpath('//div[@class="adCarStore"]/div[@class="top"]/span[@class="sp02"]/text()').extract_first() \
        if dom.xpath('//div[@class="adCarStore"]/div[@class="top"]/span[@class="sp02"]/text()') else "-"
    if caritem['dealor']=="-" or caritem['dealor']=="":
        caritem['dealtype']=u'\u4e2a\u4eba'
    else:
        caritem['dealtype']=u'\u5546\u4eba'
    if caritem['dealor']==u'\u4ea6\u5e84\u5e97':
        caritem['dealplace']=u'\u5317\u4eac\u4ea6\u5e84\u7ecf\u6d4e\u6280\u672f\u5f00\u53d1\u533a\u79d1\u521b\u516d\u885795\u53f7'
    elif caritem['dealor']==u'\u5305\u5934\u5e97':
        caritem['dealplace']=u'\u5185\u8499\u53e4\u5305\u5934\u5e02110\u56fd\u9053\u4e0e\u6c11\u65cf\u4e1c\u8def\u8def\u53e3'
    elif caritem['dealor']==u'\u5929\u6d25\u5e97':
        caritem['dealplace']=u'\u5929\u6d25\u5e02\u897f\u9752\u533a\u5349\u5eb7\u90538\u53f7'
    elif caritem['dealor']==u'\u6765\u5e7f\u8425\u5e97':
        caritem['dealplace']=u'\u5317\u4eac\u5e02\u671d\u9633\u533a\u6765\u5e7f\u8425\u65b0\u5317\u8def\u75328\u53f7'
    else:
        caritem['dealplace']="-"
    return caritem


def parse_createinfo(dom, carinfocreate, website, mysqldb):
    caritem =dict()
    mycarinfo=[]
    l_mys = dom.xpath('//div[@class="peiziBox"]/table/tbody/tr/td/b/text()')
    for sel in l_mys:
         l_info=(sel.extract()).strip()
         mycarinfo.append(l_info)
    if bool(l_mys) and carinfocreate == True:
        # carinfo create
        j = 0
        carinfocreate = False
        carinfors = []
        ii = dict()
        for i in range(0, len(mycarinfo)-1):
            ii = {"carinfo_en": "carinfo" + str(j),
                      "carinfo_cn": mycarinfo[i]}
            carinfors.append(ii)
            j += 1
        carinforsdf = pandas.DataFrame(carinfors)
        carinforsdf.to_sql(name=website + '_carinfo', con=mysqldb, flavor='mysql',
                           if_exists='replace')



def parse_carinfo2(dom):
    # caritem init
    caritem = dict()

    return caritem


def parse_carinfo1(dom):
    # caritem init
    caritem = dict()
    # carinfo
    caritem['brand_name'] =dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u54c1\u724c")]/following-sibling::*/a/text()').extract_first() \
        if dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u54c1\u724c")]/following-sibling::*/a/text()') else "-"
    caritem['class_name'] = dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u8f66\u7cfb")]/following-sibling::*/a/text()').extract_first() \
        if dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u8f66\u7cfb")]/following-sibling::*/a/text()') else "-"
    caritem['output']=''.join(dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u6392\u91cf")]/following-sibling::*/text()').re('\d+\.?\d*'))\
        if dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u6392\u91cf")]/following-sibling::*/text()') else "-"
    caritem['geartype'] =dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u53d8\u901f\u7bb1")]/following-sibling::*/text()').extract_first() \
        if dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u53d8\u901f\u7bb1")]/following-sibling::*/text()') else "-"
    caritem['emission'] = dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u6392\u653e\u6807\u51c6")]/following-sibling::*/text()').extract_first() \
        if dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u6392\u653e\u6807\u51c6")]/following-sibling::*/text()') else "-"
    caritem['color'] = dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u989c\u8272")]/following-sibling::*/text()').extract_first() \
        if dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u989c\u8272")]/following-sibling::*/text()') else "-"
    caritem['carproduct']=dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u4ea7\u5730")]/following-sibling::*/text()').extract_first() \
        if dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u4ea7\u5730")]/following-sibling::*/text()') else "-"
    caritem['carprecedure']=dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u624b\u7eed")]/following-sibling::*/text()').extract_first() \
        if dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u624b\u7eed")]/following-sibling::*/text()') else "-"
    caritem['carbearing']=''.join(dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u8f7d\u5ba2\u6570")]/following-sibling::*/text()').re('\d+')) \
        if dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u8f7d\u5ba2\u6570")]/following-sibling::*/text()') else "-"
    caritem['carstate']=dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u8f66\u51b5")]/following-sibling::*/text()').extract_first() \
        if dom.xpath(u'//ul[@class="carfiles"]/li/span[contains(text(),"\u8f66\u51b5")]/following-sibling::*/text()') else "-"
    caritem['body'] = "-"
    caritem['newcartitle'] = "-"  # new
    caritem['newcarurl'] = '-'  # new
    return caritem


def parse_otherinfo(dom):
    # caritem init
    caritem = dict()
    mycarinfo=[]
    l_mys = dom.xpath('//div[@class="peiziBox"]/table/tbody/tr/td[not(b)]/text()')
    for sel in l_mys:
        l_info=(sel.extract())
        mycarinfo.append(l_info)
    if bool(l_mys) :
        # carinfo create
        j = 0
        for i in range(0, len(mycarinfo)):
            caritem["carinfo" + str(j)] = mycarinfo[i]
            j += 1
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
    caritem['desc'] = dom.xpath('//div[@ class="xiaoBTT"]/p/text()').extract_first() if dom.xpath('//div[@ class="xiaoBTT"]/p/text()') else "-"
    caritem['img_url'] = dom.xpath('//div[@class="one"]/div[@class="img"]/img/@src').extract_first() \
        if dom.xpath('//div[@class="one"]/div[@class="img"]/img/@src').extract_first() else "-"
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
        parse_createinfo(dom,carinfocreate,website,mysqldb)
        # parse carinfo:7
        caritem = dict(caritem, **parse_carinfo2(dom))
        caritem = dict(caritem, **parse_carinfo1(dom))
        caritem = dict(caritem, **parse_otherinfo(dom))
        # parse checkpoints:8
        # caritem = dict(caritem, **parse_checkpoints(dom))
        # parse desc:9
        caritem = dict(caritem, **parse_desc(dom))

        # add
        caritems.append(caritem)
        # save to sql
        caritems = savecar(caritems, savesize, website, mysqldb)
            #     except:
            #         try:
            #             # save exception
            #             print str(counts) + ":" + i["url"] + ", parse error."
            #             saveerror(counts, i['url'], website, mysqldb)
            #             continue
            #         except:
            #             pass
            # else:
            #     print "item duplicated!"
        # final save
    except:
        pass
    savecarfinal(caritems,mysqltable,mysqldb,savesize)
    conclose(mysqldb,mysqldbc)
    return "One group finish"

#parse(0, 200)
#ppexcut(8)






