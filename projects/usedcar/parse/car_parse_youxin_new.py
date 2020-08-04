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
    website ='youxin'
    params =ParseInit(website)
    #mysql redefine
    params['createsql']="""CREATE TABLE IF NOT EXISTS `youxin` (
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
                                `makeyear` varchar(63) DEFAULT NULL,
                                `gen` varchar(63) DEFAULT NULL,
                                `registerdate` varchar(63) DEFAULT NULL,
                                `years` varchar(63) DEFAULT NULL,
                                `mileage` varchar(63) DEFAULT NULL,
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
                                `guidepricetax` varchar(63) DEFAULT NULL,
                                `newcartitle` varchar(127) DEFAULT NULL,
                                `newcarurl` varchar(127) DEFAULT NULL,
                                `geartype` varchar(63) DEFAULT NULL,
                                `emission` varchar(63) DEFAULT NULL,
                                `bodystyle` varchar(63) DEFAULT NULL,
                                `output` varchar(63) DEFAULT NULL,
                                `driveway` varchar(63) DEFAULT NULL,
                                `factoryname` varchar(63) DEFAULT NULL,
                                `hole_assurance` varchar(63) DEFAULT NULL,
                                `petrol` varchar(63) DEFAULT NULL,
                                `petrol1` varchar(63) DEFAULT NULL,
                                `stopyear` varchar(63) DEFAULT NULL,
                                `sparewheel` varchar(63) DEFAULT NULL,
                                `hubtype` varchar(63) DEFAULT NULL,
                                `hubtype_desc` varchar(63) DEFAULT NULL,
                                `backwheel` varchar(63) DEFAULT NULL,
                                `frontwheel` varchar(63) DEFAULT NULL,
                                `brake` varchar(63) DEFAULT NULL,
                                `backbrake` varchar(63) DEFAULT NULL,
                                `frontbrake` varchar(63) DEFAULT NULL,
                                `fulevolumn` varchar(63) DEFAULT NULL,
                                `luggage` varchar(63) DEFAULT NULL,
                                `fuelnumber` varchar(63) DEFAULT NULL,
                                `driveform` varchar(63) DEFAULT NULL,
                                `cylinder_hat` varchar(63) DEFAULT NULL,
                                `cylinder_body` varchar(63) DEFAULT NULL,
                                `maxtorque` varchar(63) DEFAULT NULL,
                                `maxnm` varchar(63) DEFAULT NULL,
                                `maxrpm` varchar(63) DEFAULT NULL,
                                `maxpower` varchar(63) DEFAULT NULL,
                                `maxps` varchar(63) DEFAULT NULL,
                                `trip` varchar(63) DEFAULT NULL,
                                `cylinder_bore` varchar(63) DEFAULT NULL,
                                `chassis` varchar(63) DEFAULT NULL,
                                `assistanttype` varchar(63) DEFAULT NULL,
                                `backhang` varchar(63) DEFAULT NULL,
                                `if_newcar` varchar(63) DEFAULT NULL,
                                `changedesc` varchar(63) DEFAULT NULL,
                                `repairinfo` varchar(63) DEFAULT NULL,
                                `body` varchar(63) DEFAULT NULL,
                                `seats` varchar(63) DEFAULT NULL,
                                `doors` varchar(63) DEFAULT NULL,
                                `weight` varchar(63) DEFAULT NULL,
                                `backgauge` varchar(63) DEFAULT NULL,
                                `frontgauge` varchar(63) DEFAULT NULL,
                                `wheelbase` varchar(63) DEFAULT NULL,
                                `heigh` varchar(63) DEFAULT NULL,
                                `width` varchar(63) DEFAULT NULL,
                                `length` varchar(63) DEFAULT NULL,
                                `axle` varchar(63) DEFAULT NULL,
                                `compress` varchar(63) DEFAULT NULL,
                                `fueltype` varchar(63) DEFAULT NULL,
                                `valve` varchar(63) DEFAULT NULL,
                                `lwvnumber` varchar(63) DEFAULT NULL,
                                `lwv` varchar(63) DEFAULT NULL,
                                `motortype` varchar(63) DEFAULT NULL,
                                `motorsize` varchar(63) DEFAULT NULL,
                                `motorlocation` varchar(63) DEFAULT NULL,
                                `gearnumber` varchar(63) DEFAULT NULL,
                                `fronthang` varchar(63) DEFAULT NULL,
                                `exhaust` varchar(63) DEFAULT NULL,
                                `valve_technology` varchar(63) DEFAULT NULL,
                                `desc` varchar(511) DEFAULT NULL,
                                `img_url` varchar(255) DEFAULT NULL,
                                 PRIMARY KEY  (`id`)
                              ) ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
    params['mysqltable']='youxin'
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
    caritem['title'] = dom.xpath('//div[@class="d-tit"]/div/h1/text()').extract_first().strip() if dom.xpath(
        '//div[@class="d-tit"]/div/h1/text()') else '-' 
    caritem['price1'] = '.'.join(dom.xpath('//div[@class="jiage"]/em/text()').re('\d+')) \
        if dom.xpath('//div[@class="jiage"]/em/text()') else '.'.join(dom.xpath('//div[@class="jiage"]/p/text()').re('\d+')) \
                                                            if dom.xpath('//div[@class="jiage"]/p/text()') else "-"
    caritem['pricetag'] = re.compile(u'\xa5').sub('',dom.xpath('//div[@class="jiage"]/text()').extract_first().strip()) \
        if dom.xpath('//div[@class="jiage"]/text()') else "-"
    caritem['makeyear'] = re.compile(u'\u6b3e').sub('',re.findall('\d+'+u'\u6b3e'+'|'+'\d+'+u'\u5e74',caritem['title'])[0]) \
        if re.findall('\d+'+u'\u6b3e'+'|'+u'\u5e74',caritem['title']) else "-" 
    return caritem

def parse_baseinfo(dom):
    # caritem init
    caritem = dict()
    # baseinfo
    caritem['registerdate'] = dom.xpath(
        u'//ul[@class="contit"]/li/span[contains(text(),"\u4e0a\u724c\u65f6\u95f4")]/../em/text()').extract_first()+'-01' \
        if dom.xpath(u'//ul[@class="contit"]/li/span[contains(text(),"\u4e0a\u724c\u65f6\u95f4")]/../em/text()') else "-"
    caritem['posttime'] = dom.xpath(
        u'//ul[@class="contit"]/li/span[contains(text(),"\u4e0a\u67b6\u65f6\u95f4")]/../em/text()').extract_first() \
        if dom.xpath(u'//ul[@class="contit"]/li/span[contains(text(),"\u4e0a\u67b6\u65f6\u95f4")]/../em/text()') else "-"
    caritem['years'] = "-"  # new
    caritem['mileage'] = re.compile(u'\u4e07\u516c\u91cc').sub('',dom.xpath(
        u'//ul[@class="contit"]/li/span[contains(text(),"\u8868\u663e\u91cc\u7a0b")]/../em/text()').extract_first()) \
        if dom.xpath(u'//ul[@class="contit"]/li/span[contains(text(),"\u8868\u663e\u91cc\u7a0b")]/../em/text()') else "-"
    if re.findall(u'\u516c\u91cc',caritem['mileage']):
        caritem['mileage']=str(float(re.compile(u'\u516c\u91cc').sub('',caritem['mileage']))/10000)
    #caritem['mileperage'] = "-"  # new
    caritem['region'] = "-"
    caritem['province'] = dom.xpath('//meta[@name="location"]/@content').extract_first().split(';')[0].split('=')[1] \
        if dom.xpath('//meta[@name="location"]/@content') else "zero"
    caritem['city'] = dom.xpath('//meta[@name="location"]/@content').extract_first().split(';')[1].split('=')[1] \
        if dom.xpath('//meta[@name="location"]/@content') else "-"
    caritem['dealplace'] = dom.xpath(
        u'//ul[@class="contit"]/li/span[contains(text(),"\u9500\u552e\u57ce\u5e02")]/../em/text()').extract_first() \
        if dom.xpath(u'//ul[@class="contit"]/li/span[contains(text(),"\u9500\u552e\u57ce\u5e02")]/../em/text()') else "-"
    caritem['changetimes'] = "-"
    caritem['changedate'] = "-"
    return caritem

def parse_certification(dom):
    # caritem init
    caritem = dict()
    # citification
    caritem['Insurance2'] = "-"
    caritem['carokcf'] = "-"
    caritem['carcard'] = "-"
    caritem['carinvoice'] = "-"
    caritem['accident'] = "-"  # new
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
    carinfors_name = {u'\u8f74\u8ddd': 'wheelbase', u'\u6c14\u7f38\u6392\u5217\u5f62\u5f0f': 'lwv', 
                      u'\u5e74\u68c0\u6709\u6548\u671f': 'yearchecktime', u'\u524d\u8f6e\u80ce\u89c4\u683c': 'frontwheel', 
                      u'\u6700\u5927\u529f\u7387\u8f6c\u901f': 'maxrpm', u'\u6cb9\u7bb1\u5bb9\u79ef': 'fulevolumn', 
                      u'\u4fdd\u9669\u5230\u671f\u65f6\u95f4': 'Insurance1', u'\u540e\u8f6e\u8ddd': 'backgauge', 
                      u'\u8fc7\u6237\u624b\u7eed': 'changedesc', u'\u8f66\u8eab\u7ed3\u6784': 'body', 
                      u'\u52a9\u529b\u7c7b\u578b': 'assistanttype', u'\u524d\u8f6e\u8ddd': 'frontgauge', 
                      u'\u53d1\u52a8\u673a\u7c7b\u578b': 'motortype', u'\u8f6e\u6bc2\u63cf\u8ff0': 'hubtype_desc', 
                      u'\u4f7f\u7528\u6027\u8d28': 'useage', u'\u5e74\u6b3e\u4ee3': 'gen', 
                      u'\u73af\u4fdd\u6807\u51c6': 'emission', u'\u6392\u6c14\u91cf': 'exhaust', 
                      u'\u6c14\u7f38\u6570': 'lwvnumber', u'\u53d1\u52a8\u673a\u578b\u53f7': 'motorsize', 
                      u'\u884c\u674e\u53a2\u5bb9\u79ef': 'luggage', u'\u7f38\u5f84': 'cylinder_bore', 
                      u'\u540e\u60ac\u6302\u7c7b\u578b': 'backhang', u'\u5de5\u4fe1\u90e8\u7efc\u5408\u6cb9\u8017': 'petrol', 
                      u'\u5e95\u76d8\u7ed3\u6784': 'chassis', u'\u524d\u60ac\u6302\u7c7b\u578b': 'fronthang', 
                      u'\u6700\u5927\u626d\u77e9\u8f6c\u901f': 'maxtorque', u'\u5bbd': 'width', 
                      u'\u505c\u4ea7\u65f6\u95f4': 'stopyear', u'\u71c3\u6cb9\u55b7\u5c04\u7c7b\u578b': 'fueltype', 
                      u'\u71c3\u6cb9\u6807\u53f7': 'fuelnumber', u'\u751f\u4ea7\u5382\u5546': 'factoryname', 
                      u'\u6574\u8f66\u8d28\u4fdd': 'hole_assurance', u'\u5b9e\u6d4b\u6cb9\u8017': 'petrol1', 
                      u'\u53d1\u52a8\u673a\u4f4d\u7f6e': 'motorlocation', u'\u7f38\u4f53\u6750\u8d28': 'cylinder_body', 
                      u'\u7f38\u76d6\u6750\u8d28': 'cylinder_hat', u'\u5ea7\u6905\u6570': 'seats', 
                      u'\u6700\u5927\u9a6c\u529b': 'maxps', u'\u6bcf\u7f38\u6c14\u95e8\u6570': 'valve', 
                      u'\u53d8\u901f\u7bb1\u578b\u53f7': 'gearnumber', u'\u9ad8': 'heigh', 
                      u'\u538b\u7f29\u6bd4': 'compress', u'\u6c14\u95e8\u6280\u672f': 'valve_technology', 
                      u'\u6574\u5907\u8d28\u91cf': 'weight', u'\u540e\u5236\u52a8\u7c7b\u578b': 'backbrake', 
                      u'\u6700\u5927\u626d\u77e9': 'maxnm', u'\u662f\u5426\u4e3a\u4e00\u624b\u8f66': 'if_newcar', 
                      u'\u52a8\u529b\u5f62\u5f0f': 'driveform', u'\u884c\u7a0b': 'trip', 
                      u'\u8f66\u95e8\u6570': 'doors', u'\u524d\u5236\u52a8\u7c7b\u578b': 'frontbrake', 
                      u'\u9a71\u52a8\u5f62\u5f0f': 'driveway', u'\u8f6e\u6bc2\u6750\u8d28': 'hubtype', 
                      u'\u9a7b\u8f66\u5236\u52a8\u7c7b\u578b': 'brake', u'\u8f66\u8f86\u989c\u8272': 'color', 
                      u'\u4fdd\u517b\u60c5\u51b5': 'repairinfo', u'\u5907\u80ce\u7c7b\u578b': 'sparewheel', 
                      u'\u51f8\u8f6e\u8f74\u5f62\u5f0f': 'axle', u'\u53d8\u901f\u7bb1\u7c7b\u578b': 'geartype', 
                      u'\u6700\u5927\u529f\u7387': 'maxpower', u'\u957f': 'length', 
                      u'\u540e\u8f6e\u80ce\u89c4\u683c': 'backwheel'}
    carinforsdf = pandas.DataFrame(carinfors_name.items(),columns=['name_cn','name_en'])
    if carinfocreate == True:
        carinforsdf.to_sql(name=website + '_carinfo', con=mysqldb, flavor='mysql',
                               if_exists='replace')
        carinfocreate = False
    return carinfors_name
        
def parse_carinfo2(dom,carinfors_name):
    caritem = dict()
    mycarinfo=[]
    l_mys = dom.xpath('//div[@class="msg fl"]')[:6].xpath('table/tr/td/text()')
    for sel in l_mys:
         l_info=(sel.extract())
         mycarinfo.append(l_info)
         
    r_mys = dom.xpath('//div[@class="msg fr"]')[:7].xpath('table/tr/td/text()')  
    for sel in r_mys:
         r_info=(sel.extract())
         mycarinfo.append(r_info)
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
    caritem['bodystyle'] = re.findall(u'\u4e09\u53a2'+'|'+u'\u4e24\u53a2',caritem['body'])[0] \
        if re.findall(u'\u4e09\u53a2'+'|'+u'\u4e24\u53a2',caritem['body']) else "-"
    return caritem
def parse_carinfo1(dom):
    # caritem init
    caritem = dict()
    # carinfo
    pagetitle=dom.xpath('//title/text()').extract_first()
    if len(pagetitle.split(u'\u3011'))>=2:
        if len(pagetitle.split(u'\u3011')[1].split(' '))>=2:
            brandlocation = pagetitle.split(u'\u3011')[1].split(' ')[0].find(u'\u4e8c\u624b')
            classlocation = pagetitle.split(u'\u3011')[1].split(' ')[1].find(u'\u4e8c\u624b')
            if brandlocation!=-1:
                caritem['brand_name'] = pagetitle.split(u'\u3011')[1].split(' ')[0][brandlocation + 2:]
            if classlocation!=-1:
                caritem['class_name'] = pagetitle.split(u'\u3011')[1].split(' ')[1][:classlocation]
            else:
                caritem['class_name'] = pagetitle.split(u'\u3011')[1].split(' ')[1]
    caritem['output'] = re.compile('L|T').sub('',dom.xpath(
        u'//ul[@class="contit"]/li/span[contains(text(),"\u6392\u91cf")]/../em/text()').extract_first()) \
        if dom.xpath(u'//ul[@class="contit"]/li/span[contains(text(),"\u6392\u91cf")]/../em/text()') else "-"
    caritem['guideprice'] = "-"
    caritem['guidepricetax'] = '.'.join(dom.xpath('//div[@class="wan_2"]/span/del/text()').re('\d+')) \
        if dom.xpath('//div[@class="wan_2"]/span/del/text()') else '.'.join(dom.xpath('//div[@class="d-list"]/div/div/p/del/text()').re('\d+')) \
                                                                    if dom.xpath('//div[@class="d-list"]/div/div/p/del/text()') else "-"
    caritem['newcartitle'] = "-"  # new
    caritem['newcarurl'] = '-'  # new
    return caritem

def parse_otherinfo(dom):
    # caritem init
    caritem = dict()
   
    return caritem

def parse_checkpoints( dom):
    # caritem init
    caritem = dict()
    
    return caritem

def parse_desc( dom):
    # caritem init
    caritem = dict()
    # more desc
    caritem['desc'] = dom.xpath('//span[@id="php_send_mobile"]/text()').extract_first() \
        if dom.xpath('//span[@id="php_send_mobile"]/text()') else "-"
    if len(caritem['desc']) > 500:
        caritem['desc'] = caritem['desc'][:500]
    caritem['img_url'] = dom.xpath('//div[@class="d-photo img-album"]/a[@href="javascript:void(0)"]/img/@src').extract_first() \
        if dom.xpath('//div[@class="d-photo img-album"]/a[@href="javascript:void(0)"]/img/@src') else "-"  # new
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
        # if dom.xpath('//div[@class="con"]'):
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
            #             pass
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





