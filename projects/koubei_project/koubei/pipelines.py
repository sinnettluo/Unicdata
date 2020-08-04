# -*- coding: utf-8 -*-


import pandas as pd
from sqlalchemy import create_engine
import os
from pybloom_live import ScalableBloomFilter
# from scrapy.conf import settings
from hashlib import md5
import pymongo
from scrapy.exceptions import DropItem
import logging
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.utils.project import get_project_settings

settings = get_project_settings()


class KoubeiPipeline(object):
    def __init__(self):

        self.conn = create_engine('mysql+pymysql://root:Datauser@2017@192.168.1.94:3306/koubei?charset=utf8')
        self.counts = 0
        self.connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = self.connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        self.collectionurllog = db[settings['MONGODB_COLLECTION'] + "_urllog"]

        filename = '/root/blm/' + settings['MONGODB_DB'] + '/' + settings['MONGODB_COLLECTION'] + '.blm'
        #  跑kbb 的時候重新注意下
        # filename="kbb.blm"
        # filename = 'blm/' + settings['MONGODB_DB'] + '/' + settings['MONGODB_COLLECTION'] + '.blm'
        # pybloom
        num = (int(settings['CrawlCar_Num']) + self.collection.count()) * 1.1
        self.df = ScalableBloomFilter(initial_capacity=num, error_rate=0.001)
        # read
        isexists = os.path.exists(filename)
        self.fa = open(filename, "a")
        if isexists:
            fr = open(filename, "r")
            lines = fr.readlines()
            for line in lines:
                line = line.strip('\n')
                self.df.add(line)
            fr.close()
        else:
            for i in self.collection.find():
                if "status" in i.keys():
                    item = i["status"]
                    item = md5(item).hexdigest()
                    self.df.add(item)
                    self.fa.writelines(item + '\n')

    def process_item(self, item, spider):

        if spider.name.find("weixin") >= 0 or spider.name in ['echongwang', 'tuhu_baoyang_dianping3']:
            if spider.name == "":
                self.collection.insert(dict(item))
                urlog = {'url': item['url'], 'grabtime': item['grabtime']}
                self.collectionurllog.insert(urlog)
                pass
            else:
                valid = True
                i = md5(item['status'].encode("utf-8")).hexdigest()
                returndf = self.df.add(i)
                # print(returndf)
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
                    logging.log(msg="Car added to MongoDB database!", level=logging.INFO)
                    self.counts += 1
                    logging.log(msg="scrapy                    " + str(self.counts) + "                  items",
                                level=logging.INFO)
                else:
                    logging.log(msg="Car duplicated!", level=logging.INFO)
                # log save
                urlog = {'url': item['url'], 'grabtime': item['grabtime']}
                self.collectionurllog.insert(urlog)
                return item

        i = md5(item['status'].encode("utf-8")).hexdigest()
        returndf = self.df.add(i)
        # if True:
        # logging.log(msg="pass", level=logging.INFO)
        if not returndf:
            logging.log(msg="yes", level=logging.INFO)
            # 刷新缓存区
            self.fa.flush()
            self.fa.writelines(i + '\n')

            items = []
            items.append(item)
            df = pd.DataFrame(items)
            if spider.name == "evp_fix2":
                conn = create_engine('mysql+pymysql://root:Datauser@2017@192.168.1.94:3306/koubei2?charset=utf8mb4')
                pd.io.sql.to_sql(df, name=settings['MONGODB_COLLECTION'], con=conn, if_exists="append")
            else:
                pd.io.sql.to_sql(df, name=settings['MONGODB_COLLECTION'], con=self.conn, if_exists="append")

            urlog = {'url': item['url'], 'grabtime': item['grabtime']}
            self.collectionurllog.insert(urlog)
        return item
