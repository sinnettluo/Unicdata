#-*- coding: UTF-8 -*-
import json
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
    website ='souhu'
    params =ParseInit(website)
    #mysql redefine
    params['createsql']="""CREATE TABLE IF NOT EXISTS `souhu` (
                                `id` bigint(20) NOT NULL auto_increment,
                                `website` varchar(63) DEFAULT NULL,
                                `carid` varchar(63) DEFAULT NULL,
                                `title` varchar(500) DEFAULT NULL,
                                `pagetitle` varchar(500) DEFAULT NULL,
                                `url` varchar(1000) DEFAULT NULL,
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
                                `dealplace` varchar(551) DEFAULT NULL,
                                `changetimes` varchar(63) DEFAULT NULL,
                                `changedate` varchar(63) DEFAULT NULL,
                                `Insurance1` varchar(63) DEFAULT NULL,
                                `Insurance2` varchar(63) DEFAULT NULL,
                                `caryearcheck` varchar(127) DEFAULT NULL,
                                `carokcf` varchar(63) DEFAULT NULL,
                                `carcard` varchar(63) DEFAULT NULL,
                                `carinvoice` varchar(63) DEFAULT NULL,
                                `accident` varchar(63) DEFAULT NULL,
                                `useage` varchar(63) DEFAULT NULL,
                                `telphone` varchar(63) DEFAULT NULL,
                                `dealor` varchar(127) DEFAULT NULL,
                                `dealtype` varchar(127) DEFAULT NULL,
                                `dealcompany` varchar(500) DEFAULT NULL,
                                `luggage` varchar(127) DEFAULT NULL,
                                `guideprice` varchar(63) DEFAULT NULL,
                                `guidepricetax` varchar(63) DEFAULT NULL,
                                `newcartitle` varchar(127) DEFAULT NULL,
                                `newcarurl` varchar(127) DEFAULT NULL,
                                `geartype` varchar(63) DEFAULT NULL,
                                `emission` varchar(63) DEFAULT NULL,
                                `modelid` varchar(63) DEFAULT NULL,
                                `trimmid` varchar(63) DEFAULT NULL,
                                `dealerId` varchar(63) DEFAULT NULL,
                                `brandid` varchar(63) DEFAULT NULL,
                                `modelYear` varchar(63) DEFAULT NULL,
                                `licenseProvince` varchar(127) DEFAULT NULL,
                                `licenseCity` varchar(63) DEFAULT NULL,
                                `gear` varchar(63) DEFAULT NULL,
                                `body` varchar(63) DEFAULT NULL,
                                 `output` varchar(63) DEFAULT NULL,
                                 `desc` varchar(551) DEFAULT NULL,
                                 `img_url` varchar(500) DEFAULT NULL,
                                 PRIMARY KEY  (`id`)
                              ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
    params['mysqltable']='souhu'
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
    # caritem init
    caritem = dict()
    # keyinfro
    caritem['website'] = item['website']
    caritem['carid'] = (re.findall('\d+', item["url"].split('_')[-1]))
    caritem['url'] = item["url"]
    caritem['grabtime'] = item["grabtime"]
    caritem['pagetime'] = item["pagetime"] # new
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
    caritem['title'] = dom.xpath('//div[@class="car-detail"]/h3/text()').extract_first().strip() \
        if dom.xpath('//div[@class="car-detail"]/h3/text()')else "-"
    caritem['price1'] = ''.join(dom.xpath('//span[@class="car-price"]/text()').re('\d+\.?\d*')) \
        if dom.xpath('//span[@class="car-price"]/text()') else "-"
    caritem['pricetag'] = re.compile(u'\uff08|\uff09').sub('',dom.xpath('//span[@class="price-desc"]/text()').extract_first()) \
        if dom.xpath('//span[@class="price-desc"]/text()') else "-"
    if dom.xpath('//del[@class="car-price-new"]/text()').extract_first()=="" or dom.xpath('//del[@class="car-price-new"]/text()').extract_first()==None:
        caritem['guideprice']="-"
    else:
        caritem['guideprice']=''.join(dom.xpath('//del[@class="car-price-new"]/text()').re('\d+\.?\d*'))
    caritem['guidepricetax']="-"
    return caritem


def parse_baseinfo(dom):
    # caritem init
    caritem = dict()
    #  baseinfo
    datareg=dom.xpath('//div[@class="detail-info-box"]/div[1]/span[2]/text()').extract_first()
    if datareg=="" or datareg==None or datareg==u'\u5c1a\u672a\u4e0a\u724c':
        caritem['registerdate']="-"
    else:
        caritem['registerdate'] =( '-'.join(dom.xpath('//div[@class="detail-info-box"]/div[1]/span[2]/text()').re('\d+'))+"-"+"1")

    caritem['posttime'] =dom.xpath('//div[@class="car-detail-tip"]/label[@class="message"]/text()').extract_first().split(u'\uff1a')[1] \
        if dom.xpath('//div[@class="car-detail-tip"]/label[@class="message"]/text()') else "-"
    caritem['years'] = "-"
    caritem['mileage'] =''.join(dom.xpath('//div[@class="detail-info-box"]/div[2]/span[2]/text()').re('\d+\.?\d*')) \
        if dom.xpath('//div[@class="detail-info-box"]/div[2]/span[2]/text()') else "-"
    caritem['geartype']=dom.xpath('//div[@class="detail-info-box"]/div[4]/span[2]/text()').extract_first() \
        if dom.xpath('//div[@class="detail-info-box"]/div[4]/span[2]/text()')else "-"
    caritem['region'] = "-"

    if dom.xpath('//ul[@class="car-banner"]/li[@style="display: none;"]'):
        caritem['dealtype'] = u'\u4e2a\u4eba'
        caritem['dealplace'] = "-"
    else:
        caritem['dealtype']=u'\u5546\u5bb6'
        caritem['dealplace']=''.join(dom.xpath('//td[@class="car-addr-val"]/text()').extract()).strip()\
            if dom.xpath('//td[@class="car-addr-val"]/text()') else "-"
    if len(caritem['dealplace'])>551:
        caritem['dealplace']=caritem['dealplace'][0:551]
    caritem['dealcompany']="-"
    caritem['province'] = "-"
    caritem['city'] = dom.xpath('//span[@id="J_city_show"]/text()').extract_first() if dom.xpath('//span[@id="J_city_show"]/text()') else "-"
    caritem['changetimes'] = "-"
    caritem['changedate'] = "-"
    return caritem


def parse_certification(dom):
    # caritem init
    caritem = dict()
    # citification
    caritem['Insurance1'] =dom.xpath(u'//td[contains(text(),"\u4fdd\u9669\u622a\u6b62\u65e5\u671f")]/following-sibling::*/text()').extract_first() \
        if dom.xpath(u'//td[contains(text(),"\u4fdd\u9669\u622a\u6b62\u65e5\u671f")]/following-sibling::*/text()') else "-"
    caritem['caryearcheck']= dom.xpath(u'//td[contains(text(),"\u5e74\u68c0\u622a\u6b62")]/following-sibling::*/text()').extract_first() \
        if dom.xpath(u'//td[contains(text(),"\u5e74\u68c0\u622a\u6b62")]/following-sibling::*/text()') else "-"
    caritem['Insurance2'] = dom.xpath(u'//td[contains(text(),"\u5546\u4e1a\u4fdd\u9669")]/following-sibling::*/text()').extract_first() \
        if  dom.xpath(u'//td[contains(text(),"\u5546\u4e1a\u4fdd\u9669")]/following-sibling::*/text()').extract_first() else "-"
    caritem['carokcf'] = "-"
    caritem['carcard'] = "-"
    datasum = dom.xpath('//script[@type="text/javascript"][1]/text()').extract_first().strip()
    datasum = re.compile('var|\s').sub('', datasum).split(';')
    caritem['modelid']=re.compile('\d+').search(datasum[0]).group() if re.compile('\d+').search(datasum[0]) else "-"
    caritem['trimmid']=re.compile('\d+').search(datasum[1]).group() if re.compile('\d+').search(datasum[1]) else "-"
    caritem['brandid'] =re.compile('\d+').search(datasum[-6]).group() if re.compile('\d+').search(datasum[-6]) else "-"
    caritem['dealerid']=re.compile('\d+').search(datasum[-7]).group() if re.compile('\d+').search(datasum[-7]) else "-"
    caritem['modelYear']=re.compile('\d+|-').search(datasum[-5]).group() if re.compile('\d+').search(datasum[-5]) else "-"
    caritem['licenseProvince']=re.compile('\d+').search(datasum[-4]).group() if re.compile('\d+').search(datasum[-4]) else "-"
    caritem['licenseCity']=re.compile('\d+').search(datasum[-3]).group() if re.compile('\d+').search(datasum[-3]) else "-"
    caritem['carinvoice'] = "-"
    caritem['accident'] ="-"
    caritem['useage'] = "-"
    caritem['luggage'] = "-"
    return caritem

def parse_dealor(dom):
    # caritem init
    caritem = dict()
    # dealer
    caritem['telphone'] = dom.xpath('//span[@class="car-contact-phone"]/text()').extract_first() \
        if dom.xpath('//span[@class="car-contact-phone"]/text()') else "-"

    caritem['dealor'] = dom.xpath('//div[@class="dealer-title"]/h3/text()').extract_first()  \
        if dom.xpath('//div[@class="dealer-title"]/h3/text()') else "-"
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
    '''
    caritem['carinfo1'] = dom.xpath(u'//td[contains(text(),"\u767e\u516c\u91cc\u6cb9\u8017")]/following-sibling::*/text()').extract_first() \
        if dom.xpath(u'//td[contains(text(),"\u767e\u516c\u91cc\u6cb9\u8017")]/following-sibling::*/text()') else "-"

    caritem['carinfo2'] = dom.xpath(u'//td[contains(text(),"\u53d8\u901f\u7bb1\u6863\u4f4d")]/following-sibling::*/text()').extract_first() \
        if dom.xpath(u'//td[contains(text(),"\u53d8\u901f\u7bb1\u6863\u4f4d")]/following-sibling::*/text()') else "-"

    caritem['carinfo3'] = dom.xpath(u'//td[contains(text(),"\u6700\u9ad8\u8f66\u901f")]/following-sibling::*/text()').extract_first() \
        if dom.xpath(u'//td[contains(text(),"\u6700\u9ad8\u8f66\u901f")]/following-sibling::*/text()') else "-"

    caritem['carinfo4'] = dom.xpath(u'//td[contains(text(),"\u6574\u5907\u8d28\u91cf")]/following-sibling::*/text()').extract_first() \
        if dom.xpath(u'//td[contains(text(),"\u6574\u5907\u8d28\u91cf")]/following-sibling::*/text()') else "-"

    caritem['carinfo5'] =dom.xpath(u'//td[contains(text(),"\u6392\u653e\u7cfb\u7edf")]/following-sibling::*/text()').extract_first() \
        if dom.xpath(u'//td[contains(text(),"\u6392\u653e\u7cfb\u7edf")]/following-sibling::*/text()') else "-"

    caritem['carinfo6'] = dom.xpath(u'//td[contains(text(),"\u8f74\u8ddd")]/following-sibling::*/text()').extract_first() \
        if dom.xpath(u'//td[contains(text(),"\u8f74\u8ddd")]/following-sibling::*/text()') else "-"

    caritem['carinfo7'] =dom.xpath(u'//td[contains(text(),"\u957f*\u5bbd*\u9ad8")]/following-sibling::*/text()').extract_first().split(u'\xd7')[0] \
        if dom.xpath(u'//td[contains(text(),"\u957f*\u5bbd*\u9ad8")]/following-sibling::*/text()') else "-"

    caritem['carinfo8'] = dom.xpath(u'//td[contains(text(),"\u957f*\u5bbd*\u9ad8")]/following-sibling::*/text()').extract_first().split(u'\xd7')[1] \
        if dom.xpath(u'//td[contains(text(),"\u957f*\u5bbd*\u9ad8")]/following-sibling::*/text()') else "-"

    caritem['carinfo9'] = dom.xpath(u'//td[contains(text(),"\u957f*\u5bbd*\u9ad8")]/following-sibling::*/text()').extract_first().split(u'\xd7')[2] \
        if dom.xpath(u'//td[contains(text(),"\u957f*\u5bbd*\u9ad8")]/following-sibling::*/text()') else "-"

    caritem['carinfo10'] = dom.xpath(u'//td[contains(text(),"\u52a0\u901f\u65f6\u95f4")]/following-sibling::*/text()').extract_first() \
        if  dom.xpath(u'//td[contains(text(),"\u52a0\u901f\u65f6\u95f4")]/following-sibling::*/text()') else "-"
    '''

    return caritem


def parse_carinfo1(dom):
    # caritem init
    caritem = dict()
    # carinfo
    caritem['output']= ''.join(dom.xpath(u'//td[contains(text(),"\u6392\u91cf(L)")]/following-sibling::*/text()').re('\d+\.?\d*')) \
        if dom.xpath(u'//td[contains(text(),"\u6392\u91cf(L)")]/following-sibling::*/text()') else "-"
    caritem['gear'] = dom.xpath(u'//td[contains(text(),"\u9a71\u52a8\u65b9\u5f0f")]/following-sibling::*/text()').extract_first() \
        if dom.xpath(u'//td[contains(text(),"\u9a71\u52a8\u65b9\u5f0f")]/following-sibling::*/text()') else "-"
    caritem['emission'] =dom.xpath('//span[@class="car-extra-attr SIP_C_155"]/text()').extract_first() \
        if dom.xpath('//span[@class="car-extra-attr SIP_C_155"]/text()') else "-"
    caritem['color'] = dom.xpath(u'//td[contains(text(),"\u8f66\u8f86\u989c\u8272")]/following-sibling::*/text()').extract_first() \
        if dom.xpath(u'//td[contains(text(),"\u8f66\u8f86\u989c\u8272")]/following-sibling::*/text()') else "-"

    caritem['body'] = "-"
    caritem['newcartitle'] = "-"
    caritem['newcarurl'] ="-"
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
    caritem['desc'] = dom.xpath('//div[@class="tip-message"]/text()').extract_first() \
        if dom.xpath('//div[@class="tip-message"]/text()') else "-"
    if len(caritem['desc'])>551:
        caritem['desc']=caritem['desc'][0:551]
    caritem['img_url'] = dom.xpath('//div[@class="car-big-img"]/img/@src').extract_first() \
        if dom.xpath('//div[@class="car-big-img"]/img/@src') else "-"
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
        content = item['datasave'][1]
        dom = scrapy.selector.Selector(text=content)
        # if dom.xpath(u'//title[contains(text(),"\u641c\u72d0\u4e8c\u624b\u8f66_\u3010404\u9875\u9762\u3011")]'):
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
        #caritem = dict(caritem, **parse_carinfo2(dom))
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




#parse(2400000, 2401000)
# ppexcut(8)






