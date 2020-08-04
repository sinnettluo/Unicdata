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
    website ='ganji'
    params =ParseInit(website)
    #mysql redefine
    params['createsql']= """CREATE TABLE IF NOT EXISTS `ganji` (
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
                                    `dealortype` varchar(127) DEFAULT NULL,
                                    `dealorcompany` varchar(127) DEFAULT NULL,
                                    `dealorlocation` varchar(127) DEFAULT NULL,
                                    `brand_name` varchar(63) DEFAULT NULL,
                                    `class_name` varchar(63) DEFAULT NULL,
                                    `guideprice` varchar(63) DEFAULT NULL,
                                    `guidepricetax` varchar(63) DEFAULT NULL,
                                    `newcartitle` varchar(127) DEFAULT NULL,
                                    `newcarurl` varchar(127) DEFAULT NULL,
                                    `geartype` varchar(63) DEFAULT NULL,
                                    `emission` varchar(63) DEFAULT NULL,
                                    `level` varchar(63) DEFAULT NULL,
                                    `motor` varchar(63) DEFAULT NULL,
                                    `gear` varchar(63) DEFAULT NULL,
                                    `lengthwh` varchar(63) DEFAULT NULL,
                                    `wheel` varchar(63) DEFAULT NULL,
                                    `body` varchar(63) DEFAULT NULL,
                                    `weight` varchar(63) DEFAULT NULL,
                                    `luggage` varchar(63) DEFAULT NULL,
                                    `motortype` varchar(63) DEFAULT NULL,
                                    `output` varchar(63) DEFAULT NULL,
                                    `method` varchar(63) DEFAULT NULL,
                                    `cylinders` varchar(63) DEFAULT NULL,
                                    `compression` varchar(63) DEFAULT NULL,
                                    `ps` varchar(63) DEFAULT NULL,
                                    `Nm` varchar(63) DEFAULT NULL,
                                    `carinfo0` varchar(63) DEFAULT NULL,
                                    `carinfo1` varchar(63) DEFAULT NULL,
                                    `carinfo2` varchar(63) DEFAULT NULL,
                                    `carinfo3` varchar(63) DEFAULT NULL,
                                    `carinfo4` varchar(63) DEFAULT NULL,
                                    `carinfo5` varchar(63) DEFAULT NULL,
                                    `carinfo6` varchar(63) DEFAULT NULL,
                                    `carinfo7` varchar(63) DEFAULT NULL,
                                    `carinfo8` varchar(63) DEFAULT NULL,
                                    `carinfo9` varchar(63) DEFAULT NULL,
                                    `carinfo10` varchar(63) DEFAULT NULL,
                                    `carinfo11` varchar(63) DEFAULT NULL,
                                    `carinfo12` varchar(63) DEFAULT NULL,
                                    `carinfo13` varchar(63) DEFAULT NULL,
                                    `carinfo14` varchar(63) DEFAULT NULL,
                                    `carinfo15` varchar(63) DEFAULT NULL,
                                    `carinfo16` varchar(63) DEFAULT NULL,
                                    `carinfo17` varchar(63) DEFAULT NULL,
                                    `carinfo18` varchar(63) DEFAULT NULL,
                                    `carinfo19` varchar(63) DEFAULT NULL,
                                    `carinfo20` varchar(63) DEFAULT NULL,
                                    `carinfo21` varchar(63) DEFAULT NULL,
                                    `carinfo22` varchar(63) DEFAULT NULL,
                                    `carinfo23` varchar(63) DEFAULT NULL,
                                    `carinfo24` varchar(127) DEFAULT NULL,
                                    `carinfo25` varchar(63) DEFAULT NULL,
                                    `carinfo26` varchar(63) DEFAULT NULL,
                                    `carinfo27` varchar(63) DEFAULT NULL,
                                    `carinfo28` varchar(63) DEFAULT NULL,
                                    `carinfo29` varchar(63) DEFAULT NULL,
                                    `carinfo30` varchar(63) DEFAULT NULL,
                                    `carinfo31` varchar(63) DEFAULT NULL,
                                    `carinfo32` varchar(63) DEFAULT NULL,
                                    `carinfo33` varchar(63) DEFAULT NULL,
                                    `carinfo34` varchar(63) DEFAULT NULL,
                                    `carinfo35` varchar(63) DEFAULT NULL,
                                    `carinfo36` varchar(63) DEFAULT NULL,
                                    `carinfo37` varchar(63) DEFAULT NULL,
                                    `carinfo38` varchar(63) DEFAULT NULL,
                                    `carinfo39` varchar(63) DEFAULT NULL,
                                    `totalcheck` varchar(511) DEFAULT NULL,
                                    `accidentscore` double DEFAULT NULL,
                                    `accidentdesc` varchar(255) DEFAULT NULL,
                                    `outerscore` double DEFAULT NULL,
                                    `outerdesc` varchar(127) DEFAULT NULL,
                                    `innerscore` double DEFAULT NULL,
                                    `innerdesc` varchar(127) DEFAULT NULL,
                                    `safescore` double DEFAULT NULL,
                                    `safedesc` varchar(127) DEFAULT NULL,
                                    `roadscore` double DEFAULT NULL,
                                    `roaddesc` varchar(127) DEFAULT NULL,
                                    `desc` varchar(511) DEFAULT NULL,
                                    `img_url` varchar(255) DEFAULT NULL,
                                PRIMARY KEY  (`id`)
                              ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
    params['mysqltable']='ganji'
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
    status = 'sale'
    caritem['status'] = status
    caritem['statusplus'] = item["status"]
    return caritem

def parse_keyinfo(dom):
    # caritem init
    caritem = dict()
    # keyinfro
    caritem['pagetitle'] = dom.xpath('//title/text()').extract_first()  # new
    caritem['title'] = dom.xpath('//h1[@class="title-name"]/text()').extract_first().strip() if dom.xpath(
        '//h1[@class="title-name"]/text()') else '-'
    caritem['price1'] = dom.xpath('//i[@class="arial fc-org f20"]/text()').extract_first() \
        if dom.xpath('//i[@class="arial fc-org f20"]/text()') else "-"
    return caritem

def parse_baseinfo(dom):
    # caritem init
    caritem = dict()
    # baseinfo
    caritem['registerdate'] = dom.xpath('//li[@class="iNew-yeah"]/div/i/text()').extract_first() \
        if dom.xpath('//li[@class="iNew-yeah"]/div/i/text()') else "-"
    caritem['years'] = dom.xpath('//li[@class="iNew-yeah"]/span/i/text()').extract_first() \
        if dom.xpath('//li[@class="iNew-yeah"]/span/i/text()') else "-"  # new
    caritem['mileage'] = dom.xpath('//li[@class="iNew-km"]/span/i/text()').extract_first() \
        if dom.xpath('//li[@class="iNew-km"]/span/i/text()') else "-"
    caritem['mileperage'] = dom.xpath('//li[@class="iNew-km"]/div/i/text()').extract_first() \
        if dom.xpath('//li[@class="iNew-km"]/div/i/text()') else "-"  # new
    caritem['geartype'] = dom.xpath(u'//label[contains(text(),"\u53d8 \u901f \u7bb1")]/../text()').extract_first() \
        if dom.xpath(u'//label[contains(text(),"\u53d8 \u901f \u7bb1")]/../text()') else "-"
    caritem['region'] = "-"
    caritem['province'] = dom.xpath('//meta[@name="location"]/@content').extract_first().split(';')[0].split('=')[1] \
        if dom.xpath('//meta[@name="location"]/@content') else "zero"
    caritem['city'] = dom.xpath('//meta[@name="location"]/@content').extract_first().split(';')[1].split('=')[1] \
        if dom.xpath('//meta[@name="location"]/@content') else "-"
    caritem['dealplace'] = "-"
    caritem['changetimes'] = dom.xpath('//li[@class="iNew-hu"]/span/i/text()').extract_first() \
        if dom.xpath('//li[@class="iNew-hu"]/span/i/text()') else "-"
    caritem['changedate'] = "-"
    return caritem

def parse_certification(dom):
    # caritem init
    caritem = dict()
    # citification
    caritem['Insurance1'] = dom.xpath(
        u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u4ea4\u5f3a\u9669\u5230\u671f")]/../text()').extract_first() \
        if dom.xpath(u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u4ea4\u5f3a\u9669\u5230\u671f")]/../text()') else "-"
    caritem['Insurance2'] = dom.xpath(
        u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u5546\u4e1a\u9669")]/../text()').extract_first() \
        if dom.xpath(u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u5546\u4e1a\u9669")]/../text()') else "-"
    caritem['yearchecktime'] = dom.xpath(
        u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u5e74\u68c0\u5230\u671f")]/../text()').extract_first() \
        if dom.xpath(u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u5e74\u68c0\u5230\u671f")]/../text()') else "-"
    caritem['carokcf'] = "-"
    caritem['carcard'] = "-"
    caritem['carinvoice'] = "-"
    caritem['accident'] = dom.xpath(
        u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u4e8b\u6545\u60c5\u51b5")]/../text()').extract_first() \
        if dom.xpath(u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u4e8b\u6545\u60c5\u51b5")]/../text()') else "-"  # new
    caritem['useage'] = dom.xpath(
        u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u4f7f\u7528\u6027\u8d28")]/../text()').extract_first() \
        if dom.xpath(u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u4f7f\u7528\u6027\u8d28")]/../text()') else "-"  # new
    return caritem

def parse_dealor(dom):
    # caritem init
    caritem = dict()
    # dealer
    caritem['telphone'] = dom.xpath('//span[@class="telephone"]/text()').extract_first() \
        if dom.xpath('//span[@class="telephone"]/text()') else "-"
    caritem['dealor'] = dom.xpath('//p[@class="v-p2"]/text()').extract_first().strip().strip('\n').replace(' ', '') \
        if dom.xpath('//p[@class="v-p2"]/text()') else "-"  # new
    caritem['dealortype'] = u"\u4e2a\u4eba" \
        if caritem['dealor'].find(u"\u4e2a\u4eba") != -1 else  u"\u8f66\u5546" \
        if caritem['dealor'].find(u"\u8f66\u5546") != -1 else "-"  # new
    caritem['dealorcompany'] = dom.xpath('//div[@class="certdl-det"]/p/b/text()').extract_first() \
        if dom.xpath('//div[@class="certdl-det"]/p/b/text()') else "-"  # new
    caritem['dealorlocation'] = dom.xpath('//ul[@class="vc-dealer"]/li/p/text()').extract_first() \
        if dom.xpath('//ul[@class="vc-dealer"]/li/p/text()') else "-"  # new
    return caritem

def parse_createinfo(dom,carinfocreate,website,mysqldb):
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

def parse_carinfo2(dom):
    # caritem init
    caritem = dict()
    cartitle = dom.xpath('//li[@class ="li01"]/p')
    carinfo = dom.xpath('//li[@class ="li02"]')
    if cartitle:
        names = ['level', 'motor', 'lengthwh', 'wheel', 'weight', 'luggage', 'motortype',
                 'method', 'cylinders', 'compression', 'ps', 'Nm', ]
        j = 0
        for name in names:
            caritem[name] = '-'
        j = 0
        for car in cartitle:
            ii = carinfo[j].xpath('text()').extract_first() if carinfo[j].xpath('text()') else '-'
            if car.xpath('text()'):
                if car.xpath('text()').extract_first().find(u'\u957f/\u5bbd/\u9ad8') != -1:
                    caritem['lengthwh'] = ii
                elif car.xpath('text()').extract_first().find(u'\u884c\u674e\u7bb1\u5bb9\u79ef') != -1:
                    caritem['luggage'] = ii
                elif car.xpath('text()').extract_first().find(u'\u8f74\u8ddd') != -1:
                    caritem['wheel'] = ii
                elif car.xpath('text()').extract_first().find(u'\u6700\u5927\u626d\u77e9') != -1:
                    caritem['Nm'] = ii
                elif car.xpath('text()').extract_first().find(u'\u6574\u8f66\u6574\u5907\u8d28\u91cf') != -1:
                    caritem['weight'] = ii
                elif car.xpath('text()').extract_first().find(u'\u6c7d\u7f38\u6570') != -1:
                    caritem['cylinders'] = ii
            j += 1
    return caritem
def parse_carinfo1(dom):
    # caritem init
    caritem = dict()
    # carinfo
    pagetitle=dom.xpath('//title/text()').extract_first()
    if len(pagetitle.split(u'\u3011'))>=2:
        if len(pagetitle.split(u'\u3011')[1].split('/'))>=2:
            brandlocation = pagetitle.split(u'\u3011')[1].split('/')[0].find(u'\u4e8c\u624b')
            classlocation = pagetitle.split(u'\u3011')[1].split('/')[1].find(u'\u4e8c\u624b')
            if brandlocation!=-1 and classlocation!=-1:
                caritem['brand_name'] = pagetitle.split(u'\u3011')[1].split('/')[0][brandlocation + 2:]
                caritem['class_name'] = pagetitle.split(u'\u3011')[1].split('/')[1][:classlocation]
    caritem['output'] = dom.xpath(
        u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u6392 \u6c14 \u91cf")]/../text()').extract_first() \
        if dom.xpath(u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u6392 \u6c14 \u91cf")]/../text()') else "-"
    caritem['gear'] = dom.xpath(
        u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u53d8 \u901f \u7bb1")]/../text()').extract_first() \
        if dom.xpath(u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u53d8 \u901f \u7bb1")]/../text()') else "-"
    caritem['emission'] = \
        dom.xpath(u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u6392\u653e\u6807\u51c6")]/../text()').extract()[1].strip() \
            if dom.xpath(u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u6392\u653e\u6807\u51c6")]/../text()') else "-"
    caritem['color'] = dom.xpath(
        u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u8f66\u8eab\u989c\u8272")]/../text()').extract_first() \
        if dom.xpath(u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u8f66\u8eab\u989c\u8272")]/../text()') else "-"  # new
    caritem['body'] = dom.xpath(
        u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u8f66\u8eab\u7ed3\u6784")]/../text()').extract_first() \
        if dom.xpath(u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u8f66\u8eab\u7ed3\u6784")]/../text()') else "-"
    caritem['guideprice'] = str(
        dom.xpath(u'//p/span[contains(text(),"\u65b0\u8f66\u4ef7")]/../span[2]/i[1]/text()').extract_first()) \
        if dom.xpath(u'//p/span[contains(text(),"\u65b0\u8f66\u4ef7")]/../span[2]/i[1]/text()') else "0"
    caritem['guidepricetax'] = "0" if caritem['guideprice'] == "0" else \
        str(dom.xpath(u'//p/span[contains(text(),"\u65b0\u8f66\u4ef7")]/../span[2]/i[2]/text()').extract_first()) + str(
            caritem['guideprice'])
    caritem['newcartitle'] = "".join(dom.xpath('//p[@class="pz-param-title"]/text()').extract()).strip() \
        if dom.xpath('//p[@class="pz-param-title"]/text()') else "-"  # new
    num1 = dom.xpath('//p[@class="pz-param-title"]').extract_first().find('http') \
        if dom.xpath('//p[@class="pz-param-title"]') else 0
    num2 = dom.xpath('//p[@class="pz-param-title"]').extract_first().find('target') \
        if dom.xpath('//p[@class="pz-param-title"]') else 100
    caritem['newcarurl'] = dom.xpath('//p[@class="pz-param-title"]').extract_first()[num1:(num2 - 2)] \
        if dom.xpath('//p[@class="pz-param-title"]') else '-'  # new
    return caritem

def parse_otherinfo(dom):
    # caritem init
    caritem = dict()
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
    return caritem

def parse_checkpoints(dom):
    # caritem init
    caritem = dict()
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
    return caritem

def parse_desc(dom):
    # caritem init
    caritem = dict()
    # more desc
    caritem['desc'] = "-".join(dom.xpath('//div[@class="det-detinfor"]/div[1]/p/text()').extract()).strip().strip(
        '\n').replace(' ', '') \
        if dom.xpath('//div[@class="det-detinfor"]/div[1]/p/text()') else "-"  # new
    if len(caritem['desc']) > 500:
        caritem['desc'] = caritem['desc'][:500]
    caritem['img_url'] = dom.xpath('//img[@data-role="img"]/@src').extract_first() \
        if dom.xpath('//img[@data-role="img"]/@src') else "-"  # new
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
    #
    # for i in collection.find().skip(start).limit(step):
    #     returndf=bloom_check(i['status'],df)
    #     if not returndf:
    #
    #          try:
    try:
        # counts +=1
        # print counts
        #parse original:1
        # caritem init
        # parse original:1
        caritem = parse_original(item)
        # parse keyinfo:2
        content = item['datasave'][1]
        dom = scrapy.selector.Selector(text=content)
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
        caritem = dict(caritem, **parse_carinfo1(dom))
        caritem = dict(caritem, **parse_carinfo2(dom))
        caritem = dict(caritem, **parse_otherinfo(dom))
        # parse checkpoints:8
        caritem = dict(caritem, **parse_checkpoints(dom))
        # parse desc:9
        caritem = dict(caritem, **parse_desc(dom))
        #add
        caritems.append(caritem)
        #save to sql
        caritems=savecar(caritems,mysqltable,mysqldb,savesize)
            #     except Exception, e:
            #         try:
            #             #save exception
            #             print str(counts)+":" + i["url"]+", parse error."
            #             saveerror(counts,i['url'],website,mysqldb)
            #             continue
            #         except:
            #             pass
            # else:
            #     print "item duplicated!"
    except:
        pass
    #final save
    savecarfinal(caritems,mysqltable,mysqldb,savesize)
    conclose(mysqldb,mysqldbc)
    return "One group finish"


# parse(0,100)
#ppexcut(8)





