#-*- coding: UTF-8 -*-
import scrapy
from ..items import che168_price
import time
from hashlib import md5
from SpiderInit import spider_original_Init
from SpiderInit import spider_new_Init
from SpiderInit import spider_update_Init
from SpiderInit import dfcheck
from SpiderInit import dffile
from Car_spider_update import update
import csv
import datetime
import json
import re

website ='che168_price_prov'
spidername_new = 'che168_price_prov_new'
spidername_update = 'che168_price_prov_update'

#main
class CarSpider(scrapy.Spider):
    name = website
    allowed_domains = ["che168.com"]
    def __init__(self,part=0, parts=1,*args,**kwargs):
        # args
        super(CarSpider, self).__init__(*args, **kwargs)
        # setting
        self.tag = 'original'
        self.counts = 0
        self.carnum = 20000000
        self.dbname = 'usedcar_evaluation'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df = 'none'
        self.fa = 'none'
        self.part=int(part)
        self.parts=int(parts)

    #pro_city select
    #brandselect
    def start_requests(self):
        #this month
        thismonth =datetime.date.today().month
        #modellist
        with open('blm/'+self.dbname+'/che168modellist.csv', 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            modellist = [row for row in reader]
        #citylist
        with open('blm/'+self.dbname+'/che168citylist.csv', 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            citylist = [row for row in reader]
        # valuelist
        with open('blm/' + self.dbname + '/che168valuelist.csv', 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            valuelist = [row for row in reader]
        step=len(modellist)/self.parts+1
        starti = self.part * step
        if self.part==self.parts-1:
            step = len(modellist) - starti
        #urllist
        for city in citylist:
            for model in modellist[starti:(starti+step)]:
                for year in range(int(model['min_reg_year']),int(model['max_reg_year'])+1):
                    for month in [1,5,6,12]:
                        date = str(year)+'/'+str(month)+'/01'
                        mile=1
                        #mileagelist = [1]
                        # for mile in mileagelist:
                        #     #4S置换GetPinGuData('2.03v', 'PingGuCallBack2', 'uahm10033');
                        #     #卖给个人GetPinGuData('2.09v','PingGuCallBack3','uahm10034');
                        #     #卖给车商GetPinGuData('2.04v','PingGuCallBack1','uahm10035');
                        #     #保障车GetPinGuData('2.07v','PingGuCallBack1','uahm10036');
                        #     #商家车GetPinGuData('2.08v','PingGuCallBack2','uahm10037');
                        #     #个人车GetPinGuData('2.09v','PingGuCallBack3','uahm10038');
                        value = valuelist[1]
                        print value
                        url='https://cacheapi.che168.com/Assess/UsedCarAssess.ashx?_appid=m.m&_sign=&_encoding=gb2312&pid='\
                        +str(city['provid']) +"&cid="+ str(city['cityid']) +"&mileage="+ str(mile) + \
                        "&firstregtime="+ date +"&specid="+ str(model['autohomeid']) +"&_appversion="+\
                        value['_appversion']+"&mark="+value['mark']+"&_callback="+value['_callback']
                        if not (dfcheck(self.df, url, self.tag)):
                            meta =dict()
                            meta['provid']= city['provid']
                            meta['cityid']= city['cityid']
                            meta['autohomeid']= model['autohomeid']
                            meta['regDate']= date
                            meta['milage']= str(mile)
                            meta['type']=value['type']
                            yield  scrapy.Request(url=url, meta={"datainfo":meta},callback=self.parse)

    def parse(self, response):
        item = che168_price()
        item = dict(item ,**response.meta['datainfo'])
        item['url'] = response.url
        if json.loads(response.xpath('//p/text()').re('\{.*\}')[0])['returncode'] == 0:
            # dffile
            dffile(self.fa, response.url, self.tag)
            data = json.loads(response.xpath('//p/text()').re('\{.*\}')[0])['result']
            item['price_range'] = data['referenceprice']
            item['price_low'] =  float(data['referenceprice'].split('-',1)[0])
            item['price_hig'] = float(data['referenceprice'].split('-',1)[1])
            item['price_mid'] = (item['price_low'] + item['price_hig']) / 2
            item['guideprice'] = str(data['newcarprice'])
            item['grabtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            item['status'] = md5(".".join(str(item.values()))).hexdigest()
            yield item

# new
class CarSpider_new(CarSpider):

    # basesetting
    name = spidername_new

    def __init__(self,part=0, parts=1,*args,**kwargs):
        # args
        super(CarSpider_new, self).__init__(**kwargs)
        # tag
        self.tag = 'new'
        # spider setting
        self.df = spider_new_Init(
            spidername=spidername_new,
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        filename = 'blm/' + self.dbname + '/' + spidername_new + ".blm"
        self.fa = open(filename, "a")
        self.part = int(part)
        self.parts = int(parts)

#update
class CarSpider_update(CarSpider,update):

    #basesetting
    name = spidername_update

    def __init__(self,part=0, parts=1,*args,**kwargs):
        # load
        super(CarSpider_update, self).__init__(**kwargs)
        #settings
        self.urllist = spider_update_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum
        )
        self.carnum = len(self.urllist)
        self.tag='update'
        self.part = int(part)
        self.parts = int(parts)
        #do
        super(update, self).start_requests()
