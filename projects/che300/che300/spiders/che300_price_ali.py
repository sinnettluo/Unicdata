# -*- coding: utf-8 -*-
import scrapy
from ..items import che300_price
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
from hashlib import md5
import re
import json
import datetime
import random

website = 'che300_dingjia_ali_t'
class CarSpider(scrapy.Spider):
    name = website
    allowed_domains = ["che300.com"]

    start_urls=[
        'https://m.che300.com/pinggu'
    ]

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # problem report
        self.mailer = MailSender.from_settings(settings)
        self.carnum = 2000000000
        self.counts = 0
        # Mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'usedcar_evaluation', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')
        self.citylist=["1","2","3","4","5","6","8","9","10","11","12","13","14","15",
                       "16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32"]
    #pro_city select
    #brandselect
    def parse(self,response):
        for br in response.xpath('//dl[@class="list brand-list"]'):
            for id in br.xpath('dd'):
                brandid = id.xpath('@data-brandid').extract_first()
                brandname = id.xpath('text()').extract_first()
                metadata = {"brandid": brandid, "brandname": brandname}
                url = "https://ssl-meta.che300.com/meta/series/series_brand"+ brandid +".json"
                # print url
                yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_family, dont_filter=True)

    def parse_family(self,response):
        meta = response.meta['metadata']
        # print meta
        data = json.loads(response.xpath('//p/text()').extract_first())
        for info in data:
            factoryname = info['series_group_name']
            familyid = info['series_id']
            familyname = info['series_name']
            familyinfo = {"factoryname": factoryname, "familyid": familyid, "familyname": familyname}
            familydata = dict(familyinfo, **meta)
            # print familydata
            # print familyname
            url = "https://ssl-meta.che300.com/meta/model/model_series"+ familyid +".json?"
            yield scrapy.Request(url, meta={"familydata": familydata}, callback=self.parse_vehileinfo, dont_filter=True)

    def parse_vehileinfo(self, response):
        meta = response.meta['familydata']
        # print meta
        # procity = json.loads()
        data = json.loads(response.xpath('//p/text()').extract_first())
        for info in data:
            emission = info['discharge_standard']
            geartype = info['gear_type']
            liter_type = info['liter_type']
            liter = info['liter']
            max_reg_year = int(info['max_reg_year'])
            min_reg_year = int(info['min_reg_year'])
            salesdescid = info['model_id']
            salesdesc = info['model_name']
            price = info['model_price']
            makeyear = info['model_year']
            # print type(min_reg_year)

            for  ry in xrange(min_reg_year,max_reg_year+1):
                if ry == 2017:
                    max_month=datetime.datetime.now().month
                else:
                    max_month = 12
                monlist = range(1,max_month+1)
                if len(monlist) <= 3:
                    monlist1 = monlist
                else:
                    monlist1 = random.sample(monlist, 2)
                for rm in monlist1:
                    usedyear = float((datetime.datetime.now() - datetime.datetime(ry, rm, 1)).days)/365
                    mile = round( usedyear*1.25, 2)
                    if mile >= 30:
                        milage = [1,30]
                    elif mile >1 and mile <30:
                        milage = [1,mile,30]
                    elif mile==1:
                        milage = 1
                    else :
                        milage = [mile,1]
                    for m in milage:
                        date = str(ry) + "-" + str(rm)
                        urlinfo = {"emission": emission, "geartype": geartype, "liter_type": liter_type,
                                   "liter": liter, "max_reg_year": max_reg_year, "min_reg_year": min_reg_year,
                                   "salesdescid": salesdescid, "salesdesc": salesdesc, "price": price,
                                   "makeyear": makeyear, "date": date, "milage": m, "reyear": ry}

                        urlinfo = dict(urlinfo, **meta)
                        url = "https://dingjia.che300.com/api/lib/util/city/prov_with_city"
                        yield scrapy.Request(url, meta={"urlinfo": urlinfo}, callback=self.parse_url,dont_filter=True)

    def parse_url(self, response):
        meta = response.meta['urlinfo']
        brandid = meta['brandid']
        familyid = meta['familyid']
        salesdescid = meta['salesdescid']
        milage = meta['milage']
        date = meta['date']

        data = response.xpath('//p/text()').extract_first()
        t = re.findall(r'\{\"prov_name.*?\}\]\}',data)
        for i in range(len(t)):
            p = json.loads(t[i])
            provid = p['prov_id']
            provname = p['prov_name']
            da = p['data']
            # print da
            for j in da:
                cityname = j['city_name']
                cityid = j['city_id']
                if cityid in self.citylist:
                    procity = {'provid':provid, 'provname':provname ,'cityid':cityid, 'cityname':cityname}
                    datainfo = dict(procity, **meta)
                    # print cityname
                    url = "https://www.che300.com/pinggu/v"+ provid +"c"+ cityid +"m"+ salesdescid +"r"+ str(date) +"g"+str(milage)
                    yield scrapy.Request(url, meta={"datainfo": datainfo}, callback=self.parse_status,dont_filter=True)

    def parse_status(self,response):
        meta = response.meta['datainfo']
        brandid = meta['brandid']
        familyid = meta['familyid']
        salesdescid = meta['salesdescid']
        milage = meta['milage']
        date = meta['date']
        provid = meta['provid']
        cityid = meta['cityid']
        situation = response.xpath('//ul[@class="sp-bar clearfix"]/li[contains(@class,"on")]/text()').extract_first()
        sitinfo = {'situation':situation}
        datainfo = dict(sitinfo, **meta)
        url = "https://dingjia.che300.com/app/EvalResult/getPreSaleRate?" \
              "callback=jQuery18303745581165454668_1491989508797&prov=" + provid + \
              "&city=" + cityid + "&brand=" + brandid + "&series=" + familyid + \
              "&model=" + salesdescid + "&regDate=" + date + "&mile=" + str(milage)
        #print url
        yield scrapy.Request(url, meta={"datainfo": datainfo}, callback=self.parse_price,dont_filter=True)

    def parse_price(self, response):
        #print response.url
        item = che300_price()
        meta = response.meta['datainfo']
        item['geartype'] = meta['geartype']
        item['provname'] = meta['provname']
        item['provid'] = meta['provid']
        item['makeyear'] = meta['makeyear']
        item['price'] = meta['price']
        item['cityname'] = meta['cityname']
        item['emission'] = meta['emission']
        item['reyear'] = meta['reyear']
        item['factoryname'] = meta['factoryname']
        item['brandname'] = meta['brandname']
        item['brandid'] = meta['brandid']
        item['familyname'] = meta['familyname']
        item['familyid'] = meta['familyid']
        item['date'] = meta['date']
        item['salesdesc'] = meta['salesdesc']
        item['salesdescid'] = meta['salesdescid']
        item['milage'] = meta['milage']
        item['liter_type'] = meta['liter_type']
        item['situation'] = meta['situation']
        #
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        if response.xpath('//p/text()').re('\{\"success.*\}\]\}'):
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
            item['status'] = md5(response.url).hexdigest()
            yield item