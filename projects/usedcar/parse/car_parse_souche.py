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
    website ='souche'
    params =ParseInit(website)
    #mysql redefine
    params['createsql']="""CREATE TABLE IF NOT EXISTS `souche` (
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
                                `statusplus` varchar(511) DEFAULT NULL,
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
                                `geartype` varchar(63) DEFAULT NULL,
                                `emission` varchar(63) DEFAULT NULL,
                                `weigth` varchar(63) DEFAULT NULL,
                                `doors` varchar(63) DEFAULT NULL,
                                `seats` varchar(63) DEFAULT NULL,
                                `hubtype` varchar(63) DEFAULT NULL,
                                `gearnum` varchar(63) DEFAULT NULL,
                                `lengthwh` varchar(63) DEFAULT NULL,
                                `length` varchar(63) DEFAULT NULL,
                                `width` varchar(63) DEFAULT NULL,
                                `height` varchar(63) DEFAULT NULL,
                                `wheelbase` varchar(63) DEFAULT NULL,
                                `body` varchar(63) DEFAULT NULL,
                                `petrol_permileage` varchar(63) DEFAULT NULL,
                                `luggage` varchar(63) DEFAULT NULL,
                                `fulevolumn` varchar(63) DEFAULT NULL,
                                `fueltype` varchar(63) DEFAULT NULL,
                                `fuelnumber` varchar(511) DEFAULT NULL,
                                `output` varchar(63) DEFAULT NULL,
                                `method` varchar(63) DEFAULT NULL,
                                `maxnm` varchar(63) DEFAULT NULL,
                                `power` varchar(63) DEFAULT NULL,
                                `masspeed` varchar(255) DEFAULT NULL,
                                `accelerate` varchar(63) DEFAULT NULL,
                                `driveway` varchar(127) DEFAULT NULL,
                                `cp` varchar(63) DEFAULT NULL,
                                `fronthang` varchar(127) DEFAULT NULL,
                                `backhang` varchar(63) DEFAULT NULL,
                                `frontbrake` varchar(127) DEFAULT NULL,
                                `backbrake` varchar(63) DEFAULT NULL,
                                `frontwheel` varchar(127) DEFAULT NULL,
                                `backwheel` varchar(127) DEFAULT NULL,
                                `desc` varchar(1023) DEFAULT NULL,
                                `img_url` varchar(511) DEFAULT NULL,
                                PRIMARY KEY  (`id`)
                              ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
    params['mysqltable']='souche'
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
    caritem['url'] = item["url"]
    caritem['grabtime'] = item["grabtime"]
    caritem['pagetime'] = item["pagetime"]  # new
    caritem['parsetime'] = time.strftime('%Y-%m-%d %X', time.localtime())
    # statusplus
    caritem['statusplus'] = item["status"]
    return caritem

def parse_keyinfo(dom):
    # caritem init
    caritem = dict()
    # keyinfro
    caritem['carid'] = dom.xpath('//input[@name="carId"]/@value').extract_first() \
        if dom.xpath('//input[@name="carId"]/@value') else '-'  # new
    caritem['pagetitle'] = dom.xpath('//title/text()[1]').extract_first() \
        if dom.xpath('//title/text()[1]') else '-'  # new
    caritem['title'] = dom.xpath('//div[@class="main-top"]/h1/ins/text()').extract_first().strip() \
        if dom.xpath('//div[@class="main-top"]/h1/ins/text()') else '-'
    caritem['price1'] = re.compile(u'\uffe5' + '|' + u'\u4e07').sub('',dom.xpath('//div[@class="detail_price_left clearfix"]/em/text()').extract_first()) \
        if dom.xpath('//div[@class="detail_price_left clearfix"]/em/text()') else "-"
    caritem['makeyear'] = re.compile(u'\u6b3e').sub('',re.findall('\d+'+u'\u6b3e'+'|'+u'\u5e74',caritem['title'])[0]) \
        if re.findall('\d+'+u'\u6b3e'+'|'+u'\u5e74',caritem['title']) else "-"
    # status
    caritem['status'] = dom.xpath('//ins[@class="detail-no hook-work-off"]/text()').extract_first() \
        if dom.xpath('//ins[@class="detail-no hook-work-off"]/text()') else '-'
    return caritem

def parse_baseinfo(dom):
    # caritem init
    caritem = dict()
    # baseinfo
    caritem['registerdate'] = dom.xpath(u'//div[@class="car_detail clearfix"]/div[contains(text()[2],"\u9996\u6b21\u4e0a\u724c")]/strong/text()').extract_first() + '-01' \
        if dom.xpath(u'//div[@class="car_detail clearfix"]/div[contains(text()[2],"\u9996\u6b21\u4e0a\u724c")]/strong/text()') else "-"
    caritem['years'] = "-"  # new
    caritem['mileage'] = re.compile(u'\u4e07\u516c\u91cc').sub('',dom.xpath(u'//div[@class="car_detail clearfix"]/div[contains(text()[2],"\u884c\u9a76\u91cc\u7a0b")]/strong/text()').extract_first()) \
        if dom.xpath(u'//div[@class="car_detail clearfix"]/div[contains(text()[2],"\u884c\u9a76\u91cc\u7a0b")]/strong/text()') else "-"
    caritem['mileperage'] = "-"  # new
    caritem['region'] = dom.xpath(u'//div[@class="car_detail clearfix"]/div[contains(text()[2],"\u6240\u5728\u5730")]/strong/text()').extract_first() \
        if dom.xpath(u'//div[@class="car_detail clearfix"]/div[contains(text()[2],"\u6240\u5728\u5730")]/strong/text()') else "-"
    caritem['province'] = "-"
    caritem['city'] = "-"
    caritem['dealplace'] = dom.xpath(u'//div[@class="car_detail clearfix"]/div[contains(text()[2],"\u6240\u5728\u5730")]/strong/text()').extract_first() \
        if dom.xpath(u'//div[@class="car_detail clearfix"]/div[contains(text()[2],"\u6240\u5728\u5730")]/strong/text()') else "-"
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
    caritem['useage'] = "-"  # new
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

def parse_createinfo(carinfocreate,website,mysqldb):
    carinfors_name = dict()

    carinfors_name = {u'\u8f6c\u5411\u7cfb\u7edf': 'cp', u'\u8fdb\u6c14\u5f62\u5f0f': 'method', u'\u540e\u8f6e\u80ce\u89c4\u683c(mm)': 'backwheel',
                      u'\u540e\u60ac\u6302': 'backhang', u'\u8f74\u8ddd(mm)': 'wheelbase', u'\u6574\u5907\u8d28\u91cf(kg)': 'weigth', 
                      u'\u529f\u7387(kw)': 'power', u'\u767e\u516c\u91cc\u6cb9\u8017(L)': 'petrol_permileage', u'\u5ea7\u4f4d\u6570': 'seats',
                      u'\u6700\u5927\u626d\u77e9(N\xb7m)': 'maxnm', u'\u71c3\u6cb9': 'fueltype', u'\u53d8\u901f\u7bb1': 'geartype',
                      u'\u5b98\u65b90-100km/h\u52a0\u901f(s)': 'accelerate', u'\u8f66\u578b': 'body', u'\u8f6e\u6bc2\u6750\u6599': 'hubtype',
                      u'\u6700\u9ad8\u8f66\u901f(km/h)': 'masspeed', u'\u957f*\u5bbd*\u9ad8(mm*mm*mm)': 'lengthwh',u'\u9a71\u52a8\u65b9\u5f0f': 'driveway', 
                      u'\u524d\u5236\u52a8': 'frontbrake', u'\u884c\u674e\u7bb1\u5bb9\u79ef(L)': 'luggage',u'\u6392\u653e\u6807\u51c6': 'emission', 
                      u'\u524d\u60ac\u6302': 'fronthang', u'\u6392\u91cf(L)': 'output', u'\u6cb9\u7bb1\u5bb9\u79ef(L)': 'fulevolumn', 
                      u'\u524d\u8f6e\u80ce\u89c4\u683c(mm)': 'frontwheel', u'\u8f66\u95e8\u6570': 'doors',u'\u53d8\u901f\u7bb1\u6863\u4f4d': 'gearnum', 
                      u'\u71c3\u6cb9\u6807\u53f7': 'fuelnumber', u'\u8f66\u8f86\u989c\u8272': 'color',u'\u540e\u5236\u52a8': 'backbrake'}
    carinforsdf = pandas.DataFrame(carinfors_name.items(),columns=['name_cn','name_en'])
    #carinforsdf = pandas.DataFrame(carinfors_name)
    if carinfocreate == True:
        carinforsdf.to_sql(name=website + '_carinfo', con=mysqldb, flavor='mysql',
                               if_exists='replace')
        carinfocreate = False
    return carinfors_name

def parse_carinfo2(dom,carinfors_name):
    # caritem init
    caritem = dict()
    mys = dom.xpath('//div[@class="param-content"]/table/tbody/tr') 
    #Chinese carinfo
    carinfors_cn={}
    for sel in mys :
        name=sel.xpath('th/text()').extract_first() if sel.xpath('th/text()') else '-'
        info=sel.xpath('td[2]/text()').extract_first() if sel.xpath('td[2]/text()') else '-'
        inforitem={name:info}
        carinfors_cn=dict(carinfors_cn,**inforitem)
    #
    carinfors=dict()
    for name in carinfors_name.keys():
        if carinfors_cn.has_key(name):
            name_en = carinfors_name[name]
            infor=carinfors_cn[name]
            inforitem={name_en:infor}
            carinfors=dict(carinfors,**inforitem)
        else:
            continue
    
    for name in carinfors.keys():
            caritem[name] = carinfors[name]   
    #special cases
    caritem['body'] = re.compile(u'\u8f66').sub('',caritem['body'])
    if caritem['lengthwh']=="- -" or caritem['lengthwh']=="**" or caritem['lengthwh']=="-":
        caritem['length'] = "-"
        caritem['width'] = "-"
        caritem['height'] = "-"
    else:
        caritem['length'] = caritem['lengthwh'].split('*')[0]
        caritem['width'] = caritem['lengthwh'].split('*')[1]
        caritem['height'] = caritem['lengthwh'].split('*')[2]
    caritem['doors'] = re.compile(u'\u95e8').sub('',caritem['doors'])
    caritem['seats'] = re.compile(u'\u5ea7').sub('',caritem['seats'])
    caritem['gearnum'] = re.compile(u'\u6863' + '|' + u'\u6321').sub('',caritem['gearnum'])
    caritem['hubtype'] = re.compile('\d+').sub('',caritem['hubtype'])
    caritem['petrol_permileage'] = re.compile(u'\u5de5\u4fe1\u90e8\u672a\u516c\u5e03').sub('',caritem['petrol_permileage'])
    return caritem

def parse_carinfo1(dom):
    # caritem init
    caritem = dict()
    # carinfo
    head=''.join(dom.xpath('//div[@class="detail-map"]/a/text()').extract())
    if len(head.split('>'))>=5:
        if len(head.split('>')[-1])==0:
                caritem['brand_name'] = head.split('>')[-3].strip()
                caritem['class_name'] = head.split('>')[-2].strip()
        else:
                caritem['brand_name'] = head.split('>')[-2].strip()
                caritem['class_name'] = head.split('>')[-1].strip()
    else:
        caritem['brand_name'] = "-"
        caritem['class_name'] = "-"
    if len(set(caritem['brand_name']) & set(caritem['class_name']))==len(caritem['brand_name']):
        caritem['class_name'] = re.compile(caritem['brand_name']).sub('',caritem['class_name'])
    caritem['emission'] = dom.xpath(u'//div[@class="car_detail clearfix"]/div[contains(text()[2],"\u6392\u653e\u6807\u51c6")]/strong/text()').extract_first() \
        if dom.xpath(u'//div[@class="car_detail clearfix"]/div[contains(text()[2],"\u6392\u653e\u6807\u51c6")]/strong/text()') else "-"
    if dom.xpath('//div[@class="detail_price_right"]/label/text()').extract_first() != None:
        if len(re.findall(u'\u5e02\u573a\u4ef7',dom.xpath('//div[@class="detail_price_right"]/label/text()').extract_first())[0])==3:
            caritem['guideprice'] = str(re.findall('\d.+\d',dom.xpath('//div[@class="detail_price_right"]/label/text()').extract_first())[0])
            caritem['tax'] = "0"
        else:
            caritem['guideprice'] = "0"
            caritem['tax'] = "0"
    elif dom.xpath('//div[@class="detail_price_right "]/label/text()').extract_first() != None:
        if len(dom.xpath('//div[@class="detail_price_right "]/label/text()').extract_first().split('+'))>=2:
            caritem['guideprice'] = str(''.join(re.findall('\d+[.+\d+]?',dom.xpath('//div[@class="detail_price_right "]/label/text()').extract_first().split('+')[0])))
            caritem['tax'] = str(''.join(re.findall('\d+[.+\d+]?',dom.xpath('//div[@class="detail_price_right "]/label/text()').extract_first().split('+')[1])))
        else:
            caritem['guideprice'] = "0"
            caritem['tax'] = "0"
    else:
        caritem['guideprice'] = "0"
        caritem['tax'] = "0"
    caritem['guidepricetax'] = float(caritem['guideprice'])+float(caritem['tax'])
    caritem['newcartitle'] = "-"  # new
    caritem['newcarurl'] = '-'  # new
    return caritem

def parse_otherinfo(dom,carinfors_name):
    # caritem init
    caritem = dict()
    '''
    mys = response.xpath('//div[@class="param-content"]/table/tbody/tr') 
    carinfors_cn={}
    for sel in mys :
        name=sel.xpath('th/text()').extract_first() if sel.xpath('th/text()') else '-'
        info=sel.xpath('td[2]/text()').extract_first() if sel.xpath('td[2]/text()') else '-'
        inforitem={name:info}
        carinfors_cn=dict(carinfors_cn,**inforitem)
    
    carinfors=dict()
    for name in carinfors_name.keys():
    	if carinfors_cn.has_key(name):
        name_en =carinfors_name[name]
        infor=carinfors_cn[name]
        inforitem={name_en:infor}
        carinfors=dict(carinfors,**inforitem)
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
    # more desc
    caritem['desc'] = dom.xpath('//div[@class="host-say j-host-say"]/p/text()').extract_first().strip().encode('gbk','ignore').decode('gbk','ignore') \
        if dom.xpath('//div[@class="host-say j-host-say"]/p/text()') else "-"  
    if len(caritem['desc'])>=1000:
        caritem['desc']=caritem['desc'][0:1000]
    caritem['img_url'] = dom.xpath('//li[@class="photoActive"]/img/@src').extract_first() \
        if dom.xpath('//li[@class="photoActive"]/img/@src') else "-"  # new
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
        #logging.log(msg="counts:"+str(counts)+','+i['url'], level=logging.INFO)
        #parse original:1
        # caritem init
        # parse original:1
        caritem = parse_original(item)
        # parse keyinfo:2
        content = item['datasave'][1]
        dom = scrapy.selector.Selector(text=content)
        # if dom.xpath('//div[@id="pageError"]'):
        #     continue
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
        #caritem = dict(caritem, **parse_otherinfo(dom,carinfors_name))
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


#parse(0,1000)
# ppexcut(8)



