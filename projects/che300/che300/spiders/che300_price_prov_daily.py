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

website ='che300_price_prov_daily_update_test'
spidername_new = 'che300_price_prov_daily_new'
spidername_update = 'che300_price_prov_daily_update_old'
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
        step=len(modellist)/self.parts+1
        starti = self.part * step
        if self.part==self.parts-1:
            step = len(modellist) - starti
        #urllist
        for model in modellist[starti:(starti+step)]:
                for year in range(int(model['min_reg_year']),int(model['max_reg_year'])+1):
                    # max_month = 12
                    # if year == "2018":
                    #     max_month = datetime.datetime.now().month
                    for month in (1, datetime.datetime.now().month):
                        date = str(year)+'-'+str(month)
                        mile = 0.1
                        url = 'https://dingjia.che300.com/app/EvalResult/allProvPrices?callback=jQuery18309705734921018707_1534391096144' + \
                               "&brand=" + str(model['brandid']) + "&series=" + str(model['familyid']) + \
                               "&model=" + str(model['salesdescid']) + "&regDate=" + date + "&mile=" + str(mile)
                        if not (dfcheck(self.df, url, self.tag)):
                            meta = dict()
                            meta['salesdescid'] = model['salesdescid']
                            meta['regDate'] = date
                            meta['mile'] = str(mile)
                            # headers = {
                            #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                            #     'Accept-Language': 'en',
                            #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
                            # }

                            yield scrapy.Request(url=url, meta={"datainfo": meta}, callback=self.parse_allprov)

    def parse_allprov(self, response):
        item = che300_price()
        item = dict(item, **response.meta['datainfo'])
        dffile(self.fa, response.url, self.tag)
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        if response.xpath('//p/text()'):
            item['datasave'] = response.xpath('//p/text()').extract_first()
            item['status'] = md5(item['datasave'].encode('utf-8')+item['url'] + "-" + update_code).hexdigest()
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
