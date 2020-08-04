# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymongo
from scrapy.utils.project import get_project_settings

from scrapy.exceptions import DropItem

settings = get_project_settings()


class AutohomeNewcarPipeline(object):
    def __init__(self):
        self.mongocounts = 0
        self.connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = self.connection[settings['MONGODB_DB_SAVE']]
        self.collection = db[settings['MONGODB_WRITE_COLLECTION']]

    def process_item(self, item, spider):
        logging.log(msg="Car added to MongoDB database!", level=logging.INFO)
        self.mongocounts += 1
        logging.log(msg=f"scrapy              {self.mongocounts}              items", level=logging.INFO)
        if len(item["carinfo"]) == 0:
            raise DropItem(f"Unqualified data! --> {item['url']}")
        else:
            self.collection.insert(item)
        return item

    def close_spider(self, spider):
        self.connection.close()

