# -*- coding: utf-8 -*-
import scrapy
import time
from ganji.items import ChedaoshanqianItem
import logging
from hashlib import md5
from SpiderInit import spider_original_Init
from SpiderInit import spider_new_Init
from SpiderInit import spider_update_Init
from SpiderInit import dfcheck
from SpiderInit import dffile
from Car_spider_update import update
import json
from scrapy.conf import settings


website ='chedaoshanqian'
spidername_new = 'chedaoshanqian_new'
spidername_update = 'chedaoshanqian_update'


class CarSpider(scrapy.Spider):

    name = website
    #allowed_domains = ["dealer.auto.sohu.com"]
    start_urls = [
        "http://c.chedaoshanqian.com/regions/cities/firstLetter"
    ]



    def __init__(self,**kwargs):
        print "test"
        # problem report
        self.counts = 0
        self.carnum = 500000
        # Mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'usedcar', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    #city
    def parse(self, response):
        jsdata = json.loads(response.body_as_unicode())
        for label in jsdata['data']:
            for sd  in jsdata['data'][label]:
                cityid=sd['regionId']
                cityname=sd['regionName']
                urlbase="http://c.chedaoshanqian.com/brands/categories/top/firstLetter"
                metadata={'cityid':cityid,'cityname':cityname}
                yield scrapy.Request(urlbase, meta={'metadata': metadata}, callback=self.select2_parse, dont_filter=True)
    #agency
    def select2_parse(self,response):
        metadata=response.meta['metadata']
        if metadata:
            cityid=metadata['cityid']
        brdata = json.loads(response.body_as_unicode())
        for label in brdata['data']:
            for sd  in brdata['data'][label]:
                #rint sd
                brandid=sd['brandCategoryId']
                brandname=sd['brandCategoryName']
                #print cityid,brandid
                for pagenum in range(1,26):
                    metadata_brand = dict({'brandid': brandid,'brandname':brandname}, **metadata)
                    urlbase = "http://c.chedaoshanqian.com/items/searchItems?cityId="+str(cityid)+"&brandId="+str(brandid)+\
                              "&pageSize=200&pageNum="+str(pagenum)
                    #print urlbase
                    yield scrapy.Request(urlbase, meta={'metadata': metadata_brand}, callback=self.select3_parse)

    def select3_parse(self,response):
        metadata=response.meta['metadata']
        if  response.body.find('{')!=-1:
            ltdata = json.loads(response.body_as_unicode())
            if len(ltdata['data']['data']) !=0:
                for label in ltdata['data']['data']:
                    itemid=label['itemId']
                    metadata_list = dict({'itemid': itemid}, **metadata)
                    urlbase="http://c.chedaoshanqian.com/items/"+str(itemid)
            # print metadata
            # print urlbase
                    yield scrapy.Request(urlbase, meta={'metadata': metadata_list}, callback=self.select4_parse)


    def select4_parse(self,response):
        self.counts+=1
        print 'download:'+str(self.counts)
        item=ChedaoshanqianItem()
        metadata=response.meta['metadata']
        if metadata:
            item['cityid']=metadata['cityid']
            item['cityname'] = metadata['cityname']
            item['brandid'] = metadata['brandid']
            item['brandname']=metadata['brandname']
            item['itemid'] = metadata['itemid']
        item['grabtime'] = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        item['url'] = "http://c.chedaoshanqian.com/detail?id="+str(item['itemid'])
        item['status'] =response.url
        item['website'] = website
        frdata=json.loads(response.body_as_unicode())['data']
        item['agencyid']=frdata['agency']['agencyId']
        item['agencyname']=frdata['agency']['agencyName']
        item['province']=frdata['region1']['regionName']
        #other
        item['seriesid']=frdata['series']['brandCategoryId']
        item['seriesname'] = frdata['series']['brandCategoryName']
        item['makeyear'] = frdata['year']['brandCategoryName']
        item['registerdate'] = frdata['firstRegisterDate']
        item['mileage'] = frdata['currentMileage']
        item['price1']=frdata['price']
        item['guideprice']=frdata['priceInfo']['brandNewPrice']
        item['guidepricetax']=frdata['priceInfo']['purchaseTax']
        item['changetimes'] = frdata['ownerChangeTimes']
        item['yearchecktime'] = frdata['annualInspectionExpiredDate']
        item['Insurance1']=frdata['trafficInsuranceExpiredDate']
        item['Insurance2']=frdata['commercialInsuranceExpiredDate']
        item['img_url'] = frdata['pictureUrls'][0]
        item['agencycarnum']=frdata['branchInfoVO']['branchItemOnlineCnt']
        item['agencyrate']=frdata['branchInfoVO']['evaluation']
        item['agencyattionnum']=frdata['branchInfoVO']['attentionNum']
        item['agencycity']=frdata['branchInfoVO']['city']
        item['agencyphone'] = frdata['branchInfoVO']['phone']
        item['emission'] = frdata['emissionStandardName']
        item['carsource']=frdata['carSourceName']
        item['geartype'] = frdata['itemBaseInfoAll'][2]['value']
        item['output']=frdata['itemBaseInfoAll'][3]['value']
        item['color'] = frdata['itemBaseInfoAll'][7]['value']
        item['body'] = frdata['itemBaseInfoAll'][8]['value']
        item['shortdesc']=frdata['carName']
        item['dealtype']=u'\u5546\u5bb6'
        item['telphone']=frdata['consultPhone']
        item['desc']=frdata['description']
        yield item


class CarSpider_new(CarSpider):

    #basesetting
    name = spidername_new

    def __init__(self, **kwargs):
        # args
        super(CarSpider_new, self).__init__(**kwargs)
        #tag
        self.tag='new'
        # spider setting
        self.df =spider_new_Init(
                spidername=spidername_new,
                dbname=self.dbname,
                website=website,
                carnum=self.carnum)
        filename = 'blm/' + self.dbname + '/' + spidername_new + ".blm"
        self.fa = open(filename, "a")

#update
class CarSpider_update(CarSpider,update):

    #basesetting
    name = spidername_update

    def __init__(self, **kwargs):
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
        #do
        super(update, self).start_requests()





