#-*- coding: UTF-8 -*-
import scrapy
import requests
from ganji.items import GanjiItem
import time
import logging
from hashlib import md5
from SpiderInit import spider_original_Init
from SpiderInit import spider_new_Init
from SpiderInit import spider_update_Init
from SpiderInit import dfcheck
from SpiderInit import dffile
from Car_spider_update import update
import json
import re


website ='laipaiche_test1'

header = {
    'Connection': 'keep - alive',  # 保持链接状态
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

cookie={}

cookie['PHPSESSID']="k692fpcb6mcu75iivemt07u742"
cookie['uid']="Chn0nFmc88aeGGvvA3l/Ag=="
cookie['15308_7']='true'
cookie['lpaiche:cookie:user_info']="%7B%22uid%22%3A%22106635%22%2C%22user_name%22%3A%22clcw_mz0n_264%22%2C%22dealer_id%22%3A%2215308%22%2C%22mobile%22%3A%2213301679752%22%2C%22uniq_login_token%22%3A%22MDAwMDAwMDAwMK-eoqy0r5arhHZnra91p660fdHZgpvSYoXQa5uMZb2Vu4iyq7Owv6yDipCrrpzOnr-No5WOhbWdhbmDrYd6qd6wrrqsv2irrA%22%7D"


class CarSpider(scrapy.Spider):
    name=website

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        #setting-
        self.tag='original'
        self.counts=0
        self.carnum=1500000
        self.dbname = 'usedcar'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df='none'
        self.fa='none'

    def start_requests(self):
        print "start"
        brandid=["15","60","88","121","139","144","221","223","8","25","30","45","56","68","77","82","104","110","151","154","168","177","210","218","219","227","229","230","231","12","13","21","81","86","103","108","212","213","9","24","26","35","42","43","48","61","75","96","98","123","130","167","170","207","209","224",
                 "33", "41", "50", "53", "76", "85", "109", "122", "145", "169", "175", "196", "216", "225", "236", "7",
                 "58", "92", "105", "126","127","18","40","44","59","70","90","107","113","118","124","128","166","178","184","191","192","204","205","233","19","63","79","87","91","115","116","138","162","173","179","197","198","199","201","202",
                 "228","3","22","23","28","29","52","89","94","129","185","14","16","20","74","93","135","137","140","141","142","146","150","153","156","160","200","217","39","57","114","143","148","155","157","181","215","10",
                 "84","1","69","132","152","31","49","55","131","17","83","95","193","194","208","97","158","206","2","5","32","67","71","78","102","120","125","133","134","147","163","186","211","222","232","235","38","51","65",
                 "80", "100", "117", "180", "182", "234", "54", "72", "99", "106", "112", "188", "190", "214", "66",
                 "149", "165", "171", "174", "187", "220", "226", "6", "34", "46", "47", "62", "64", "101", "111",
                 "119", "136", "161", "183", "189", "195", "4", "11","27","36","37","73","159","164","172","176","203",]
        for temp in brandid:
            url1 = "http://www.lpaiche.com/HisPrice/index/ajax/1/brand_id/"+temp+"?p=1"
            metadata={"brandid":temp,"current_page":1}
            yield scrapy.Request(url=url1,meta={'metadata':metadata}, headers=header, cookies=cookie,dont_filter=True)


    def parse(self,response):
        print "do parse"+"     --    "+response.url
        metadata = response.meta['metadata']
        temp=response.xpath('//p/text()').extract_first()
        str1=re.findall('(?<=\"car_no\":\").*?\",\"reg_city',temp)
        for temp1 in str1:
            urlbase=re.findall('(.*)","reg_city',temp1)[0]
            url="http://www.lpaiche.com/Car/report/car_no/"+urlbase
            print "parse"+"    "+url
            yield scrapy.Request(url,meta={'metadata':metadata},callback=self.parse_car,dont_filter=True)
        if len(str1)==10:
            metadata['current_page']+=1
            next_page="http://www.lpaiche.com/HisPrice/index/ajax/1/brand_id/"+metadata['brandid']+"?p="+str(metadata['current_page'])
            yield scrapy.Request(next_page,meta={'metadata':metadata},callback=self.parse,dont_filter=True)

    def parse_car(self,response):
        print "do parse car"
        item = GanjiItem()
        print response.body
        item['url'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
        item['website'] = website
        item['status'] = response.url
        item['pagetime'] = 'zero'
        html=requests.get('http://www.lpaiche.com/Car/report/car_no/JC01201702218A1B', cookies=cookie)
        item['datasave'] =html.text
        yield item
