# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import os

import pymongo
from pybloom_live import ScalableBloomFilter
from scrapy.exceptions import DropItem
import pandas as pd
from hashlib import md5

from sqlalchemy import create_engine


class XinlangPipeline(object):
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def __init__(self, settings):
        # mysql
        # self.conn = create_engine(
        #     f'mysql+pymysql://{settings["MYSQL_USER"]}:{settings["MYSQL_PWD"]}@{settings["MYSQL_SERVER"]}:{settings["MYSQL_PORT"]}/{settings["MYSQL_DB"]}?charset=utf8')
        # mongo
        self.connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = self.connection[settings['MONGODB_DB']]

        # count
        self.mongocounts = 0
        self.dropcounts = 0

        # mongo
        self.collection = self.db[settings['MONGODB_COLLECTION']]

        # bloomfilter
        try:
            num = (int(settings['CRAWL_NUM']) + self.collection.count()) * 1.5
        except:
            num = settings['CRAWL_NUM']
        self.df = ScalableBloomFilter(initial_capacity=num, error_rate=0.001)

        self.settings = settings

    @property
    def fa(self):
        return self._fa

    @fa.setter
    def fa(self, value):
        self._fa = value

    def open_spider(self, spider):
        if spider.name == 'yiche_koubei':
            # bloom file
            current_dir = os.path.abspath(os.path.dirname(__file__))
            up_dir = os.path.abspath(os.path.dirname(current_dir))
            filename = spider.name + '.blm'
            filedir = up_dir + '/blm/' + self.settings['MONGODB_DB']
            if not os.path.exists(filedir):
                os.makedirs(filedir)
            filepath = filedir + "/" + filename

            # read
            isexists = os.path.exists(filepath)
            self.fa = open(filepath, "a")
            if isexists:
                fr = open(filepath, "r")
                lines = fr.readlines()
                for line in lines:
                    line = line.strip('\n')
                    self.df.add(line)
                fr.close()
            else:
                for i in self.collection.find():
                    if "url" in i.keys():
                        item = i["url"]
                        item = md5(item.encode("utf8")).hexdigest()
                        self.df.add(item)
                        spider.fa.writelines(item + '\n')
        # elif spider.name == 'ouyeel':
        #     self.collection = self.db[settings['MONGODB_COLLECTION_OY']]

    def process_item(self, item, spider):
        if spider.name == 'yiche_koubei':
            valid = True
            i = md5(item['url'].encode("utf8")).hexdigest()
            returndf = self.df.add(i)
            # print(returndf)
            # if not returndf and item["price1"] is not None and '天' in item["post_time"] and int(
            #         re.findall('(.*?)天', item["post_time"])[0]) > 3:
            #     valid = True
            # else:
            #     valid = False
            #     raise DropItem(f"Unqualified data! --> {item['url']}")
            if not returndf:
                valid = True
            else:
                valid = False
                # raise DropItem(f"isexists data! --> {item['url']}")

            if valid:
                # 刷新缓存区
                self.fa.flush()
                self.fa.writelines(i + '\r\n')
                # 数据存入mongo
                self.collection.insert(dict(item))
                logging.log(msg="data added to MongoDB database!", level=logging.INFO)
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
                # pd.io.sql.to_sql(df, name=settings['MONGODB_COLLECTION_YCKB'], con=self.conn, if_exists="append", index=False)
                # pd.io.sql.to_sql(df, name=settings['MYSQL_TABLE'], con=self.conn, if_exists="append")

            else:
                # self.dropcounts += 1
                raise DropItem(f"isexists data! --> {item['url']}")
        else:
            self.collection.insert(item)
            logging.log(msg="data added to MongoDB database!", level=logging.INFO)
            self.mongocounts += 1
            logging.log(msg=f"scrapy              {self.mongocounts}              items", level=logging.INFO)
            # 数据存入mysql
            items = list()
            items.append(item)
            df = pd.DataFrame(items)
            # mysql
            conn = create_engine(f'mysql+pymysql://{self.settings["MYSQL_USER"]}:{self.settings["MYSQL_PWD"]}@{self.settings["MYSQL_SERVER"]}:{self.settings["MYSQL_PORT"]}/{self.settings["MYSQL_DB"]}?charset=utf8')
            df.to_sql(name=self.settings['MONGODB_COLLECTION'], con=conn, if_exists="append", index=False)
        return item

    def close_spider(self, spider):
        if spider.name == 'yizhe_koubei':
            self.connection.close()
            # self.conn.dispose()
            self.fa.close()
        else:
            self.connection.close()
            # self.conn.dispose()

