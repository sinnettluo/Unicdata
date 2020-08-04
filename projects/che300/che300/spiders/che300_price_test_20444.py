#-*- coding: UTF-8 -*-
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
import json

website ='che300_price_test_20444'
spidername_new = 'che300_price_test_new'
spidername_update = 'che300_price_test_update_s'
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

    #pro_city select
    #brandselect
    def start_requests(self):
        #this month
        thismonth =datetime.date.today().month
        #modellist
        with open('blm/'+self.dbname+'/modellist.csv', 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            modellist = [row for row in reader]
        #citylist
        with open('blm/'+self.dbname+'/citylist.csv', 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            citylist = [row for row in reader]
        step=len(modellist)/self.parts+1
        starti = self.part * step
        if self.part==self.parts-1:
            step = len(modellist) - starti
        #urllist
        # for model in modellist:
        #     if model["salesdescid"] == "20444":
        #         index = modellist.index(model)

        for city in citylist[2:3]:
            for model in modellist:
                if model["salesdescid"] == "20444":
                    for year in range(1999,2019):
                        if year == "2018":
                            monthlist = range(1, datetime.datetime.now().month+1)
                        else:
                            monthlist = range(1,13)
                        for month in monthlist:
                            date = str(year)+'-'+str(month)
                            for mile in range(1,121)+[0.2]:
                                if mile%2==0:
                                    mile=mile/2
                                else:
                                    mile = float(mile)/2.0
                                url ="https://dingjia.che300.com/app/EvalResult/getPreSaleRate?callback=jQuery1830036377570742932575_1523857340152" \
                                     "&prov=" + str(city['provid']) +"&city=" + str(city['cityid']) + \
                                     "&brand=" + str(model['brandid']) + "&series=" + str(model['familyid']) + \
                                     "&model=" + str(model['salesdescid']) + "&regDate=" + date + "&mile=" + str(mile)
                                url1='https://dingjia.che300.com/app/EvalResult/allProvPrices?callback=jQuery1830036377570742932575_1523857340152' + \
                                     "&brand=" + str(model['brandid']) + "&series=" + str(model['familyid']) + \
                                     "&model=" + str(model['salesdescid']) + "&regDate=" + date + "&mile=" + str(mile)
                                if not (dfcheck(self.df, url, self.tag)):
                                    meta =dict()
                                    meta['provid']= city['provid']
                                    meta['cityid']= city['cityid']
                                    meta['salesdescid']= model['salesdescid']
                                    meta['regDate']= date
                                    meta['mile']= str(mile)
                                    yield  scrapy.Request(url=url, meta={"datainfo":meta},callback=self.parse)

                            if not (dfcheck(self.df, url1, self.tag)):
                                meta =dict()
                                meta['salesdescid']= model['salesdescid']
                                meta['regDate']= date
                                meta['mile']= str(mile)
                                yield  scrapy.Request(url=url1, meta={"datainfo":meta},callback=self.parse_allprov)

    def parse(self, response):
        item = che300_price()
        item = dict(item ,**response.meta['datainfo'])
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        item['status'] = md5(response.url).hexdigest()
        if response.xpath('//p/text()').re('\{\"success.*\}\]\}'):
            # dffile
            dffile(self.fa, response.url, self.tag)
            data = json.loads(response.xpath('//p/text()').re('\{\"success.*\}\]\}')[0])['success']
            item['price1'] = data[0]['price']
            item['price2'] = data[1]['price']
            item['price3'] = data[2]['price']
            item['price4'] = data[3]['price']
            item['price5'] = data[4]['price']
            item['price6'] = data[5]['price']
            item['price7'] = data[6]['price']
            item['saleRate1'] = data[0]['saleRate']
            item['saleRate2'] = data[1]['saleRate']
            item['saleRate3'] = data[2]['saleRate']
            item['saleRate4'] = data[3]['saleRate']
            item['saleRate5'] = data[4]['saleRate']
            item['saleRate6'] = data[5]['saleRate']
            item['saleRate7'] = data[6]['saleRate']
            item['saleDateRange1'] = data[0]['saleDateRange']
            item['saleDateRange2'] = data[1]['saleDateRange']
            item['saleDateRange3'] = data[2]['saleDateRange']
            item['saleDateRange4'] = data[3]['saleDateRange']
            item['saleDateRange5'] = data[4]['saleDateRange']
            item['saleDateRange6'] = data[5]['saleDateRange']
            item['saleDateRange7'] = data[6]['saleDateRange']
            yield item

    def parse_allprov(self, response):
        item = che300_price()
        item = dict(item, **response.meta['datainfo'])
        dffile(self.fa, response.url, self.tag)
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        item['status'] = md5(response.url + "-" + time.strftime('%Y-%m',time.localtime(time.time()))).hexdigest()
        item['datasave'] = response.xpath('//p/text()').extract_first()
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
