#-*- coding: UTF-8 -*-
import re
import scrapy
from ..items import che300_price
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
import MySQLdb
import json
import random

website ='che300_price_test_2019_update'
spidername_new = 'che300_price_test_new'
spidername_update = 'che300_price_test_update_old'
from scrapy.conf import settings
update_code = settings["UPDATE_CODE"]
#main
class CarSpider(scrapy.Spider):
    name = website
    allowed_domains = ["che300.com"]
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

        self.headers = {
            'user-agent': 'activity/3.4.2.18 (Linux; Android 7.0; RNE-AL00; Build/HUAWEIRNE-AL00)',
        }
    #pro_city select
    #brandselect
    def start_requests(self):
        #this month
        thismonth =datetime.date.today().month
        #modellist
        # with open('blm/'+self.dbname+'/modellist.csv', 'rb') as csvfile:
        #     reader = csv.DictReader(csvfile)
        #     modellist = [row for row in reader]
        # #citylist
        # with open('blm/'+self.dbname+'/citylist.csv', 'rb') as csvfile:
        #     reader = csv.DictReader(csvfile)
        #     citylist = [row for row in reader]
        # step=len(modellist)/self.parts+1
        # starti = self.part * step
        # if self.part==self.parts-1:
        #     step = len(modellist) - starti
        #urllist
        # for model in modellist:
        #     if model["salesdescid"] == "1127558":
        #         index = modellist.index(model)
        mysqlconnection = MySQLdb.connect("192.168.1.94", "root", "Datauser@2017", 'for_android', 3306)
        dbc = mysqlconnection.cursor()
        mysqlconnection.set_character_set('utf8')
        dbc.execute('SET NAMES utf8;')
        dbc.execute('SET CHARACTER SET utf8;')
        dbc.execute('SET character_set_connection=utf8;')

        sql = "select * from che300_for_test"
        dbc.execute(sql)
        res = dbc.fetchall()
        for row in res:
            devicd_id = int(random.random() * 100000000000000)
            str_list = list("AiYFDzzOetCTfRcEelKjETIGc4v5i1ohdmOSL0q8e9P")
            random.shuffle(str_list)
            device_token = ''.join(str_list) + "_"
            rlat = round(random.random() * 10, 2)
            rlng = round(random.random() * 100, 2)
            url1 = "https://dingjia.che300.com/app/EvalResult/newGetBaseEvalPrice?" \
                  "&prov=" + str(row[6]) + "&city=" + str(row[2]) + \
                  "&brand=" + str(row[1]) + "&series=" + str(row[8]) + \
                  "&model=" + str(row[5]) + "&regDate=" + row[7] + "&mile=" + str(row[4]) + "&sign=" + str(
                row[9]) + "&from=android&device_id=" + str(devicd_id)
            url1 = url1 + "&lat=%d&lng=%d" % (rlat, rlng)
            url1 = url1 + "&device_token=%s" % device_token
            if not (dfcheck(self.df, url1 + "-" + update_code, self.tag)):
                meta =dict()
                meta['salesdescid']= str(row[5])
                meta['regDate']= row[7]
                meta['mile']= str(row[4])
                yield scrapy.Request(url=url1, meta={"datainfo":meta}, headers=self.headers, callback=self.parse)

    def parse(self, response):
        item = che300_price()
        item = dict(item ,**response.meta['datainfo'])
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        item['status'] = md5(response.url + "-" + update_code).hexdigest()
        data = response.text
        data = re.sub(r'"highlight_config":"{"','"highlight_config":{"',data)
        data =re.sub(r'"}","name":','"},"name":',data)
        data = json.loads(data)
        # print(response.text)
        # if response.xpath('//p/text()').re('\{\"success.*\}\]\}'):
            # dffile
        # dffile(self.fa, response.url, self.tag)
        # data = json.loads(response.xpath('//p/text()').re('\{\"success.*\}\]\}')[0])['success']
        item['price1'] = data["success"]["evalResult"]["dealer_low_buy_price"]
        item['price2'] = data["success"]["evalResult"]["dealer_buy_price"]
        item['price3'] = data["success"]["evalResult"]["individual_low_sold_price"]
        item['price4'] = data["success"]["evalResult"]["individual_price"]
        item['price5'] = data["success"]["evalResult"]["dealer_low_sold_price"]
        item['price6'] = data["success"]["evalResult"]["dealer_price"]
        item['price7'] = data["success"]["evalResult"]["dealer_high_sold_price"]
        # item['saleRate1'] = data[0]['saleRate']
        # item['saleRate2'] = data[1]['saleRate']
        # item['saleRate3'] = data[2]['saleRate']
        # item['saleRate4'] = data[3]['saleRate']
        # item['saleRate5'] = data[4]['saleRate']
        # item['saleRate6'] = data[5]['saleRate']
        # item['saleRate7'] = data[6]['saleRate']
        # item['saleDateRange1'] = data[0]['saleDateRange']
        # item['saleDateRange2'] = data[1]['saleDateRange']
        # item['saleDateRange3'] = data[2]['saleDateRange']
        # item['saleDateRange4'] = data[3]['saleDateRange']
        # item['saleDateRange5'] = data[4]['saleDateRange']
        # item['saleDateRange6'] = data[5]['saleDateRange']
        # item['saleDateRange7'] = data[6]['saleDateRange']
        # print(item)
        yield item

    def parse_allprov(self, response):
        item = che300_price()
        item = dict(item, **response.meta['datainfo'])
        dffile(self.fa, response.url, self.tag)
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        item['status'] = md5(response.url + "-" + update_code).hexdigest()
        item['datasave'] = response.xpath('//p/text()').extract_first()
        # yield item


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
