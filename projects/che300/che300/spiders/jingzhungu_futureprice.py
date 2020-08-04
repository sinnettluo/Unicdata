# -*- coding: utf-8 -*-
import scrapy
from ..items import jingzhungu_futureprice
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
from hashlib import md5
import re
import json
import datetime
from datetime import date

website = 'jingzhungu_futureprice'
class CarSpider(scrapy.Spider):
    name = website
    allowed_domains = ["jingzhengu.com"]

    start_urls=[
        'http://m.jingzhengu.com/getMakeModelStyleAll/getMakeList?isEst=1&produceStatus=0'
    ]

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)

        # problem report
        self.mailer = MailSender.from_settings(settings)
        self.carnum = 2000000000
        self.counts = 0
        self.today = date.today()
        # Mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'usedcar_evaluation', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    #pro_city select
    #brandselect
    def parse(self,response):
        data = json.loads(response.xpath('//p/text()').extract_first())
        if data['status']==200:
            temp=data['list']
            for da in temp:
                brandname = da['makeName']
                brandid = da['makeId']
                metadata = {"brandid": brandid, "brandname": brandname}
                # print brandname, brandid
                url = "http://m.jingzhengu.com/areacity/citylist"
                yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_proinfo, dont_filter=True)
    #procity parse
    def parse_proinfo(self,response):
        meta = response.meta['metadata']
        brandid = meta['brandid']
        # print meta
        data = json.loads(re.findall('\\[.*?\\]',response.xpath('//body/text()').extract()[5])[0])
        for info in data:
            cityID = info['cityID']
            cityName = info['cityName']
            provID = info['provID']
            provName = info['provName']
            proinfo = {"cityID": cityID, "cityName": cityName, "provID": provID, "provName": provName}
            metadata = dict(proinfo, **meta)
            #print metadata
            url = "http://www.jingzhengu.com/Resources/ajax/PingGuHandlerV5.ashx?op=" \
                  "getAppointYearBeforeModel&makeid="+ str(brandid) +"&year=2017"
            yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_familyinfo, dont_filter=True)

    def parse_familyinfo(self,response):
        meta = response.meta['metadata']
        data = json.loads(response.xpath('//p/text()').extract_first().replace('var ptv_carserial=',''))
        for info in data:
            factoryname = info['GroupName']
            familyname = info['Text']
            familyid = info['Value']
            familyinfo = {"factoryname": factoryname, "familyname": familyname, "familyid": familyid}
            url = 'http://www.jingzhengu.com/Resources/Ajax/PingGuHandlerV5.ashx?' \
                  'op=getAppointYearBeforeStyle&modelid='+ str(familyid) +'&year=2017'
            metadata=dict(familyinfo,**meta)
            yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_vehileinfo, dont_filter=True)

    def parse_vehileinfo(self,response):
        meta = response.meta['metadata']
        cityID = meta['cityID']
        provID = meta['provID']

        data = json.loads(response.xpath('//p/text()').extract_first().replace('var ptv_carbasicinfo=', ''))
        for info in data:
            makeyear = info['GroupName'].replace(u' \u6b3e','')
            guideprice = info['NowMsrp']
            salesdesc = info['Text']
            salesdescid = info['Value']
            # print makeyear

            minyear = int(makeyear) - 1
            if makeyear <= 2015:
                maxyear = makeyear+2
            else:
                maxyear  = 2017
            for y in xrange(minyear,maxyear+1):
                if y == 2017:
                    maxmon = self.today.month
                    mon = xrange(1, maxmon + 1)
                elif y==minyear:
                    mon=xrange(6,13)
                else:
                    mon=xrange(1,13)
                for m in mon:
                    usedmile = int(((self.today-datetime.date(y, m, 1)).days/365.0)*2)
                    xmile = int((self.today-datetime.date(y, m, 1)).days/30.0)
                    if xmile <= 30:
                        maxmile = xmile
                    else:
                        maxmile = 30
                    if usedmile < 1 & maxmile > 1:
                        milage = [usedmile,1,maxmile]
                    elif usedmile >1:
                        milage = [1,usedmile, maxmile]
                    else:
                        milage = [usedmile, maxmile]

                    for mile in milage:
                        if mile==0:
                            mile=0.1
                        date = str(y)+"-"+str(m)+"-"+"1"

                        url = "http://www.jingzhengu.com/Resources/Ajax/MaintainValueV5.ashx?op=getCarScrapValue&" \
                              "sid="+ salesdescid +"&regdate="+ date +"&milage="+ str(mile) +"&provid="+ str(provID) +"&cityid="+str(cityID)
                        # print y,m,mile
                        vehileinfo = {"makeyear": makeyear, "guideprice": guideprice, "salesdesc": salesdesc,
                                      "salesdescid": salesdescid, "reyear": y, "remonth": m,"mileage": mile,}
                        metadata = dict(vehileinfo, **meta)
                        yield scrapy.Request(url, meta={"metadata": metadata}, callback=self.parse_priceinfo,dont_filter=True)
    def parse_priceinfo(self,response):
        # count
        print "response.url", response.url
        self.counts += 1
        print "download              " + str(self.counts) + "                  items"
        # item loader
        item = jingzhungu_futureprice()
        meta = response.meta['metadata']
        item['mileage'] = meta['mileage']
        item['makeyear'] = meta['makeyear']
        item['guideprice'] = meta['guideprice']
        item['brandname'] = meta['brandname']
        item['familyid'] = meta['familyid']
        item['brandid'] = meta['brandid']
        item['remonth'] = meta['remonth']
        item['provName'] = meta['provName']
        item['provID'] = meta['provID']
        item['salesdesc'] = meta['salesdesc']
        item['familyname'] = meta['familyname']
        item['cityName'] = meta['cityName']
        item['salesdescid'] = meta['salesdescid']
        item['cityID'] = meta['cityID']
        item['factoryname'] = meta['factoryname']
        item['reyear'] = meta['reyear']
        #
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        #
        data = json.loads(response.xpath('//p/text()').extract_first())
        months = []
        years = []
        for i in data['Months']:
            months.append(data['Months'][i])
        for j in data['Year']:
            years.append(data['Year'][j])
        item['month1'] = months[0]
        item['month2'] = months[1]
        item['month3'] = months[2]
        item['month4'] = months[3]
        item['month5'] = months[4]
        item['year1'] = years[0]
        item['year2'] = years[1]
        item['year3'] = years[2]
        item['year4'] = years[3]
        item['year5'] = years[4]

        item['status'] = md5(response.url).hexdigest()
        yield item
