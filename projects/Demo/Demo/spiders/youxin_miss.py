# -*- coding: utf-8 -*-
import scrapy
import time
import json
import re
import pymysql
import pandas as pd
import numpy as np
from datetime import datetime
import time


# from .items import YouxinMissSpider Item
def readMysqls(sql):
    dbconn = pymysql.connect(
        host="192.168.1.94",
        database='usedcar_update',
        user="dataUser94",
        password="94dataUser@2020",
        port=3306,
        charset='utf8')
    # 查询
    sqlcmd = sql
    df = pd.read_sql(sqlcmd, dbconn)
    return df


class YouxinMissSpider(scrapy.Spider):
    name = 'youxin_miss'
    # allowed_domains = ['youxin.com']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(YouxinMissSpider, self).__init__(**kwargs)
        self.counts = 0
        sql = "SELECT * from youxin_online WHERE grab_time>= '2019'"
        # sql = "SELECT * from che168_online WHERE grab_time>= '2019'"
        df_tmps = readMysqls(sql)
        df = df_tmps.copy()
        df = df.drop_duplicates('url')
        field_list = ["carid", "newcarid", "car_source", "grab_time", "post_time", "sold_date", "pagetime", "url",
                      "status",
                      "registerdate", "price1", "mileage", "prov", "city", "img_url"]
        df_1 = df.loc[:, field_list].copy()
        self.df_no_img = df_1[df_1["img_url"].isnull()]

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'usedcar_update',
        'MYSQL_TABLE': 'youxin_miss',
        'MONGODB_SERVER': '192.168.1.94',
        'MONGODB_DB': 'usedcar_update',
        'MONGODB_COLLECTION': 'youxin_miss',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 5,
        'COOKIES_ENABLED': False,
        'DOWNLOADER_MIDDLEWARES': {
            'Demo.middlewares.DemoProxyMiddleware': 700,
        },
        'ITEM_PIPELINES': {
            'Demo.pipelines.DemoPipeline': 300,
        },

    }

    def start_requests(self):
        for index, rows in self.df_no_img.iterrows():
            url = rows["url"]
            meta = {
                "url": rows["url"],
                "carid": rows["carid"],
                "newcarid": rows["newcarid"],
                "car_source": rows["car_source"],
                "grab_time": rows["grab_time"],
                "post_time": rows["post_time"],
                "sold_date": rows["sold_date"],
                "pagetime": rows["pagetime"],
                "registerdate": rows["registerdate"],
                "price1": rows["price1"],
                "mileage": rows["mileage"],
                "prov": rows["prov"],
                "city": rows["city"],
            }
            yield scrapy.Request(
                url=url,
                meta=meta,
            )

    def parse(self, response):
        item = dict()
        item["carid"] = response.meta["carid"]
        item["newcarid"] = response.meta["newcarid"]
        item["car_source"] = response.meta["car_source"]
        item["grab_time"] = response.meta["grab_time"]
        item["post_time"] = response.meta["post_time"]
        item["sold_date"] = response.meta["sold_date"]
        item["pagetime"] = response.meta["pagetime"]
        item["registerdate"] = response.meta["registerdate"]
        item["price1"] = response.meta["price1"]
        item["mileage"] = response.meta["mileage"]
        item["prov"] = response.meta["prov"]
        item["city"] = response.meta["city"]
        item["url"] = response.meta["url"]
        item["img_url"] = response.xpath("//img[@class='cd_m_info_mainimg']/@data-src").get()
        print(item)
        yield item
