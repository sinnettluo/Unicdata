# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from scrapy.exceptions import DropItem
from pybloom_live import ScalableBloomFilter
from hashlib import md5
import pathlib
import os
import time
import logging
import pymongo
import pandas as pd
from scrapy import signals
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class YongdaPipeline(object):

    @classmethod
    def from_crawler(cls, crawler):
        # 获取配置中的时间片个数，默认为12个，1分钟
        idle_number = crawler.settings.getint('IDLE_NUMBER', 6)
        # 实例化扩展对象
        ext = cls(crawler.settings, idle_number, crawler)
        # 将扩展对象连接到信号， 将signals.spider_idle 与 spider_idle() 方法关联起来。
        crawler.signals.connect(ext.spider_idle, signal=signals.spider_idle)
        return ext

    def __init__(self, settings, idle_number, crawler):
        # mysql
        self.conn = create_engine(f'mysql+pymysql://{settings["MYSQL_USER"]}:{settings["MYSQL_PWD"]}@{settings["MYSQL_SERVER"]}:{settings["MYSQL_PORT"]}/{settings["MYSQL_DB"]}?charset=utf8')

        # mongo
        # uri = f'mongodb://{settings["MONGODB_USER"]}:{settings["MONGODB_PWD"]}@{settings["MONGODB_SERVER"]}:{settings["MONGODB_PORT"]}/'
        # self.connection = pymongo.MongoClient(uri)
        # self.connection = pymongo.MongoClient(
        #     settings['MONGODB_SERVER'],
        #     settings['MONGODB_PORT']
        # )
        # db = self.connection[settings['MONGODB_DB']]
        # self.collection = db[settings['MONGODB_COLLECTION']]

        # count
        self.mongocounts = 0
        self.counts = 0
        self.CrawlCar_Num = 1000000
        self.settings = settings

        # redis 信号
        self.crawler = crawler
        self.idle_number = idle_number
        self.idle_list = []
        self.idle_count = 0

        # bloom file
        filename = str(pathlib.Path.cwd()) + '/blm/' + settings['MYSQL_DB'] + '/' + settings['MYSQL_TABLE'] + '.blm'
        dirname = str(pathlib.Path.cwd()) + '/blm/' + settings['MYSQL_DB']

        # scrapy date
        self.start_date = None
        self.end_date = None
        self.scrapy_date = f'{self.start_date}  -   {self.end_date}'

        # dataframe
        self.df_result = pd.DataFrame()

        # 布隆过滤
        self.df = ScalableBloomFilter(initial_capacity=self.CrawlCar_Num, error_rate=0.01)
        # self.df = BloomFilter(capacity=self.CrawlCar_Num, error_rate=0.01)

        # read
        if os.path.exists(dirname):
            if os.path.exists(filename):
                self.fa = open(filename, "a")
            else:
                pathlib.Path(filename).touch()
                self.fa = open(filename, "a")
        else:
            os.makedirs(dirname)
            pathlib.Path(filename).touch()
            self.fa = open(filename, "a")

        with open(filename, "r") as fr:
            lines = fr.readlines()
            for line in lines:
                line = line.strip('\n')
                self.df.add(line)

    def open_spider(self, spider):
        self.start_date = time.strftime('%Y-%m-%d %X', time.localtime())

    def process_item(self, item, spider):
        if spider.name == '':
            valid = True
            i = md5(item[''].encode("utf8")).hexdigest()
            returndf = self.df.add(i)
            if returndf:
                valid = False
                raise DropItem("Drop data {0}!".format(item["statusplus"]))
            else:
                pass
            if valid:
                self.fa.writelines(i + '\n')
                # 数据存入mysql
                items = list()
                items.append(item)
                df = pd.DataFrame(items)
                df.to_sql(name=self.settings['MYSQL_TABLE'], con=self.conn, if_exists="append", index=False)
                logging.log(msg=f"scrapy              {self.mongocounts}              items", level=logging.INFO)
                self.mongocounts += 1
                # if spider.name == '':
                    # self.df_result = pd.concat([self.df_result, df])
                    # self.mongocounts += 1
                    # logging.log(msg=f"add              {self.mongocounts}              items", level=logging.INFO)
                # else:
                    # df.to_sql(name=self.settings['MYSQL_TABLE'], con=self.conn, if_exists="append", index=False)
                    # self.mongocounts += 1
                    # logging.log(msg=f"scrapy              {self.mongocounts}              items", level=logging.INFO)

    def close_spider(self, spider):
        # self.connection.close()
        # if spider.name == '':
            # self.df_result.to_sql(name=self.settings['MYSQL_TABLE'], con=self.conn, if_exists="append", index=False)
        self.conn.dispose()
        self.end_date = time.strftime('%Y-%m-%d %X', time.localtime())
        self.scrapy_date = f'{self.start_date}  -   {self.end_date}'
        logging.info(self.scrapy_date)

    def spider_idle(self, spider):
        self.idle_count += 1  # 空闲计数
        self.idle_list.append(time.time())  # 每次触发 spider_idle时，记录下触发时间戳
        idle_list_len = len(self.idle_list)  # 获取当前已经连续触发的次数
        print(self.scrapy_date)
        logging.info(self.scrapy_date)
        # print(idle_list_len)
        # print(self.idle_count)
        # print(self.idle_list[-1] - self.idle_list[-2])
        # 判断 当前触发时间与上次触发时间 之间的间隔是否大于5秒，如果大于5秒，说明redis 中还有key
        if idle_list_len > 2 and not (1 < (self.idle_list[-1] - self.idle_list[-2]) < 6):
            self.idle_list = [self.idle_list[-1]]
            self.idle_count = 1

        elif idle_list_len == self.idle_number + 1:
            # 空跑一分钟后记录结束时间
            self.end_date = time.strftime('%Y-%m-%d %X', time.localtime())
            self.scrapy_date = f'{self.start_date}  -   {self.end_date}'
            self.start_date = time.strftime('%Y-%m-%d %X', time.localtime())
            print(self.scrapy_date)
            print("*"*100)

        elif idle_list_len > self.idle_number + 12:
            # 空跑一分钟后重置起始时间
            self.start_date = time.strftime('%Y-%m-%d %X', time.localtime())
            self.idle_count = 0

            # 触发n次以后,开始存取数据
            # if spider.name in ['ouyeel_detail', 'ouyeel_jj']:
            #     self.df_end.to_sql(name=self.settings['MONGODB_COLLECTION'] + '_tmp', con=self.conn, if_exists="append", index=False)
            #     logging.log(msg=f"add              {self.mongocounts}             mysql", level=logging.INFO)
            #     self.df_end = pd.DataFrame()
            #     print("*" * 100)
            # # 连续触发的次数达到配置次数后关闭爬虫
            # # 执行关闭爬虫操作
            # self.crawler.engine.close_spider(spider, 'closespider_pagecount')

