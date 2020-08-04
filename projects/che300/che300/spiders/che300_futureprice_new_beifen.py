# -*- coding: UTF-8 -*-
import re

import scrapy
import MySQLdb
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
import json
from scrapy.conf import settings

# update_code = settings["UPDATE_CODE"]
update_code = time.strftime("%Y%m%d", time.localtime())

website = 'che300_futureprice_update'
spidername_new = 'che300_futureprice_new'
spidername_update = 'che300_futureprice_update_old'


# main
class CarSpider(scrapy.Spider):
    name = website

    # allowed_domains = ["che300.com"]
    def __init__(self, part=0, parts=1, *args, **kwargs):
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
        self.part = int(part)
        self.parts = int(parts)



    def structure_http(self, result):
        # "(2, 'price22.1863101943prov3city3mile0.1model11805year2006month6typedealer_price', 'D46B1542376EE8F1')"
        # "https://dingjia.che300.com/demo/evaluate/getPriceTrendSign?mile=3&sign=5061D26526E610B6&city=3&prov=3&year=2018&month=1&price=33.2503327331714&app_type=android_price&type=dealer_price&model=1146056"
        price = re.search(r"price(.*?)prov", result[1]).group(1)
        sign = result[2]
        mile = re.search(r'mile(.*?)mode', result[1]).group(1)
        city = re.search(r'city(.*?)mile', result[1]).group(1)
        prov = re.search(r'prov(.*?)city', result[1]).group(1)
        year = re.search(r'year(.*?)month', result[1]).group(1)
        month = re.search(r'month(.*?)type', result[1]).group(1)
        model = re.search(r'model(.*?)year', result[1]).group(1)
        # print(price, sign, mile, city, prov, year, month, model)

        meta = dict()
        meta['provid'] = prov
        meta['cityid'] = city
        meta['salesdescid'] = model
        meta['regDate'] = str(year) + "-" + str(month)
        meta['mile'] = mile




        http = "https://dingjia.che300.com/demo/evaluate/getPriceTrendSign?mile={}&sign={}&city={}&prov={}&year={}&month={}&price={}&app_type=android_price&type=dealer_price&model={}" \
            .format(mile, sign, city, prov, year, month, price, model)
        # print(http)
        return (http, meta)

    def start_requests(self):

        mysqlconnection = MySQLdb.connect("192.168.1.94", "root", "Datauser@2017", 'for_android', 3306)
        dbc = mysqlconnection.cursor()
        mysqlconnection.set_character_set('utf8')
        dbc.execute('SET NAMES utf8;')
        dbc.execute('SET CHARACTER SET utf8;')
        dbc.execute('SET character_set_connection=utf8;')

        count = dbc.execute('select * from che300_trend')
        print("一共%d条" % count)
        for i in range(count):
            result = dbc.fetchone()
            print result
            url, meta = self.structure_http(result)

            yield scrapy.Request(url=url, meta={"datainfo":meta}, callback=self.parse)

    # pro_city select
    # brandselect
    # def start_requests(self):
    #     #this month
    #     thismonth =datetime.date.today().month
    #     #modellist
    #     with open('blm/'+self.dbname+'/modellist.csv', 'rb') as csvfile:
    #         reader = csv.DictReader(csvfile)
    #         modellist = [row for row in reader]
    #     #citylist
    #     with open('blm/'+self.dbname+'/citylist.csv', 'rb') as csvfile:
    #         reader = csv.DictReader(csvfile)
    #         citylist = [row for row in reader]
    #     step=len(modellist)/self.parts+1
    #     starti = self.part * step
    #     if self.part==self.parts-1:
    #         step = len(modellist) - starti
    #     #urllist
    #     for city in citylist[2:3]:
    #         for model in modellist[starti:(starti+step)]:
    #             for year in range(int(model['min_reg_year']),int(model['max_reg_year'])+1):
    #                 if year == 2018:
    #                     for month in range(1, datetime.datetime.now().month+1):
    #                         date = str(year)+'-'+str(month)
    #                         mile = 0.2
    #                         url = "https://dingjia.che300.com/app/EvalResult/getResidualAnalysis?prov="\
    #                               + str(city['provid']) +"&city="+ str(city['cityid']) +"&series="+ str(model['familyid']) +"&model="+ \
    #                               str(model['salesdescid']) +"&regDate="+ date  +"&mile="+str(mile)
    #                         if not (dfcheck(self.df, url, self.tag)):
    #                             meta =dict()
    #                             meta['provid']= city['provid']
    #                             meta['cityid']= city['cityid']
    #                             meta['salesdescid']= model['salesdescid']
    #                             meta['regDate']= date
    #                             meta['mile']= str(mile)
    #                             yield  scrapy.Request(url=url, meta={"datainfo":meta},callback=self.parse)
    #                 else:
    #                     for month in range(1, 13):
    #                         date = str(year)+'-'+str(month)
    #                         mile = 0.2
    #                         url = "https://dingjia.che300.com/app/EvalResult/getResidualAnalysis?prov="\
    #                               + str(city['provid']) +"&city="+ str(city['cityid']) +"&series="+ str(model['familyid']) +"&model="+ \
    #                               str(model['salesdescid']) +"&regDate="+ date  +"&mile="+str(mile)
    #                         if not (dfcheck(self.df, url, self.tag)):
    #                             meta =dict()
    #                             meta['provid']= city['provid']
    #                             meta['cityid']= city['cityid']
    #                             meta['salesdescid']= model['salesdescid']
    #                             meta['regDate']= date
    #                             meta['mile']= str(mile)
    #                             yield  scrapy.Request(url=url, meta={"datainfo":meta},callback=self.parse)

    def parse(self, response):
        item = che300_price()
        item = dict(item, **response.meta['datainfo'])
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        item['status'] = md5(response.url + "-" + update_code).hexdigest()
        # if response.xpath('//p/text()').re('\{\"success.*\}\]\}'):
        #     # dffile
        #     dffile(self.fa, response.url, self.tag)
        data = json.loads(response.text)['data']
        for dataitem in data:
            year = str(3*data.index(dataitem))
            price = dataitem['eval_price']
            # cols = 'year_' + str(year)
            item[year] = price
        yield item
        # print(item)

# new
class CarSpider_new(CarSpider):
    # basesetting
    name = spidername_new

    def __init__(self, part=0, parts=1, *args, **kwargs):
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


# update
class CarSpider_update(CarSpider, update):
    # basesetting
    name = spidername_update

    def __init__(self, part=0, parts=1, *args, **kwargs):
        # load
        super(CarSpider_update, self).__init__(**kwargs)
        # settings
        self.urllist = spider_update_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum
        )
        self.carnum = len(self.urllist)
        self.tag = 'update'
        self.part = int(part)
        self.parts = int(parts)
        # do
        super(update, self).start_requests()
