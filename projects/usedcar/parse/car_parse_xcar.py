# -*- coding: UTF-8 -*-
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
# load funcs
from Parse_Init import *
from SaveData import *
from PP_Init import *


# basesetting
def Init():
    # params
    website = 'xcar'
    params = ParseInit(website)
    # mysql redefine
    params['createsql'] = """CREATE TABLE IF NOT EXISTS `xcar_p` (
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
                                `dealplace` varchar(551) DEFAULT NULL,
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
                                `dealcompany` varchar(127) DEFAULT NULL,
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
                                `4skeep` varchar(63) DEFAULT NULL,
                                `salecounts` varchar(63) DEFAULT NULL,
                                `soldcounts` varchar(63) DEFAULT NULL,
                                 `output` varchar(63) DEFAULT NULL,
                                 `mid` varchar(255) DEFAULT NULL,
                                 `desc` varchar(551) DEFAULT NULL,
                                 `img_url` varchar(255) DEFAULT NULL,
                                 PRIMARY KEY  (`id`)
                              ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
    params['mysqltable']='xcar_p'
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
    caritem['status'] = str(re.findall('sale|sold', item["status"])[0])
    caritem['statusplus'] = item["status"]
    return caritem


def parse_keyinfo(dom,item):
    # caritem init
    caritem = dict()
    # keyinfro
    caritem['url'] = item["url"]
    caritem['pagetitle'] = dom.xpath('//title/text()').extract_first() if dom.xpath('//title/text()') else "-"
    caritem['title'] = dom.xpath('//div[@class="datum_right"]/h2/text()').extract_first() \
        if  dom.xpath('//div[@class="datum_right"]/h2/text()') \
        else dom.xpath('//div[@class="specifics_title"]/h1/text()').extract_first() \
            if dom.xpath('//div[@class="specifics_title"]/h1/text()') else "-"

    if "shop" in caritem['url']:
        caritem['price1'] =''.join(dom.xpath('//div[@class="datum_data"]/p[1]/span[1]/b/text()').re('\d+\.?\d*')) \
            if dom.xpath('//div[@class="datum_data"]/p[1]/span[1]/b') \
            else dom.xpath('//div[@class="info_cost"]/p/span[@class="cost"]/text()').extract_first() \
                if dom.xpath('//div[@class="info_cost"]/p/span[@class="cost"]/text()') else "-"
    elif "personal" in caritem['url']:
        caritem['price1'] = ''.join(dom.xpath('//div[@class="datum_price"]/p[1]/b/text()').re('\d+\.?\d*')) \
            if dom.xpath('//div[@class="datum_price"]/p[1]/b') \
            else dom.xpath('//div[@class="info_cost"]/p/span[@class="cost"]/text()').extract_first() \
                if dom.xpath('//div[@class="info_cost"]/p/span[@class="cost"]/text()') else "-"
    else:
        caritem['price1']="-"

    if "shop" in caritem['url']:
        caritem['guideprice'] =''.join(dom.xpath('//div[@class="datum_data"]/p[1]/span[3]/a/text()').re('\d+\.?\d*')) \
            if dom.xpath('//div[@class="datum_data"]/p[1]/span[3]/a') \
            else ''.join(dom.xpath('//div[@class="info_cost"]/p[2]/text()').re('\d+\.?\d*')) \
                if dom.xpath('//div[@class="info_cost"]/p[2]/text()') else "-"
    elif "personal" in caritem['url']:
        caritem['guideprice'] = ''.join(dom.xpath('//div[@class="datum_price"]/p[3]/span/text()').re('\d+\.?\d*')) \
            if dom.xpath('//div[@class="datum_price"]/p[3]/span') \
            else ''.join(dom.xpath('//div[@class="info_cost"]/p[2]/text()').re('\d+\.?\d*')) \
                if dom.xpath('//div[@class="info_cost"]/p[2]/text()') else "-"
    else:
        caritem['guideprice']="-"

    caritem['pricetag'] = "-"

    caritem['brand_name']=re.compile(u'\u4e8c\u624b').sub('',dom.xpath('//div[@class="bread"][1]/a[3]/text()').extract_first()) \
        if dom.xpath('//div[@class="bread"][1]/a[3]/text()') else "-"

    caritem['class_name']=re.compile(u'\u4e8c\u624b').sub('',dom.xpath('//div[@class="bread"][1]/a[4]/text()').extract_first()) \
        if dom.xpath('//div[@class="bread"][1]/a[4]/text()') else "-"

    return caritem


def parse_baseinfo(dom,item):
    # caritem init
    caritem = dict()
    # baseinfo
    caritem['url'] = item["url"]
    if "shop" in caritem['url']:
        caritem['registerdate'] ='-'.join(dom.xpath('//div[@class="datum_data"]/p[2]/span[1]/text()').re('\d+\.?\d*'))+"-01" \
            if dom.xpath('//div[@class="datum_data"]/p[2]/span[1]') \
            else '-'.join(dom.xpath('//ul[@class="datum_ul"]/li[1]/text()').re('\d+\.?\d*')) \
                if dom.xpath('//ul[@class="datum_ul"]/li[1]/text()') else "-"
    elif "personal" in caritem['url']:
        caritem['registerdate'] = '-'.join(dom.xpath('//div[@class="datum_price"]/p[4]/span[1]/text()').re('\d+\.?\d*')) +"-01" \
            if dom.xpath('//div[@class="datum_price"]/p[4]/span[1]') \
            else '-'.join(dom.xpath('//ul[@class="datum_ul"]/li[1]/text()').re('\d+\.?\d*')) \
                if dom.xpath('//ul[@class="datum_ul"]/li[1]/text()') else "-"
    else:
        caritem['registerdate']="-"

    caritem['posttime'] = '-'.join(dom.xpath('//div[@class="release_time"]/text()').re('\d+\.?\d*')) \
        if dom.xpath('//div[@class="release_time"]') \
        else '-'.join(dom.xpath('//span[@class="time"]/text()').re('\d+\.?\d*')) \
            if dom.xpath('//span[@class="time"]/text()') else "-"

    caritem['years'] = "-"

    if "shop" in caritem['url']:
        caritem['mileage'] =''.join(dom.xpath('//div[@class="datum_data"]/p[2]/span[2]/text()').re('\d+\.?\d*'))\
            if dom.xpath('//div[@class="datum_data"]/p[2]/span[2]') \
            else ''.join(dom.xpath('//ul[@class="datum_ul"]/li[3]/text()').re('\d+\.?\d*')) \
                if dom.xpath('//ul[@class="datum_ul"]/li[3]/text()') else "-"
    elif "personal" in caritem['url']:
        caritem['mileage'] = '-'.join(dom.xpath('//div[@class="datum_price"]/p[4]/span[2]/text()').re('\d+\.?\d*')) \
            if dom.xpath('//div[@class="datum_price"]/p[4]/span[2]') \
            else ''.join(dom.xpath('//ul[@class="datum_ul"]/li[3]/text()').re('\d+\.?\d*')) \
                if dom.xpath('//ul[@class="datum_ul"]/li[3]/text()') else "-"
    else:
        caritem['mileage']="-"

    if "shop" in caritem['url']:
        caritem['geartype'] =dom.xpath('//div[@class="datum_data"]/p[2]/span[4]/text()').extract_first()\
            if dom.xpath('//div[@class="datum_data"]/p[2]/span[4]') \
            else dom.xpath('//ul[@class="datum_ul"]/li[4]/text()').extract_first() \
                if dom.xpath('//ul[@class="datum_ul"]/li[4]/text()') else "-"
    elif "personal" in caritem['url']:
        caritem['geartype'] = dom.xpath('//div[@class="datum_price"]/p[4]/span[4]/text()').extract_first() \
            if dom.xpath('//div[@class="datum_price"]/p[4]/span[4]') \
            else dom.xpath('//ul[@class="datum_ul"]/li[4]/text()').extract_first() \
                if dom.xpath('//ul[@class="datum_ul"]/li[4]/text()') else "-"
    else:
        caritem['geartype']="-"

    if "shop" in caritem['url']:
        caritem['output'] =''.join(dom.xpath('//div[@class="datum_data"]/p[2]/span[3]/text()').re('\d+\.?\d*'))\
            if dom.xpath('//div[@class="datum_data"]/p[2]/span[3]') \
            else ''.join(dom.xpath('//ul[@class="datum_ul"]/li[2]/text()').re('\d+\.?\d*')) \
                if dom.xpath('//ul[@class="datum_ul"]/li[2]/text()') else "-"
    elif "personal" in caritem['url']:
        caritem['output'] = ''.join(dom.xpath('//div[@class="datum_price"]/p[4]/span[3]/text()').re('\d+\.?\d*')) \
            if dom.xpath('//div[@class="datum_price"]/p[4]/span[3]') \
            else ''.join(dom.xpath('//ul[@class="datum_ul"]/li[2]/text()').re('\d+\.?\d*')) \
                if dom.xpath('//ul[@class="datum_ul"]/li[2]/text()') else "-"
    else:
        caritem['output']="-"

    if "shop" in caritem['url']:
        caritem['emission'] =dom.xpath('//div[@class="datum_data"]/p[2]/span[5]/text()').extract_first()\
            if dom.xpath('//div[@class="datum_data"]/p[2]/span[5]') \
            else dom.xpath('//ul[@class="datum_ul"]/li[6]/text()').extract_first() \
                if dom.xpath('//ul[@class="datum_ul"]/li[6]/text()') else "-"
    elif "personal" in caritem['url']:
        caritem['emission'] =dom.xpath('//div[@class="datum_price"]/p[4]/span[5]/text()').extract_first() \
            if dom.xpath('//div[@class="datum_price"]/p[4]/span[5]') \
            else dom.xpath('//ul[@class="datum_ul"]/li[6]/text()').extract_first() \
                if dom.xpath('//ul[@class="datum_ul"]/li[6]/text()') else "-"
    else:
        caritem['emission']="-"

    caritem['gear'] ="-"
    caritem['province'] = dom.xpath('//table[@class="info_table"]/tr[1]/td[2]/span/text()').extract_first().split("-")[0] \
        if dom.xpath('//table[@class="info_table"]/tr[1]/td[2]/span') \
        else dom.xpath('//table[@class="details_table"]/tr[1]/td[2]/text()').extract_first().split("-")[0]  \
            if dom.xpath('//table[@class="details_table"]/tr[1]/td[2]/text()') else "-"

    caritem['city'] = dom.xpath('//table[@class="info_table"]/tr[1]/td[2]/span/text()').extract_first().split("-")[1] \
        if dom.xpath('//table[@class="info_table"]/tr[1]/td[2]/span') \
        else dom.xpath('//table[@class="details_table"]/tr[1]/td[2]/text()').extract_first().split("-")[1] \
            if dom.xpath('//table[@class="details_table"]/tr[1]/td[2]') else "-"

    caritem['changetimes'] = "-"
    caritem['changedate'] = "-"
    caritem['body']="-"
    return caritem


def parse_certification(dom):
    # caritem init
    caritem = dict()
    # citification
    caritem['Insurance1'] = dom.xpath('//table[@class="info_table"]/tr[3]/td[2]/span/text()').extract_first() \
        if dom.xpath('//table[@class="info_table"]/tr[3]/td[2]/span') \
        else  dom.xpath('//table[@class="details_table"]/tr[3]/td[2]/text()').extract_first() \
            if dom.xpath('//table[@class="details_table"]/tr[3]/td[2]/text()') else "-"

    caritem['Insurance2'] = "-"

    caritem['yearchecktime'] =dom.xpath('//table[@class="info_table"]/tr[3]/td[4]/span/text()').extract_first() \
        if dom.xpath('//table[@class="info_table"]/tr[3]/td[4]/span') \
        else  dom.xpath('//table[@class="details_table"]/tr[3]/td[4]/text()').extract_first() \
            if dom.xpath('//table[@class="details_table"]/tr[3]/td[4]/text()') else "-"

    caritem['carokcf'] = "-"
    caritem['carcard'] = "-"
    caritem['carinvoice'] = "-"
    caritem['accident'] = "-"  # new
    caritem['useage'] =dom.xpath('//table[@class="info_table"]/tr[1]/td[4]/span/text()').extract_first()  \
        if dom.xpath('//table[@class="info_table"]/tr[1]/td[4]/span')\
        else  dom.xpath('//table[@class="details_table"]/tr[1]/td[4]/text()').extract_first() \
            if dom.xpath('//table[@class="details_table"]/tr[1]/td[4]/text()') else "-"

    return caritem


def parse_dealor(dom,item):
    # caritem init
    caritem = dict()
    # dealer
    caritem['url'] = item["url"]
    caritem['dealplace'] = dom.xpath('//div[@class="location"]/text()').extract_first() \
        if  dom.xpath('//div[@class="location"]') \
        else dom.xpath('//div[@class="details_bottom"]/p[1]/span/text()').extract_first() \
            if dom.xpath('//div[@class="details_bottom"]/p[1]/span/text()') else "-"
    if caritem['dealplace']==None:
        caritem['dealplace']="-"
    else:
        if len(caritem['dealplace'])>551:
            caritem['dealplace']=caritem['dealplace'][:551]

    caritem['telphone'] =dom.xpath('//table[@class="datum_table"]/tr[2]/td[3]/em/text()').extract_first()\
        if dom.xpath('//table[@class="datum_table"]/tr[2]/td[3]/em')\
        else dom.xpath('//div[@class="specifics_main clearfix mb_20"]/div[@class="shop_cont"]/dl[1]/dd/text()').extract_first() \
            if dom.xpath('//div[@class="specifics_main clearfix mb_20"]/div[@class="shop_cont"]/dl[1]/dd/text()') else "-"

    caritem['dealor'] = dom.xpath('//div[@ class="phone"]/span[2]/text()').extract_first()  \
        if dom.xpath('//div[@class="phone"]/span[2]')\
        else dom.xpath('//div[@class="details_one"]/span[@class="name"]/text()').extract_first() \
            if dom.xpath('//div[@class="details_one"]/span[@class="name"]/text()') else "-"

    if "shop" in caritem['url']:
        caritem['dealtype'] =u'\u5546\u5bb6'
    elif "personal" in caritem['url']:
        caritem['dealtype'] =u'\u4e2a\u4eba'
    else:
        caritem['dealtype']="-"


    caritem['salecounts']=dom.xpath('//table[@class="datum_table"]/tr[1]/td[2]/em/text()').extract_first() \
        if dom.xpath('//table[@class="datum_table"]/tr[1]/td[2]/em') \
        else dom.xpath('//div[@class="specifics_main clearfix mb_20"]/div[@class="shop_cont"]/dl[6]/dd/text()').extract_first()  \
            if dom.xpath('//div[@class="specifics_main clearfix mb_20"]/div[@class="shop_cont"]/dl[6]/dd/text()') else "-"

    caritem['soldcounts']=dom.xpath('//table[@class="datum_table"]/tr[2]/td[2]/text()').re('\d+\.?\d*')[0] \
        if dom.xpath('//table[@class="datum_table"]/tr[2]/td[2]') \
        else dom.xpath('//div[@class="specifics_main clearfix mb_20"]/div[@class="shop_cont"]/dl[5]/dd/text()').extract_first() \
            if dom.xpath('//div[@class="specifics_main clearfix mb_20"]/div[@class="shop_cont"]/dl[5]/dd/text()') else "-"

    caritem['dealcompany'] = dom.xpath('//div[@class="shop_title"]/h2/text()').extract_first()\
        if dom.xpath('//div[@class="shop_title"]/h2') \
        else dom.xpath('//div[@class="specifics_main clearfix mb_20"]/div[@class="shop_cont"]/h3/text()').extract_first() \
            if dom.xpath('//div[@class="specifics_main clearfix mb_20"]/div[@class="shop_cont"]/h3/text()') else "-"

    return caritem


def parse_createinfo(dom, carinfocreate, website, mysqldb):
    mycarinfo = []
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

    caritem['color'] = dom.xpath('//table[@class="info_table"]/tr[2]/td[4]/span/text()').extract_first() \
        if  dom.xpath('//table[@class="info_table"]/tr[2]/td[4]/span')\
        else dom.xpath('//table[@class="details_table"]/tr[2]/td[4]/text()').extract_first() \
            if dom.xpath('//table[@class="details_table"]/tr[2]/td[4]/text()') else "-"

    caritem['4skeep']=dom.xpath('//table[@class="info_table"]/tr[2]/td[6]/span/text()').extract_first() \
        if dom.xpath('//table[@class="info_table"]/tr[2]/td[6]/span')\
        else  dom.xpath('//table[@class="details_table"]/tr[2]/td[6]/text()').extract_first() \
            if dom.xpath('//table[@class="details_table"]/tr[2]/td[6]/text()') else "-"

    caritem['guidepricetax'] = '-'
    caritem['newcartitle'] = "-"
    caritem['newcarurl'] = dom.xpath('//div[@class="tag_cont"]/iframe/@src').extract_first() \
        if dom.xpath('//div[@class="tag_cont"]/iframe/@src') \
        else dom.xpath('//div[@class="info_show"]/iframe/@src').extract_first()  \
            if dom.xpath('//div[@class="info_show"]/iframe/@src') else "-"
    caritem['mid']=dom.xpath('//div[@class="tag_cont"]/iframe/@src').extract_first().split('mid=')[1] \
        if dom.xpath('//div[@class="tag_cont"]/iframe/@src') \
        else dom.xpath('//div[@class="info_show"]/iframe/@src').extract_first().split('mid=')[1] \
            if dom.xpath('//div[@class="info_show"]/iframe/@src') else "-"

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
    caritem['totalcheck'] = dom.xpath('//div[@class="sc_info_right"]/p/text()').extract_first()
        if dom.xpath('//div[@class="sc_info_right"]/p/text()') else "-"
    caritem['accidentdesc'] = "-".join(checkdesc)
        if checkdesc else "-"
    '''
    return caritem


def parse_desc(dom):
    # caritem init
    caritem = dict()
    # more desc
    caritem['desc'] = dom.xpath('//div[@class="tag_cont sq_message"]/p/text()').extract_first().encode('gbk','ignore').decode('gbk','ignore') \
        if dom.xpath('//div[@class="tag_cont sq_message"]/p') \
        else dom.xpath('//div[@class="details_list2 clearfix mt12"][1]/p/text()').extract_first().encode('gbk','ignore').decode('gbk','ignore') \
            if dom.xpath('//div[@class="details_list2 clearfix mt12"][1]/p') else "-"
    if caritem['desc']==None:
        caritem['desc']="-"
    else:
        if len(caritem['desc'])>551:
            caritem['desc']=caritem['desc'][:551]

    caritem['img_url'] = dom.xpath('//ul[@class="img_mian"]/li[1]/a/img/@src').extract_first() \
        if dom.xpath('//ul[@class="img_mian"]/li[1]/a/img/@src') \
        else dom.xpath('//div[@class="details_list2 clearfix mt12"][2]/p[1]/img/@src').extract_first() \
            if dom.xpath('//div[@class="details_list2 clearfix mt12"][2]/p[1]/img/@src') else "-"

    return caritem


# car parse control
def parse(item):
    # -*- coding: UTF-8 -*-
    # carinit
    caritems = []
    # params
    params = Init()
    processparamlist = ParseprocessInit(params)
    website = processparamlist[0]
    carinfocreate = processparamlist[1]
    counts = processparamlist[2]
    savesize = processparamlist[3]
    mysqltable = processparamlist[4]
    # connection = processparamlist[5]
    # collection = processparamlist[6]
    mysqldb = processparamlist[7]
    mysqldbc = processparamlist[8]
    # df = processparamlist[9]

    # for i in collection.find().skip(start).limit(step):
    #     returndf = bloom_check(i['status'], df)
    #     if not returndf:
    #         try:
    try:
        # counts += 1
        # print counts
        # parse original:1
        # caritem init
        # parse original:1
        caritem = parse_original(item)
        # parse keyinfo:2
        content= item['datasave'][1]
        dom = scrapy.selector.Selector(text=content)
        # if dom.xpath(u'//title[contains(text(),"\u60a8\u8bbf\u95ee\u7684\u9875\u9762\u51fa\u9519\u4e86")]'):
        #     continue
        caritem = dict(caritem, **parse_keyinfo(dom,item))

        # parse baseinfo:3
        caritem = dict(caritem, **parse_baseinfo(dom,item))
        # parse certification:4
        caritem = dict(caritem, **parse_certification(dom))
        # parse dealor:5
        caritem = dict(caritem, **parse_dealor(dom,item))
        # parse createinfo:6
        # parse_createinfo(dom,carinfocreate,website,mysqldb)
        # parse carinfo:7
        #caritem = dict(caritem, **parse_carinfo1(dom))
        caritem = dict(caritem, **parse_carinfo2(dom))
        # caritem = dict(caritem, **parse_otherinfo(dom))
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
    savecarfinal(caritems, mysqltable, mysqldb, savesize)
    conclose( mysqldb, mysqldbc)
    return "One group finish"





#parse(0, 2000)
# ppexcut(8)






