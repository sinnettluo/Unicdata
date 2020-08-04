
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
    website ='che273'
    params =ParseInit(website)

    #mysql redefine
    params['createsql']="""CREATE TABLE IF NOT EXISTS `che273_test` (
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
    params['mysqltable'] = 'cn2che_test'
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
    # status
    caritem['status'] = str(re.findall('sale|sold', item["status"])[0])
    caritem['statusplus'] = item["status"]
    return caritem

def parse_keyinfo(dom):
    # caritem init
    caritem = dict()
    # keyinfro
    caritem['pagetitle'] = dom.xpath('//title/text()').extract_first() if dom.xpath('//title/text()') else "-"  # new
    caritem['title'] = dom.xpath('//div[@class="car-info-title"]/h1/text()').extract_first() \
        if dom.xpath('//div[@class="car-info-title"]/h1/text()') \
        else re.compile(u'\u3010').sub('',dom.xpath('//h1[@data-widget="app/ms_v2/js/detail.js#showTitle"]/b/text()').extract_first().strip()).strip() \
            if dom.xpath('//h1[@data-widget="app/ms_v2/js/detail.js#showTitle"]/b/text()') else "-"
    datatp=dom.xpath(u'//li/label[contains(text(),"\u6392\u91cf")]/../text()').extract_first()
    if  datatp==u'0.00L'  or datatp=="" or datatp==u'\u672a\u77e5' or datatp==None :
        if re.compile("\d\.\d").findall(caritem['title']):
            caritem['output']=re.compile("\d\.\d").findall(caritem['title'])[0]
        else:
            caritem['output']="-"
    else:
        caritem['output'] = ''.join(dom.xpath(u'//li/label[contains(text(),"\u6392\u91cf")]/../text()').re('\d+\.?\d*')) \
            if dom.xpath(u'//li/label[contains(text(),"\u6392\u91cf")]/../text()') else "-"

    caritem['price1'] = dom.xpath('//strong[@class="main_price"]/text()').extract_first() \
        if dom.xpath('//strong[@class="main_price"]/text()') else ''.join(dom.xpath('//strong[@class="total"]/span[not(@class="unit")]/text()').extract()) \
            if dom.xpath('//strong[@class="total"]/span[not(@class="unit")]/text()') else "-"
    caritem['pricetag'] = "-"
    return caritem

def parse_baseinfo(dom):
    # caritem init
    caritem = dict()
    # baseinfo
    if dom.xpath(u'//dl/dd[contains(text(),"\u4e0a\u724c\u65f6\u95f4")]/strong/text()').extract_first() ==u'\u672a\u77e5':
        caritem['registerdate']="-"
    else:
        caritem['registerdate'] = ('-'.join(
            dom.xpath(u'//dl/dd[contains(text(),"\u4e0a\u724c\u65f6\u95f4")]/strong/text()').re('\d+')) + "-" + "1") \
            if dom.xpath(u'//dl/dd[contains(text(),"\u4e0a\u724c\u65f6\u95f4")]/strong/text()') \
            else (
        '-'.join(dom.xpath('//div[@class="car-info-para"]/div[1]/div[@class="con"]/text()').re('\d+')) + "-" + "1") \
            if dom.xpath('//div[@class="car-info-para"]/div[1]/div[@class="con"]/text()') else "-"

    caritem['posttime'] = dom.xpath('//div[@id="detail_main_info"]/div/div[@class="time"]/span[1]/text()').extract_first() \
        if dom.xpath('//div[@id="detail_main_info"]/div/div[@class="time"]/span[1]/text()') \
        else '-'.join(dom.xpath('//div[@class="car-info-title"]/div[@class="time"]/text()').re('\d+')) \
            if dom.xpath('//div[@class="car-info-title"]/div[@class="time"]/text()') else "-"
    caritem['years'] = "-"
    datam=dom.xpath(u'//li/label[contains(text(),"\u8868\u663e\u91cc\u7a0b")]/../text()').extract_first()
    if datam=="" or datam==None or datam==u'\u672a\u77e5' or datam==u'-':
        caritem['mileage']="-"
    else:
        if datam.find(u'\u4e07') !=-1:
            caritem['mileage'] = re.match('\d+\.?\d*',datam).group(0)
        else:
            caritem['mileage'] =round(float(re.match('\d+\.?\d*',datam).group(0))/10000,1)

    caritem['geartype'] = dom.xpath(u'//li/label[contains(text(),"\u53d8\u901f\u7bb1")]/../text()').extract_first() \
        if dom.xpath(u'//li/label[contains(text(),"\u53d8\u901f\u7bb1")]/../text()') else "-"
    caritem['region'] = "-"
    caritem['dealplace'] = dom.xpath(u'//li/label[contains(text(),"\u4ea4\u6613\u5730\u533a")]/../text()').extract_first() \
        if dom.xpath(u'//li/label[contains(text(),"\u4ea4\u6613\u5730\u533a")]/../text()')  else "-"
    if caritem['dealplace'] !="-":
        if "/" in caritem['dealplace']:
            caritem['province'] = caritem['dealplace'].split("/")[0]
            caritem['city'] = caritem['dealplace'].split("/")[1]
        else:
            caritem['province'] = caritem['dealplace']
            caritem['city'] = caritem['dealplace']
    else:
        caritem['province'] = "-"
        caritem['city'] = "-"

    caritem['changetimes'] = "-"
    caritem['changedate'] = "-"
    return caritem

def parse_certification(dom):
    # caritem init
    caritem = dict()
    # citification
    caritem['Insurance1'] =dom.xpath(u'//li/label[contains(text(),"\u4ea4\u5f3a\u9669")]/../text()').extract_first() \
        if dom.xpath(u'//li/label[contains(text(),"\u4ea4\u5f3a\u9669")]/../text()') else "-"
    caritem['Insurance2'] =dom.xpath(u'//li/label[contains(text(),"\u6709\u65e0\u5546\u4e1a\u9669")]/../text()').extract_first() \
        if dom.xpath(u'//li/label[contains(text(),"\u6709\u65e0\u5546\u4e1a\u9669")]/../text()') else "-"
    caritem['yearchecktime'] =dom.xpath(u'//li/label[contains(text(),"\u5e74\u68c0\u60c5\u51b5")]/../text()').extract_first() \
        if dom.xpath(u'//li/label[contains(text(),"\u5e74\u68c0\u60c5\u51b5")]/../text()') else "-"
    caritem['checkstate']=dom.xpath('//div[@class="tag"]/em/text()').extract_first() if dom.xpath('//div[@class="tag"]/em/text()') else "-"
    caritem['carmiantain']=dom.xpath(u'//li/label[contains(text(),"\u4fdd\u517b\u60c5\u51b5")]/../text()').extract_first() \
        if dom.xpath(u'//li/label[contains(text(),"\u4fdd\u517b\u60c5\u51b5")]/../text()') else "-"
    caritem['carlabel']=''.join(dom.xpath('//li[@class="feature"]/a/text()').extract()) \
        if dom.xpath('//li[@class="feature"]/a/text()') \
        else ''.join(dom.xpath('//li[@class="other"]/a/text()').extract()) if dom.xpath('//li[@class="other"]/a/text()') else "-"
    if len(caritem['carlabel']) >127:
        caritem['carlabel'] = caritem['carlabel'][:127]
    caritem['carcard'] = dom.xpath('//li[@class="feature"]/a[1]/@href').extract_first().split('/')[-2] \
        if dom.xpath('//li[@class="feature"]/a[1]/@href') \
        else dom.xpath('//li[@class="other"]/a[1]/@href').extract_first().split('/')[-2] if dom.xpath('//li[@class="other"]/a[1]/@href') else "-"
    caritem['carmakeyear']=dom.xpath('//li[@class="feature"]/a[2]/@href').extract_first().split('/')[-2] \
         if  dom.xpath('//li[@class="feature"]/a[2]/@href') \
         else dom.xpath('//li[@class="other"]/a[2]/@href').extract_first().split('/')[-3] if dom.xpath('//li[@class="other"]/a[2]/@href') else "-"
    caritem['caringname']=dom.xpath('//li[@class="feature"]/a[2]/@href').extract_first().split('/')[-3] \
         if  dom.xpath('//li[@class="feature"]/a[2]/@href') \
         else dom.xpath('//li[@class="other"]/a[2]/@href').extract_first().split('/')[-3] if dom.xpath('//li[@class="other"]/a[2]/@href') else "-"
    caritem['carinvoice'] = "-"
    caritem['accident'] = "-"  # new
    caritem['useage'] = dom.xpath(u'//li/label[contains(text(),"\u4f7f\u7528\u6027\u8d28")]/../text()').extract_first() \
        if dom.xpath(u'//li/label[contains(text(),"\u4f7f\u7528\u6027\u8d28")]/../text()') else "-"
    caritem['changetimes']=dom.xpath(u'//li/label[contains(text(),"\u8fc7\u6237\u6b21\u6570")]/../text()').extract_first() \
        if dom.xpath(u'//li/label[contains(text(),"\u8fc7\u6237\u6b21\u6570")]/../text()') else "-"
    caritem['cargood']=dom.xpath('//div[@class="img-view"]/div/span[@class="txt"]/text()').extract_first() \
        if dom.xpath('//div[@class="img-view"]/div/span[@class="txt"]/text()') else "-"
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

def parse_createinfo(dom,carinfocreate,website,mysqldb):
    caritem=[]
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
    '''
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
    '''
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
    caritem['totalcheck'] = dom.xpath('//div[@class="sc_info_right"]/p/text()').extract_first() \
        if dom.xpath('//div[@class="sc_info_right"]/p/text()') else "-"
    caritem['accidentdesc'] = "-".join(checkdesc) \
        if checkdesc else "-"
    '''
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
        # parse baseinfo:3
        caritem = dict(caritem, **parse_baseinfo(dom))
        # parse certification:4
        caritem = dict(caritem, **parse_certification(dom))
        # parse dealor:5
        caritem = dict(caritem, **parse_dealor(dom))
        # parse createinfo:6
        #parse_createinfo(dom,carinfocreate,website,mysqldb)
        # parse carinfo:7
        #caritem = dict(caritem, **parse_carinfo2(dom))
        caritem = dict(caritem, **parse_carinfo1(dom))
        #caritem = dict(caritem, **parse_otherinfo(dom))
        # parse checkpoints:8
        #caritem = dict(caritem, **parse_checkpoints(dom))
        # parse desc:9
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






