#-*- coding: UTF-8 -*-
import scrapy
from ganji.items import GanjiItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import MySQLdb
import pybloom
import hashlib
import re



carnum = 1000000
website ='che58_config'
Reported =False
#main
class CarSpider(scrapy.Spider):

    #basesetting
    name = website
    allowed_domains = ["58.com"]
    # setting Reload
    # log
    #settings.set('LOG_FILE', website + ".scrapy.log", priority='cmdline')
    # Delay
    #settings.set('DOWNLOAD_DELAY', 0, priority='cmdline')

    def __init__(self, **kwargs):
        # args
        super(CarSpider, self).__init__(**kwargs)
        #problem report
        self.mailer = MailSender.from_settings(settings)
        self.counts=0
        # Mongo
        settings.set('CrawlCar_Num', carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'usedcar', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')
        #mysql
        # mysql
        mysqldb = MySQLdb.connect("192.168.1.94", "root", "Datauser@2017", "usedcar", port=3306)
        mysqldbc = mysqldb.cursor()
        # read
        mysqldbc.execute("select newcarurl from che58")
        items = mysqldbc.fetchall()
        self.urllist=[]
        df =pybloom.BloomFilter(carnum,0.01)
        for i in items:
            j=i[0]
            md5i= hashlib.md5(j)
            rf = df.add(md5i)
            if not rf:
                self.urllist.append(j)

    # get car list
    def start_requests(self):
        self.totalsize = len(self.urllist)
        print self.totalsize
        if self.totalsize==0:
            self.totalsize=100
        size = 100
        stepsize = int(self.totalsize / size)
        lists = []
        self.idlist = []
        for id in range(0, self.totalsize, stepsize):
            url = self.urllist[id]
            list = scrapy.Request(url, meta={"id": id})
            lists.append(list)
            self.idlist.append(id)
        return lists

    # get car infor
    def parse(self, response):
        #error report status
        global Reported
        #count
        self.counts +=1
        logging.log(msg="download              " + str(self.counts) + "                  items", level=logging.INFO)
        if not("callback.58.com" in response.url):
            #reported check
            Reported = False
            #base infor
            datetime =''
            #item loader
            item = GanjiItem()
            item['url'] = response.url
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['website'] = website
            item['status'] = response.url
            item['pagetime'] = datetime
            item['datasave'] = re.sub(r'\s+', ' ', response.xpath('//html').extract_first())
            yield item
        elif not(Reported):
            logging.log(msg="Response.url:" + response.url +"-"+str(Reported) , level=logging.INFO)
            self.mailer.send(to=["huzhangyong@haistand.com.cn"], subject=website, body="Scrapy Error, please check"+response.url ,
                        cc=["zhaolili@haistand.com.cn"])
            Reported=True
        # next request
        idnext = int(response.meta['id']) + 1
        if idnext not in self.idlist:
            self.idlist.append(idnext)
            url = self.urllist[idnext]
            yield scrapy.Request(url, meta={"id": idnext}, callback=self.parse)


