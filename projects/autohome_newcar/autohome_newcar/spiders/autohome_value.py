# -*- coding: utf-8 -*-
import json
import time
from copy import deepcopy

import pymongo
import scrapy
from pybloom_live import ScalableBloomFilter
from scrapy.utils.project import get_project_settings
from hashlib import md5

from autohome_newcar.items import AutohomeNewcarItem

website = 'autohome_value'

settings = get_project_settings()


class AutohomeValueSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['che168.com']
    start_urls = ['http://che168.com/']

    custom_settings = {
        'DOWNLOAD_DELAY': 0,
        'CONCURRENT_REQUESTS': 8,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
    }

    def __init__(self, **kwargs):
        super(AutohomeValueSpider, self).__init__(**kwargs)
        self.counts = 0
        self.carnum = 800000
        self.name = 'autohome_value'
        self.carid = list()

        self.connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = self.connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_READ_COLLECTION']]
        num = (self.collection.count()) * 1.5
        self.df = ScalableBloomFilter(initial_capacity=num, error_rate=0.001)
        # filename = '../blm/' + settings['MONGODB_WRITE_COLLECTION'] + '.blm'
        # filename = settings["BLM_PATH"] + '/' + settings['MONGODB_COLLECTION'] + '.blm'
        # filename = './test.blm'
        # self.fa = open(filename, "a")
        for i in self.collection.find():
            if "familyid" in i.keys():
                item = i["familyid"]
                item = md5(item.encode("utf8")).hexdigest()
                if not self.df.add(item):
                    # self.fa.writelines(i["familyid"] + '\n')
                    self.carid.append(i["familyid"])
        self.connection.close()

    def parse(self, response):
        item = AutohomeNewcarItem()
        for i in self.carid:
            url = f'https://pinguapi.che168.com/v1/assesspublic/seriesofrate?_appid=m.m&seriesid={i}'
            item["carid"] = i
            item["url"] = f'https://www.che168.com/keepvalue/result_{i}.html'
            yield scrapy.Request(
                url=url,
                callback=self.parse_detail_url,
                meta=deepcopy({"item": item}),
                dont_filter=True
            )

    def parse_detail_url(self, response):
        item = response.meta["item"]
        res = json.loads(response.body)
        try:
            item["carinfo"] = res["result"]
        except KeyError:
            item["carinfo"] = []
            print("无数据...")
        url = f'https://www.che168.com/handler/keepvalue/GetKeepValueBySeriesId.ashx?seriesid={item["carid"]}'
        yield scrapy.Request(
            url=url,
            callback=self.parse_num,
            meta={"item": item}
        )

    def parse_num(self, response):
        item = response.meta["item"]
        res = json.loads(response.body)
        if len(item["carinfo"]) != 0:
            for i in range(0, len(item["carinfo"])):
                try:
                    item["carinfo"][i]["sale_num"] = res["result"][i]["num"]
                except:
                    item["carinfo"][i]["sale_num"] = 0
        # print(item)
        item["grab_time"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        yield item