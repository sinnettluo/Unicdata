# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
import logging
from pybloom import BloomFilter
from hashlib import md5
from scrapy.mail import MailSender
import os
import time

class che300Pipeline(object):
    def __init__(self):
        #mail
        self.mailer = MailSender.from_settings(settings)
        #mongo
        self.connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )

        #  修改mongodb的時候try 下  萬一之前的數據庫不存在   rename的時候才會報錯
        url_time = time.strftime("%Y%m%d", time.localtime())
        db = self.connection[settings['MONGODB_DB']]
        if settings["MONGODB_COLLECTION"] in["che300_app_modelinfo2_update","che300_price_color_update","che300_futureprice_update","che300_price_daily_update","che300_price_test_2019_update","che300_price_prov_daily_update_test"]:
            if settings["MONGODB_COLLECTION"] =="che300_price_test_2019_update":
                # 新數據庫的名字，也是久數據庫的名字
                self.MONGODB_COLLECTION = settings["MONGODB_COLLECTION"].split("_2019_")[0]
            else:
                self.MONGODB_COLLECTION = settings["MONGODB_COLLECTION"].split("_update")[0]
            colloection_old =db[self.MONGODB_COLLECTION]
            try:
                colloection_old.rename(self.MONGODB_COLLECTION+"_{}".format(url_time))
            except Exception as e:
            #      出錯的時候説明 以前的數據庫不存在
                logging.log(msg="mondodb is not exist %s" %e ,level=logging.INFO)
            else:
                pass
            self.collection = db[self.MONGODB_COLLECTION]
        else:
            self.MONGODB_COLLECTION =settings['MONGODB_COLLECTION']
            self.collection = db[settings['MONGODB_COLLECTION']]
        self.collectionurllog = db[settings['MONGODB_COLLECTION']+"_urllog_{}".format(url_time)]
        #bloom file
        filename = 'blm/' + settings['MONGODB_DB'] + '/' + settings['MONGODB_COLLECTION']+".blm"
        #pybloom
        num = (int(settings['CrawlCar_Num'])+self.collection.count())*1.1
        self.df = BloomFilter(capacity=num,error_rate=0.001)
        #read
        isexists = os.path.exists(filename)
        self.fa = open(filename, "a")
        if isexists:
            fr = open(filename, "r")
            lines = fr .readlines()
            for line in lines:
                line =line.strip('\n')
                self.df.add(line)
            fr.close()
        else:
            for i in self.collection.find():
                if "status" in i.keys():
                    item =i["status"]
                    item = md5(item).hexdigest()
                    self.df.add(item)
                    self.fa.writelines(item + '\n')
        #count
        self.downloadcounts=0
        self.counts=0


    def process_item(self, item, spider):
        logging.log(msg='**************************{}*****************************'.format(item),level=logging.INFO)
        valid = True
        i = md5(item['status']).hexdigest()

        returndf = self.df.add(i)
        if returndf:
            valid = False
        else:
            for data in item:
                if not data:
                    valid = False
                    raise DropItem("Missing {0}!".format(data))
        if valid:
            self.fa.writelines(i + '\n')
            self.collection.insert(dict(item))
            self.counts += 1
        else:
            logging.log(msg="Car duplicated!", level=logging.INFO)
        #log save
        urlog = {'url': item['url'], 'grabtime': item['grabtime']}
        self.collectionurllog.insert(urlog)
        return item

    def close_spider(self, spider):
        self.mysqlconnection = MySQLdb.connect("192.168.1.94", "root", "Datauser@2017", 'for_android', 3306)
        self.dbc = self.mysqlconnection.cursor()
        self.mysqlconnection.set_character_set('utf8')
        self.dbc.execute('SET NAMES utf8;')
        self.dbc.execute('SET CHARACTER SET utf8;')
        self.dbc.execute('SET character_set_connection=utf8;')
        self.connection.close()
        self.fa.close()
        if self.MONGODB_COLLECTION in ["che300_app_modelinfo2","che300_price_color","che300_futureprice_update_test","che300_price_daily_update_test","che300_price_test","che300_price_prov_daily","che300_modellist_daily"]:
            try:
                self.dbc.execute("update che300_detection set {} ={}+1 where row_names =1;".format(self.MONGODB_COLLECTION,self.MONGODB_COLLECTION))
            except  :
                logging.log(msg="fail！！！！！！！！！！！！！！！！！！ ",level=logging.INFO)
            else:
                logging.log(msg="success！！！！！！！！！！！！！！！！！1 ", level=logging.INFO)
            finally:
                self.mysqlconnection.commit()
                self.dbc.close()
                self.mysqlconnection.close()
        if self.MONGODB_COLLECTION  == "che300_modellist_"+settings["UPDATE_CODE"]:
            try:
                self.dbc.execute("update che300_detection set che300_app_modelinfo2=0,che300_price_color=0, che300_futureprice_update_test=0,che300_price_daily_update_test=0,che300_price_test=0,che300_price_prov_daily=0,che300_modellist_daily=0 where row_names =1;")
            except:
                logging.log(msg="fail!!!!!!!!!!!!!!!!!!!!!!", level=logging.INFO)
            else:
                logging.log(msg="success！！！！！！！！！！！！！！！！！1 ", level=logging.INFO)
            finally:
                self.mysqlconnection.commit()
                self.dbc.close()
                self.mysqlconnection.close()

        # self.mailer.send(to=["chzyy2017@163.com","hzhy_1@163.com"],
        #                  subject=settings['MONGODB_COLLECTION'], body="Scrapy Finished!")