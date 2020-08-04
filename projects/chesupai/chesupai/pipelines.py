# -*- coding: utf-8 -*-
import logging
import os
import re

import pandas as pd
from sqlalchemy import create_engine
import pymysql
import pymongo
from scrapy.mail import MailSender
from scrapy.utils.project import get_project_settings
from pybloom_live import BloomFilter
from pybloom_live import ScalableBloomFilter
from hashlib import md5
from scrapy.exceptions import DropItem


settings = get_project_settings()


class ChesupaiPipeline(object):
    def __init__(self):
        # mysql
        self.conn = create_engine(f'mysql+pymysql://{settings["MYSQL_USER"]}:{settings["MYSQL_PWD"]}@{settings["MYSQL_SERVER"]}:{settings["MYSQL_PORT"]}/{settings["MYSQL_DB"]}?charset=utf8')

        # mail
        self.mailer = MailSender.from_settings(settings)
        # mongo
        self.connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = self.connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
        self.collectionurllog = db[settings['MONGODB_COLLECTION'] + "_urllog"]
        self.collectionwrong = db[settings['MONGODB_COLLECTION'] + "_wrongurllog"]
        # bloom file
        # current_dir = os.path.abspath(os.path.dirname(__file__))
        # up_dir = os.path.abspath(os.path.dirname(current_dir))
        # filename = settings['MONGODB_COLLECTION'] + '.blm'
        # filedir = up_dir + '/blm/' + settings['MONGODB_DB']
        # if not os.path.exists(filedir):
        #     os.makedirs(filedir)
        # filepath = filedir + "/" + filename
        filename = 'blm/' + settings['MONGODB_DB'] + '/' + settings['MONGODB_COLLECTION'] + '.blm'
        # filename = settings["BLM_PATH"] + '/' + settings['MONGODB_COLLECTION'] + '.blm'
        # pybloom
        num = (int(settings['CRAWL_NUM']) + self.collection.count()) * 1.5
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
                if "statusplus" in i.keys():
                    item = i["statusplus"]
                    item = md5(item.encode("utf8")).hexdigest()
                    self.df.add(item)
                    self.fa.writelines(item + '\n')
        # count
        self.mongocounts = 0

    def process_item(self, item, spider):
        valid = True
        i = md5(item['statusplus'].encode("utf8")).hexdigest()
        # print(i)
        returndf = self.df.add(i)
        # print(returndf)

        # if not returndf and item["price1"] is not None and '天' in item["post_time"] and int(re.findall('(.*?)天', item["post_time"])[0]) > 3:
        if not returndf and item["price1"] is not None:
            valid = True
        else:
            valid = False
            raise DropItem(f"Unqualified data! --> {item['url']}")

        # print(valid)
        # print("*"*100)

        if valid:
            # 刷新缓存区
            self.fa.flush()
            self.fa.writelines(i + '\r\n')
            # 数据存入mongo
            self.collection.insert(dict(item))
            logging.log(msg="Car added to MongoDB database!", level=logging.INFO)
            self.mongocounts += 1
            logging.log(msg=f"scrapy              {self.mongocounts}              items", level=logging.INFO)
            # 数据存入mysql
            items = list()
            items.append(item)
            df = pd.DataFrame(items)
            # if spider.name == "evp_fix2":
            #     conn = create_engine('mysql+pymysql://root:Datauser@2017@192.168.1.94:3306/koubei2?charset=utf8mb4')
            #     pd.io.sql.to_sql(df, name=settings['MONGODB_COLLECTION'], con=conn, if_exists="append")
            # else:
            pd.io.sql.to_sql(df, name=settings['MYSQL_TABLE'], con=self.conn, if_exists="append", index=False)

        else:
            logging.log(msg="Car info isexists!", level=logging.INFO)
            raise DropItem(f"Unqualified data! --> {item['url']}")
        # log save
        urlog = {'url': item['url'], 'grab_time': item['grab_time']}
        self.collectionurllog.insert(urlog)
        return item

    def close_spider(self, spider):
        self.connection.close()
        self.conn.dispose()
        self.fa.close()
