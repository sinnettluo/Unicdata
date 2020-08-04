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
    website ='haoche51'
    params =ParseInit(website)
    #mysql redefine
    params['createsql']= """CREATE TABLE IF NOT EXISTS `haoche51` (
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
                                `registerplace` varchar(63) DEFAULT NULL,
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
                                `guidepricetax` varchar(63) DEFAULT NULL,
                                `newcartitle` varchar(127) DEFAULT NULL,
                                `newcarurl` varchar(127) DEFAULT NULL,
                                `geartype` varchar(63) DEFAULT NULL,
                                `emission` varchar(63) DEFAULT NULL,
                                `output` varchar(63) DEFAULT NULL,
                                `level` varchar(63) DEFAULT NULL,
                                `motor` varchar(63) DEFAULT NULL,
                                `gear` varchar(63) DEFAULT NULL,
                                `gearnumber` varchar(63) DEFAULT NULL,
                                `lengthwh` varchar(63) DEFAULT NULL,
                                `length` varchar(63) DEFAULT NULL,
                                `width` varchar(63) DEFAULT NULL,
                                `height` varchar(63) DEFAULT NULL,
                                `wheelbase` varchar(63) DEFAULT NULL,
                                `body` varchar(63) DEFAULT NULL,
                                `doors` varchar(63) DEFAULT NULL,
                                `seats` varchar(63) DEFAULT NULL,
                                `bodystyle` varchar(63) DEFAULT NULL,
                                `weight` varchar(63) DEFAULT NULL,
                                `luggage` varchar(63) DEFAULT NULL,
                                `motortype` varchar(63) DEFAULT NULL,
                                `method` varchar(63) DEFAULT NULL,
                                `lwvnumber` varchar(63) DEFAULT NULL,
                                `compress` varchar(63) DEFAULT NULL,
                                `maxps` varchar(63) DEFAULT NULL,
                                `maxnm` varchar(63) DEFAULT NULL,
                                `fuelnumber` varchar(63) DEFAULT NULL,
                                `fuelmethod` varchar(63) DEFAULT NULL,
                                `driveway` varchar(63) DEFAULT NULL,
                                `fronthang` varchar(63) DEFAULT NULL,
                                `backhang` varchar(63) DEFAULT NULL,
                                `assistanttype` varchar(63) DEFAULT NULL,
                                `frontbrake` varchar(63) DEFAULT NULL,
                                `backbrake` varchar(63) DEFAULT NULL,
                                `hubtype` varchar(63) DEFAULT NULL,
                                `frontwheel` varchar(63) DEFAULT NULL,
                                `backwheel` varchar(63) DEFAULT NULL,
                                `bn_bo` varchar(63) DEFAULT NULL,
                                `bq_br` varchar(63) DEFAULT NULL,
                                `bs_bp` varchar(63) DEFAULT NULL,
                                `bx` varchar(63) DEFAULT NULL,
                                `cc` varchar(63) DEFAULT NULL,
                                `cc1` varchar(63) DEFAULT NULL,
                                `cd` varchar(63) DEFAULT NULL,
                                `ch` varchar(63) DEFAULT NULL,
                                `ci` varchar(63) DEFAULT NULL,
                                `dy` varchar(63) DEFAULT NULL,
                                `dz` varchar(63) DEFAULT NULL,
                                `ea` varchar(63) DEFAULT NULL,
                                `eb` varchar(63) DEFAULT NULL,
                                `ec` varchar(63) DEFAULT NULL,
                                `ef` varchar(63) DEFAULT NULL,
                                `em` varchar(63) DEFAULT NULL,
                                `ei_ej` varchar(63) DEFAULT NULL,
                                `es` varchar(63) DEFAULT NULL,
                                `cw` varchar(63) DEFAULT NULL,
                                `db_dc` varchar(63) DEFAULT NULL,
                                `dh_di` varchar(63) DEFAULT NULL,
                                `dl` varchar(63) DEFAULT NULL,
                                `cq` varchar(63) DEFAULT NULL,
                                `cu` varchar(63) DEFAULT NULL,
                                `cv` varchar(63) DEFAULT NULL,
                                `et` varchar(63) DEFAULT NULL,
                                `airconditiontype` varchar(63) DEFAULT NULL,
                                `totalcheck` varchar(511) DEFAULT NULL,
                                `accidentscore` varchar(63) DEFAULT NULL,
                                `accidentdesc` varchar(511) DEFAULT NULL,
                                `outerscore` varchar(63) DEFAULT NULL,
                                `outerdesc` varchar(511) DEFAULT NULL,
                                `innerscore` varchar(63) DEFAULT NULL,
                                `innerdesc` varchar(511) DEFAULT NULL,
                                `safescore` varchar(63) DEFAULT NULL,
                                `safedesc` varchar(511) DEFAULT NULL,
                                `roadscore` varchar(63) DEFAULT NULL,
                                `roaddesc` varchar(511) DEFAULT NULL,
                                `desc` varchar(511) DEFAULT NULL,
                                `img_url` varchar(511) DEFAULT NULL,
                                PRIMARY KEY  (`id`)
                              ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
    params['mysqltable']='haoche51'
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
    caritem['url'] = item['url']
    caritem['carid'] = re.compile('\/').sub('',re.findall('\/\d+',item['url'])[0])
    caritem['grabtime'] = item['grabtime']
    caritem['pagetime'] = item['pagetime']  # new
    caritem['parsetime'] = time.strftime('%Y-%m-%d %X', time.localtime())
    # status
    caritem['status'] = str(re.findall('sale|sold', item["status"])[0])
    caritem['statusplus'] = item["status"]
    return caritem

def parse_keyinfo(dom):
    # caritem init
    caritem = dict()
    # keyinfro
    #caritem['carid'] = dom.xpath('//div[@class="rpt-cid"]/text()').re('\d+')[0] \
        #if dom.xpath('//div[@class="rpt-cid"]/text()') else '-'
    caritem['pagetitle'] = dom.xpath('//title/text()').extract_first()  # new
    caritem['title'] = dom.xpath('//h1[@id="detail-ctitle"]/text()').extract_first().strip() \
        if dom.xpath('//h1[@id="detail-ctitle"]/text()') else '-'
    if dom.xpath('//div[@class="ftlf emph"]/span/text()'):
        caritem['price1'] = dom.xpath('//div[@class="ftlf emph"]/span/text()').extract_first()
    elif dom.xpath('//div[@class="price"]/span[@class="emph"]/text()'):
        caritem['price1'] = dom.xpath('//div[@class="price"]/span[@class="emph"]/text()').extract_first() 
    else: "-"
    caritem['makeyear'] = re.compile(u'\u6b3e'+'|'+u'\u5e74').sub('',re.findall('\d+'+u'\u6b3e'+'|'+'\d+'+u'\u5e74',caritem['title'])[0]) \
        if re.findall('\d+'+u'\u6b3e'+'|'+'\d+'+u'\u5e74',caritem['title']) else "-" 
    return caritem

def parse_baseinfo(dom):
    # caritem init
    caritem = dict()
    # baseinfo
    if dom.xpath('//div[@class="autotit txac"]/h2/text()').extract_first():
        path = dom.xpath('//div[@class="autotit txac"]/h2/text()').extract_first()
        caritem['registerdate'] = re.compile('\.').sub('-',re.compile(u'\u4e0a\u724c').sub('',path.split('|')[0]))+'-01' \
            if len(path.split('|'))>=1 else "-"
        caritem['mileage'] = '.'.join(re.findall('\d+',path.split('|')[1])) \
            if len(path.split('|'))>=2 else "-"
        caritem['geartype'] = path.split('|')[2] \
            if len(path.split('|'))>=3 else "-"
        caritem['registerplace'] = re.compile(u'\u724c\u7167').sub('',path.split('|')[3]) \
            if len(path.split('|'))>=4 else "-"   
    caritem['years'] = "-"  # new
    caritem['mileperage'] = "-"  # new
    caritem['region'] = dom.xpath('//a[@class="citico"]/text()').extract_first() \
        if dom.xpath('//a[@class="citico"]/text()') else "-"
    caritem['province'] = "-"
    caritem['city'] = "-"
    caritem['dealplace'] = dom.xpath('//span[@id="kanche_addr"]/@data-city').extract_first() \
        if dom.xpath('//span[@id="kanche_addr"]/@data-city') else "-"
    caritem['changetimes'] = re.findall('\d+',dom.xpath('//div[@class="autotit txac"]/h2/text()[2]').extract_first())[0] \
        if dom.xpath('//div[@class="autotit txac"]/h2/text()[2]') else "-"
    caritem['changedate'] = '-'.join(dom.xpath('//div[@class="autotit txac"]/h2/i/text()').re('\d+')) \
        if dom.xpath('//div[@class="autotit txac"]/h2/i/text()') else "-"
    return caritem

def parse_certification(dom):
    # caritem init
    caritem = dict()
    # citification
    caritem['Insurance1'] = '-'.join(dom.xpath(u'//div[contains(text(),"\u4ea4\u5f3a\u9669\u6709\u6548\u671f")]/text()[1]').re('\d+')) \
        if dom.xpath(u'//div[contains(text(),"\u4ea4\u5f3a\u9669\u6709\u6548\u671f")]/text()[1]') else "-"
    caritem['Insurance2'] = re.compile(u'\u65e0').sub('',re.compile(u'\u5546\u4e1a\u9669').sub('',
        dom.xpath(u'//div[contains(text(),"\u4ea4\u5f3a\u9669\u6709\u6548\u671f")]/text()[2]').extract_first().split(u'\u3011')[1])) \
        if dom.xpath(u'//div[contains(text(),"\u4ea4\u5f3a\u9669\u6709\u6548\u671f")]/text()[2]') else "-"
    caritem['yearchecktime'] = re.compile(u'\u5546\u4e1a\u9669').sub('',dom.xpath(u'//div[contains(text(),"\u4ea4\u5f3a\u9669\u6709\u6548\u671f")]/text()[3]').extract_first().split(u'\u3011')[1]) \
        if dom.xpath(u'//div[contains(text(),"\u4ea4\u5f3a\u9669\u6709\u6548\u671f")]/text()[3]') else "-"
    caritem['carokcf'] = re.compile(u'\u5546\u4e1a\u9669').sub('',dom.xpath(u'//div[contains(text(),"\u4ea4\u5f3a\u9669\u6709\u6548\u671f")]/text()[4]').extract_first().split(u'\u3011')[1]) \
        if dom.xpath(u'//div[contains(text(),"\u4ea4\u5f3a\u9669\u6709\u6548\u671f")]/text()[4]') else "-"
    caritem['carcard'] = re.compile(u'\u5546\u4e1a\u9669').sub('',dom.xpath(u'//div[contains(text(),"\u4ea4\u5f3a\u9669\u6709\u6548\u671f")]/text()[5]').extract_first().split(u'\u3011')[1]) \
        if dom.xpath(u'//div[contains(text(),"\u4ea4\u5f3a\u9669\u6709\u6548\u671f")]/text()[5]') else "-"
    caritem['carinvoice'] = re.compile(u'\u5546\u4e1a\u9669').sub('',dom.xpath(u'//div[contains(text(),"\u4ea4\u5f3a\u9669\u6709\u6548\u671f")]/text()[6]').extract_first().split(u'\u3011')[1]) \
        if dom.xpath(u'//div[contains(text(),"\u4ea4\u5f3a\u9669\u6709\u6548\u671f")]/text()[6]') else "-"
    caritem['accident'] = "-"  # new
    caritem['useage'] = "-"  # new
    return caritem

def parse_dealor(dom):
    # caritem init
    caritem = dict()
    # dealer
    caritem['telphone'] = dom.xpath('//span[@class="tel-f00-18"]/text()').extract_first() \
        if dom.xpath('//span[@class="tel-f00-18"]/text()') else "-"
    caritem['dealor'] = re.compile(u'\u8f66\u4e3b'+'|'+u'\u62a5\u4ef7').sub('',dom.xpath('//div[@class="own-nme"]/text()').extract_first()) \
        if dom.xpath('//div[@class="own-nme"]/text()') else "-"  # new
    '''
    caritem['dealortype'] = "-"  # new
    caritem['dealorcompany'] = -"  # new
    caritem['dealorlocation'] = "-"  # new
    '''
    return caritem

def parse_createinfo(carinfocreate,website,mysqldb):
    carinfors_name = dict()
    carinfors_name = {u'\u4e0a\u5761\u8f85\u52a9': 'ci', u'\u4f9b\u6cb9\u65b9\u5f0f': 'fuelmethod', 
                      u'\u8f66\u8eab\u7a33\u5b9a\u63a7\u5236(ESP)': 'ch', u'\u8fdb\u6c14\u5f62\u5f0f': 'method', 
                      u'\u6700\u5927\u9a6c\u529b(Ps)': 'maxps', u'\u513f\u7ae5\u5ea7\u6905\u63a5\u53e3': 'bx', 
                      u'\u8f74\u8ddd(mm)': 'wheelbase', u'\u7ea7\u522b': 'level', 
                      u'\u591a\u529f\u80fd\u65b9\u5411\u76d8': 'cu', u'\u524d\u96fe\u706f': 'ef', 
                      u'\u6700\u5927\u626d\u77e9(N*m)': 'maxnm', u'\u65e0\u94a5\u5319\u8fdb\u5165': 'cc1', 
                      u'\u957f\u5bbd\u9ad8(mm)': 'lengthwh', u'\u8f66\u8eab\u7ed3\u6784': 'body', 
                      u'\u524d\u60ac\u67b6\u7c7b\u578b': 'fronthang', u'\u5382\u5546\u6307\u5bfc\u4ef7': 'guideprice', 
                      u'\u65e5\u95f4\u884c\u8f66\u706f': 'ec', u'\u611f\u5e94\u96e8\u5237': 'es', 
                      u'\u6c19\u6c14\u5927\u706f': 'ea', u'\u7535\u52a8\u5929\u7a97': 'dy', 
                      u'\u94dd\u5408\u91d1\u8f6e\u5708': 'hubtype', u'\u5168\u666f\u5929\u7a97': 'dz', 
                      u'ABS \u9632\u62b1\u6b7b': 'cd', u'\u540e\u89c6\u955c\u7535\u52a8\u8c03\u8282': 'em', 
                      u'\u65b9\u5411\u76d8\u6362\u6321': 'cv', u'\u540e\u6392\u5ea7\u6905\u653e\u5012\u65b9\u5f0f': 'dl', 
                      u'\u71c3\u6cb9\u6807\u53f7': 'fuelnumber', u'\u65e0\u94a5\u5319\u542f\u52a8': 'cc', 
                      u'\u4e3b/\u526f\u9a7e\u9a76\u5ea7\u5b89\u5168\u6c14\u56ca': 'bn_bo', u'\u524d\u8f6e\u80ce\u89c4\u683c': 'frontwheel', 
                      u'\u540e\u60ac\u67b6\u7c7b\u578b': 'backhang', u'\u771f\u76ae\u65b9\u5411\u76d8': 'cq', 
                      u'\u538b\u7f29\u6bd4': 'compress', u'\u4e3b/\u526f\u9a7e\u9a76\u5ea7\u7535\u52a8\u8c03\u8282': 'db_dc', 
                      u'\u6574\u5907\u8d28\u91cf(kg)': 'weight', u'\u52a9\u529b\u7c7b\u578b': 'assistanttype', 
                      u'LED \u5927\u706f': 'eb', u'\u53d1\u52a8\u673a': 'motor', 
                      u'\u524d/\u540e\u6392\u5934\u90e8\u6c14\u56ca': 'bs_bp', u'\u53d1\u52a8\u673a\u578b\u53f7': 'motortype', 
                      u'\u524d\u5236\u52a8\u5668\u7c7b\u578b': 'frontbrake', u'\u540e\u5236\u52a8\u5668\u7c7b\u578b': 'backbrake', 
                      u'\u53d8\u901f\u7bb1': 'gear', u'\u524d/\u540e\u6392\u5ea7\u6905\u52a0\u70ed': 'dh_di', 
                      u'\u9a71\u52a8\u65b9\u5f0f': 'driveway', u'\u5b9a\u901f\u5de1\u822a': 'et', 
                      u'\u884c\u674e\u7bb1\u5bb9\u79ef(L)': 'luggage', u'\u6392\u91cf(L)': 'output', 
                      u'\u771f\u76ae/\u4eff\u76ae\u5ea7\u6905': 'cw', u'\u6c7d\u7f38\u6570(\u4e2a)': 'lwvnumber', 
                      u'\u524d/\u540e\u7535\u52a8\u8f66\u7a97': 'ei_ej', u'\u7a7a\u8c03\u63a7\u5236\u65b9\u5f0f': 'airconditiontype', 
                      u'\u524d/\u540e\u6392\u4fa7\u6c14\u56ca': 'bq_br', u'\u540e\u8f6e\u80ce\u89c4\u683c': 'backwheel'}
    carinforsdf = pandas.DataFrame(carinfors_name.items(),columns=['name_cn','name_en'])
    if carinfocreate == True:
        carinforsdf.to_sql(name=website + '_carinfo', con=mysqldb, flavor='mysql',
                               if_exists='replace')
        carinfocreate = False
    return carinfors_name

def parse_carinfo1(dom):
    # caritem init
    caritem = dict()
    # carinfo
    if dom.xpath('//script[contains(text(),"brand_name")]/text()'):
        namelist = dom.xpath('//script[contains(text(),"brand_name")]/text()').extract_first()
        brandlocation = namelist.find('brand_name')
        classlocation = namelist.find('class_name')
        vehiclelocation = namelist.find('vehicle_id')
        if brandlocation!=-1 and classlocation!=-1:
            caritem['brand_name'] = namelist[brandlocation+12:classlocation-3].strip().strip("'")
            caritem['class_name'] = namelist[classlocation+12:vehiclelocation-3].strip().strip("'")
        else:
            caritem['brand_name'] = "-"
            caritem['class_name'] = "-"
    caritem['emission'] = re.compile(u'\u6392\u653e').sub('',dom.xpath('//div[@class="autotit txac"]/h2/span[@class="cspt"]/text()').extract_first()) \
            if dom.xpath('//div[@class="autotit txac"]/h2/span[@class="cspt"]/text()') else "-"
    caritem['color'] = dom.xpath(
        u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u8f66\u8eab\u989c\u8272")]/../text()').extract_first() \
        if dom.xpath(u'//div[@class="det-basinfor"]/ul/li/label[contains(text(),"\u8f66\u8eab\u989c\u8272")]/../text()') else "-"  # new
    caritem['guidepricetax'] = dom.xpath('//span[@class="txde"]/text()').extract_first() \
        if dom.xpath('//span[@class="txde"]/text()') else "-"
    caritem['newcartitle'] = "-"
    caritem['newcarurl'] = "-"  # new
    return caritem    
    
def parse_carinfo2(dom,carinfors_name):
    # caritem init
    caritem = dict()
    #carinfo
    mycarinfo=[]
    mys = dom.xpath('//div[@class ="parcon-box ftzm ptb20"]/div/ul/li/text()')
    for sel in mys:
         a=(sel.extract())
         mycarinfo.append(a)
    #Chinese carinfo
    carinfors_cn={}
    for i in range(0,len(mycarinfo)-1,2) :
        name = mycarinfo[i]
        info = mycarinfo[i+1]
        inforitem={name:info}
        carinfors_cn=dict(carinfors_cn,**inforitem)
    #right carinfo
    carinfors=dict()
    for name in carinfors_name.keys():
        if carinfors_cn.has_key(name):
            name_en = carinfors_name[name]
            infor=carinfors_cn[name]
            inforitem={name_en:infor}
            carinfors=dict(carinfors,**inforitem)
        else:
            name_en = carinfors_name[name]
            infor='-'
            inforitem={name_en:infor}
            carinfors=dict(carinfors,**inforitem)
    #caritem
    for name in carinfors.keys():
            caritem[name] = carinfors[name] 
    if caritem['lengthwh']== "-":
        caritem['length'] = "-"
        caritem['width'] = "-"
        caritem['height'] = "-"
    elif len(caritem['lengthwh'].split('*'))>=3:
        caritem['length'] = caritem['lengthwh'].split('*')[0]
        caritem['width'] = caritem['lengthwh'].split('*')[1]
        caritem['height'] = caritem['lengthwh'].split('*')[2]
    caritem['guideprice'] = re.compile(u'\uffe5'+'|'+u'\u4e07\u5143').sub('',caritem['guideprice'])
    caritem['gearnumber'] = re.compile(u'\u6321'+'|'+u'\u6863').sub('',re.findall('\d+'+u'\u6321'+'|'+'\d+'+u'\u6863',caritem['gear'])[0]) \
        if re.findall(u'\u6321'+'|'+u'\u6863',caritem['gear']) else '-'
    caritem['doors'] = re.compile(u'\u95e8').sub('',re.findall('\d+'+u'\u95e8',caritem['body'])[0]) \
        if re.findall('\d+'+u'\u95e8',caritem['body']) else '-'
    caritem['seats'] = re.compile(u'\u5ea7').sub('',re.findall('\d+'+u'\u5ea7',caritem['body'])[0]) \
        if re.findall('\d+'+u'\u5ea7',caritem['body']) else '-'
    caritem['bodystyle'] = re.findall(u'\u4e24\u53a2'+'|'+u'\u4e09\u53a2',caritem['body'])[0] \
        if re.findall(u'\u4e24\u53a2'+'|'+u'\u4e09\u53a2',caritem['body']) else '-'
    return caritem


def parse_otherinfo(dom):
    # caritem init
    caritem = dict()
    
    return caritem

def parse_checkpoints(dom):
    # caritem init
    caritem = dict()
    # desc
    descnames = {u'\u5185\u9970\u68c0\u6d4b': 'innerdesc', u'\u8bbe\u5907\u548c\u5b89\u5168\u6027': 'safedesc', 
                 u'\u4e8b\u6545\u6392\u67e5': 'accidentdesc', u'\u673a\u68b0\u548c\u8def\u6d4b': 'roaddesc', 
                 u'\u5916\u89c2\u68c0\u6d4b': 'outerdesc'}
    myname = dom.xpath('//h4[@class="dtc-h4"]')
    myinfo = dom.xpath('//div[@style="padding-top:6px;"]') 
    descnames_cn={}
    for i in range(0,5) :
        name=myname.xpath('text()').extract()[i].strip() if myname.xpath('text()') else '-'
        info=myinfo.xpath('text()').extract()[i].strip() if myinfo.xpath('text()') else '-'
        inforitem={name:info}
        descnames_cn=dict(descnames_cn,**inforitem)
    descnames_info=dict()
    for name in descnames.keys():
        if descnames_cn.has_key(name):
            name_en = descnames[name]
            infor=descnames_cn[name]
            inforitem={name_en:infor}
            descnames_info=dict(descnames_info,**inforitem)
        else:
            name_en = descnames[name]
            infor='-'
            inforitem={name_en:infor}
            descnames_info=dict(descnames_info,**inforitem)
    for name in descnames_info.keys():
        caritem[name] = descnames_info[name]
    #score
    scorenames = {u'\u5185\u9970\u68c0\u6d4b': 'innerscore', u'\u8bbe\u5907\u548c\u5b89\u5168\u6027': 'safescore', 
                  u'\u4e8b\u6545\u6392\u67e5': 'accidentscore', u'\u673a\u68b0\u548c\u8def\u6d4b': 'roadscore', 
                  u'\u5916\u89c2\u68c0\u6d4b': 'outerscore'}
    mys = dom.xpath('//div[@class="profile-scores"]') 
    scorenames_cn={}
    for i in range(0,5) :
        name=mys.xpath('ul/li/text()').extract()[i].strip() if mys.xpath('ul/li/text()') else '-'
        info=mys.xpath('ul/li/span/b/text()').extract()[i].strip() if mys.xpath('ul/li/span/b/text()') else '-'
        inforitem={name:info}
        scorenames_cn=dict(scorenames_cn,**inforitem)
    scorenames_info=dict()
    for name in scorenames.keys():
        if scorenames_cn.has_key(name):
            name_en = scorenames[name]
            infor=scorenames_cn[name]
            inforitem={name_en:infor}
            scorenames_info=dict(scorenames_info,**inforitem)
        else:
            name_en = scorenames[name]
            infor='-'
            inforitem={name_en:infor}
            scorenames_info=dict(scorenames_info,**inforitem)
    for name in scorenames_info.keys():
        caritem[name] = str(scorenames_info[name])
    #total
    caritem['totalcheck'] = dom.xpath('//div[@class="ckr-sug"]/text()').extract_first() \
        if dom.xpath('//div[@class="ckr-sug"]/text()') else "-"
    return caritem

def parse_desc(dom):
    # caritem init
    caritem = dict()
    # more desc
    caritem['desc'] = dom.xpath('//meta[@name="description"]/@content').extract_first() \
        if dom.xpath('//meta[@name="description"]/@content') else "-"  # new
    if len(caritem['desc']) > 500:
        caritem['desc'] = caritem['desc'][:500]
    caritem['img_url'] = dom.xpath('//img[@class="item-img"]/@src').extract_first() \
        if dom.xpath('//img[@class="item-img"]/@src') else "-"  # new
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
        caritem = dict(caritem, **parse_keyinfo(dom))
        # parse baseinfo:3
        caritem = dict(caritem, **parse_baseinfo(dom))
        # parse certification:4
        caritem = dict(caritem, **parse_certification(dom))
        # parse dealor:5
        caritem = dict(caritem, **parse_dealor(dom))
        # parse createinfo:6
        carinfors_name = parse_createinfo(carinfocreate,website,mysqldb)
        # parse carinfo:7
        caritem = dict(caritem, **parse_carinfo1(dom))
        caritem = dict(caritem, **parse_carinfo2(dom,carinfors_name))
        caritem = dict(caritem, **parse_otherinfo(dom))
        # parse checkpoints:8
        caritem = dict(caritem, **parse_checkpoints(dom))
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

# parse(0,200)
#ppexcut(8)





