# -*- coding: utf-8 -*-
import scrapy
from ..items import che300_historyprice
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
from hashlib import md5
import re
import json
import datetime

website = 'che300_historyprice'
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
                       "16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","35","38","39","41",
                       "42","44","46","50","70","125","147","153","162","185","317"]
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
            usedyearlist=[]
            yearlist=[]
            monlist=[]
            if max_reg_year==2017:
                usedyear_min=0
                max_month = datetime.datetime.now().month
            else:
                usedyear_min = float((datetime.datetime.now() - datetime.datetime(max_reg_year, 12, 1)).days)/ 365
                max_month=12
            usedyear_max= float((datetime.datetime.now() - datetime.datetime(min_reg_year, 1, 1)).days)/365
            usedyearlist =[usedyear_max,usedyear_min]
            yearlist = [min_reg_year,max_reg_year]
            monlist = [1,max_month]
            for i in [0,1]:
                usedyear=usedyearlist[i]
                if usedyear!=0:
                    milage = round(usedyear*1.25,2)
                else:
                    milage=0.1
                # print milage
                reyear=yearlist[i]
                mon=monlist[i]
                date = str(reyear) + "-" + str(mon)
                # print date
                if i==0:
                    mile=30
                    # print mile
                    urlinfo = {"emission": emission, "geartype": geartype, "liter_type": liter_type,
                               "liter": liter, "max_reg_year": max_reg_year, "min_reg_year": min_reg_year,
                               "salesdescid": salesdescid, "salesdesc": salesdesc, "price": price,
                               "makeyear": makeyear, "date":date, "milage":mile,"reyear":reyear}
                    urlinfo = dict(urlinfo, **meta)
                    #print urlinfo
                    url = "https://dingjia.che300.com/api/lib/util/city/prov_with_city"
                    yield scrapy.Request(url, meta={"urlinfo": urlinfo}, callback=self.parse_url,
                                         dont_filter=True)
                else:
                    for mile in [milage,round(usedyear*2,2)]:
                        # print mile
                        urlinfo = {"emission": emission, "geartype": geartype, "liter_type": liter_type,
                                   "liter": liter, "max_reg_year": max_reg_year, "min_reg_year": min_reg_year,
                                   "salesdescid": salesdescid, "salesdesc": salesdesc, "price": price,
                                   "makeyear": makeyear, "date":date, "milage":mile,"reyear":reyear}
                        urlinfo = dict(urlinfo, **meta)
                        url = "https://dingjia.che300.com/api/lib/util/city/prov_with_city"
                        yield scrapy.Request(url, meta={"urlinfo": urlinfo}, callback=self.parse_url,
                                             dont_filter=True)

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
                    url = "https://dingjia.che300.com/app/EvalResult/getPreSaleRate?callback=jQuery&prov=" + provid + \
                          "&city=" + cityid + "&brand=" + brandid + "&series=" + familyid + "&model=" + salesdescid + "&regDate=" + date + "&mile=" + str(milage)
                    # print url
                    yield scrapy.Request(url, meta={"datainfo": datainfo}, callback=self.parse_price,
                                         dont_filter=True)

    def parse_price(self, response):
        # print response.url
        meta = response.meta['datainfo']
        provid = meta['provid']
        cityid = meta['cityid']
        reyear = meta['reyear']
        brandid = meta['brandid']
        familyid = meta['familyid']
        date = meta['date']
        salesdescid = meta['salesdescid']
        milage = meta['milage']

        if response.xpath('//p/text()').re('\{\"success.*\}\]\}'):
            data = json.loads(response.xpath('//p/text()').re('\{\"success.*\}\]\}')[0])['success']
            price4 = data[3]['price']
            priceinfo = {'price4':price4}
            datainfo = dict(priceinfo, **meta)
            url = 'https://dingjia.che300.com/app/EvalResult/getPriceHistory?&provId='\
                + provid +'&cityId='+ cityid +'&modelId='+ familyid +'&regYear='+ str(reyear )+'&regMonth='+ str(re.findall(r'\d+',date)[1]) +\
                  '&mileAge='+ str(milage) +'&price='+str(price4)
            yield scrapy.Request(url, meta={"datainfo": datainfo}, callback=self.parsehistoryprice,dont_filter=True)

    def parsehistoryprice(self,response):
        # print response.url
        item = che300_historyprice()
        meta = response.meta['datainfo']
        # print meta
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
        item['price4'] = meta['price4']
        #
        # #
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        if json.loads(response.xpath('//p/text()').extract_first())['status']==1:
            data = json.loads(response.xpath('//p/text()').re('\[.*\]')[0])
            try:
                item['price_h6'] = str(data[0]['eval_price'])
                item['price_h5'] = str(data[1]['eval_price'])
                item['price_h4'] = str(data[2]['eval_price'])
                item['price_h3'] = str(data[3]['eval_price'])
                item['price_h2'] = str(data[4]['eval_price'])
                item['price_h1'] = str(data[5]['eval_price'])
            except Exception,e:
                pass

        item['status'] = md5(response.url).hexdigest()
        yield item