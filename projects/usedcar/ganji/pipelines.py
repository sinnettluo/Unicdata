# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
import logging
from pybloom_live import BloomFilter
from pybloom_live import ScalableBloomFilter
from hashlib import md5
from scrapy.mail import MailSender
import os
import sys
import pandas
import MySQLdb
import car_parse
import scrapy
import time
from sqlalchemy import create_engine


#sys.path.append('parse')
#tmp="car_parse_"+settings['MONGODB_COLLECTION']
#if settings['MONGODB_COLLECTION'] in ["youxin","youche","ygche","xcar","taboche","souhu","souche","iautos","haoche51","ganji","cn2che","che273"]:
   # module1=__import__(tmp)


class GanjiPipeline(object):
    def __init__(self):
        # mail
        self.mailer = MailSender.from_settings(settings)
        # mongo
        self.connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = self.connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        self.collectionurllog = db[settings['MONGODB_COLLECTION']+"_urllog"]
        self.collectionwrong = db[settings['MONGODB_COLLECTION']+"_wrongurllog"]
        #bloom file
        # filename= settings['BLM_PATH'] + settings['MONGODB_DB']+'/'+settings['MONGODB_COLLECTION']+'.blm'
        filename = 'blm/' + settings['MONGODB_DB'] + '/' + settings['MONGODB_COLLECTION'] + '.blm'
        #pybloom
        num = (int(settings['CrawlCar_Num'])+self.collection.count())*1.1
        self.df = ScalableBloomFilter(initial_capacity=num, error_rate=0.01)
        #read
        isexists = os.path.exists(filename)
        self.fa = open(filename, "a")
        if isexists:
            fr = open(filename, "r")
            lines = fr .readlines()
            for line in lines:
                line = line.strip('\r\n')
                self.df.add(line)
            fr.close()
        else:
            for i in self.collection.find():
                if "status" in i.keys():
                    item = i["status"]
                    item = md5(item).hexdigest()
                    self.df.add(item)
                    self.fa.writelines(item + '\r\n')
        #count
        self.mongocounts=0
        self.sqlcounts=0
        #mysql
        self.mysqlconnection =MySQLdb.connect(settings['MYSQLDB_SERVER'],
                                         settings['MYSQLDB_USER'],
                                         settings['MYSQLDB_PASS'],
                                         settings['MYSQLDB_DB'],
                                         port=settings['MYSQLDB_PORT']
                                         )
        self.dbc = self.mysqlconnection.cursor()
        self.mysqlconnection.set_character_set('utf8')
        self.dbc.execute('SET NAMES utf8;')
        self.dbc.execute('SET CHARACTER SET utf8;')
        self.dbc.execute('SET character_set_connection=utf8;')
        # self.table = settings['MONGODB_COLLECTION']+ '_' +time.strftime("%Y%W")
        self.table = settings['MONGODB_COLLECTION']+ '_online'
        self.items=[]
        self.caritemlist =car_parse.Parse_conf(settings['MONGODB_COLLECTION'])
        # print self.caritemlist

    def process_item(self, item, spider):
        # print(item)
        valid = True
        i = md5(item['status']).hexdigest()
        print(i)
        returndf = self.df.add(i)
        print(returndf)
        if item['url'].find('error') == -1:
            iserror =False
        else:
            iserror=True
        print(iserror)
        if returndf or iserror:
            valid = False
        else:
            for data in item:
                if not data:
                    valid = False
                    raise DropItem("Missing {0}!".format(data))

        print(valid)
        print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        if valid:
            self.fa.writelines(i + '\r\n')
            self.collection.insert(dict(item))
            #logging.log(msg="Car added to MongoDB database!", level=logging.INFO)
            self.mongocounts += 1
            #logging.log(msg="scrapy                    " + str(self.counts) + "                  items", level=logging.INFO)
            #mysql save
            if settings['MONGODB_COLLECTION'] in ["taoche", "youxin","ttpai","che168","youxinpai","guazi","renrenche","kaixin","haoche51","souche","hx2car","che168","renrenche","iautos","souhu","haoche99","che273","che101","chewang","xcar","ganji","zg2sc","ygche","che58","youche","cn2che","baixing", "che273_test"]:
                domtext = scrapy.selector.Selector(text=item["datasave"][1])
                parsed_item = car_parse.ILikeParse(self.caritemlist, item, domtext)
                self.items.append(parsed_item)
                # logging.log(msg=item["datasave"][0],level=logging.INFO)
                # logging.log(msg=item["datasave"][1],level=logging.INFO)
                # logging.log(msg=parsed_item,level=logging.INFO)
                # logging.log(msg=item['url'],level=logging.INFO)
                # logging.log(msg="add to SQL",level=logging.INFO)
                self.items = self.savedata(self.items, self.table, self.mysqlconnection, 1)
            elif settings['MONGODB_COLLECTION'] in ["chemao", "aokangda", "auto51", 'aokangda_test', 'chezhibao']:
                domtext=scrapy.selector.Selector(text=item["datasave"][0])
                parsed_item = car_parse.ILikeParse(self.caritemlist, item, domtext)
                self.items.append(parsed_item)
                # logging.log(msg=item["datasave"][0],level=logging.INFO)
                #logging.log(msg=item["datasave"][1],level=logging.INFO)
                # logging.log(msg=parsed_item,level=logging.INFO)
                # logging.log(msg=item['url'],level=logging.INFO)
                # logging.log(msg="add to SQL",level=logging.INFO)
                self.items = self.savedata(self.items,self.table,self.mysqlconnection,1)


                # logging.log(msg="add sql                   " + str(self.counts) + "                  items",  level=logging.INFO)
        elif iserror:
            logging.log(msg="Car Error!", level=logging.INFO)
            # log save
            urlog = {'url': item['url'], 'grabtime': item['grabtime']}
            self.collectionwrong.insert(urlog)
        else:
            pass
            #logging.log(msg="Car duplicated!", level=logging.INFO)
        #log save
        urlog = {'url': item['url'], 'grabtime': item['grabtime']}
        self.collectionurllog.insert(urlog)
        return item

    def close_spider(self, spider):
        self.connection.close()
        self.fa.close()
        self.savefinal(self.items,self.table,self.mysqlconnection)
        countitems=[]
        countitem=dict()
        countitem['website']=settings['MONGODB_COLLECTION']
        countitem['date']=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        countitem['mongocount']=self.mongocounts
        countitem['sqlcounts']=self.sqlcounts
        if(self.mongocounts!=0 and self.sqlcounts!=0):
            if(self.sqlcounts/self.mongocounts<0.5):
                self.mailer.send(to=["huzhangyong@haistand.com.cn"], subject=settings['MONGODB_COLLECTION'],body="Website update!"+settings['MONGODB_COLLECTION'],
                                 cc=["zhanglinmeng@haistand.com.cn"])
        countitems.append(countitem)
        df = pandas.DataFrame(countitems)
        # df.to_sql(name=tablename, con=mysqldb, flavor='mysql', if_exists='append', index=False)
        # df.to_sql(name="statistic", con=self.mysqlconnection, flavor='mysql', if_exists='append', index=False)
        self.mysqlconnection.close()
        self.dbc.close()
        self.mailer.send(to=["huzhangyong@haistand.com.cn"], subject=settings['MONGODB_COLLECTION'], body="Scrapy Finished!",
                         cc=["hzhy_1@163.com"])
        if not(spider.name.find('_new')==-1):
                nextspider = spider.name
                nextspider =nextspider.replace('_new','_update')
                orderstring = 'curl http://localhost:6800/schedule.json -d project='+settings['MONGODB_DB']+' -d spider='+nextspider
                os.system(orderstring)
        # else:
        #     website=settings['MONGODB_COLLECTION']
        #     parse_string ='python '+n+'.py'
        #     os.system(parse_string)

    def savedata(self,items,tablename,mysqldb,savesize=1):
        error = True
        count = 0
        # print(items)
        print(len(items))
        if len(items)==savesize:
            while error and count == 0:
                print("XXXX")
                try:
                    df = pandas.DataFrame(items)
                    df.to_sql(name=tablename, con=mysqldb, flavor='mysql', if_exists='append', index=False)
                    self.sqlcounts+=1
                    logging.log(msg="add to SQL",level=logging.INFO)
                    error = False
                except Exception as e:
                    print(e)
                    print("MARK")
                    if str(e).find("MySQL server has gone away") >= 0:
                        try:
                            mysqldb = MySQLdb.connect(settings['MYSQLDB_SERVER'],
                                             settings['MYSQLDB_USER'],
                                             settings['MYSQLDB_PASS'],
                                             settings['MYSQLDB_DB'],
                                             port=settings['MYSQLDB_PORT']
                                             )
                            dbc = mysqldb.cursor()
                            mysqldb.set_character_set('utf8')
                            dbc.execute('SET NAMES utf8;')
                            dbc.execute('SET CHARACTER SET utf8;')
                            dbc.execute('SET character_set_connection=utf8;')
                            self.mysqlconnection = mysqldb
                        except Exception as e:
                            print(e)
                            items = []

                    error = True
                    count = 1
            items=[]
        return items

    def savefinal(self,items,tablename,mysqldb):
        if len(items)!=0:
            df = pandas.DataFrame(items)
            self.sqlcounts+=len(items)
            df.to_sql(name=tablename, con=mysqldb, flavor='mysql', if_exists='append', index=False)
