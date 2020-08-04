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
from hashlib import md5
from scrapy.mail import MailSender
import os
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request
import requests

# class JzgImagePipline(ImagesPipeline):
#     def get_media_requests(self, item, info):
#         for image_url in item['image_urls']:
#             yield Request(image_url)
#
#     def item_completed(self, results, item, info):
#         image_paths = [x['path'] for ok, x in results if ok]
#         if not image_paths:
#             raise DropItem("Item contains no images")
#         item['image_paths'] = image_paths
#         return item

class CarbuisnessPipeline(object):
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
        # bloom file
        filename = 'blm/'+settings['MONGODB_DB']+'/'+settings['MONGODB_COLLECTION']+'.blm'
        # pybloom
        num = (int(settings['CrawlCar_Num'])+self.collection.count())*1.1
        self.df = BloomFilter(capacity=num,error_rate=0.01)
        # read
        isexists = os.path.exists(filename)
        self.fa = open(filename, "a")
        if isexists:
            fr = open(filename, "r")
            lines = fr .readlines()
            for line in lines:
                line = line.strip('\n')
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
        self.counts = 0


    def process_item(self, item, spider):

        # if spider.name == "jzg_price_test":
        #     for i in item:
        #         if i.find("_img") > 0:
        #             img_res = requests.request("get", url=item[i], headers={"accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"})
        #             file_name = item[i].split("?")[-1]
        #             with open("blm/jzg_price_img/"+file_name, "ab") as f:
        #                 f.write(img_res.content)
        #                 f.close()



        if spider.name == "lechebang":
            self.collection.insert(dict(item))
            logging.log(msg="Car added to MongoDB database!", level=logging.INFO)
            self.counts += 1
            logging.log(msg="scrapy                    " + str(self.counts) + "                  items",
                        level=logging.INFO)

            urlog = {'url': item['url'], 'grabtime': item['grabtime']}
            self.collectionurllog.insert(urlog)
            return item

        if spider.name == "":
            self.collection.insert(dict(item))
            urlog = {'url': item['url'], 'grabtime': item['grabtime']}
            self.collectionurllog.insert(urlog)
            pass
        else:
            valid = True
            i = md5(item['status']).hexdigest()
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
                logging.log(msg="scrapy                    " + str(self.counts) + "                  items", level=logging.INFO)
            else:
                logging.log(msg="Car duplicated!", level=logging.INFO)
            #log save
            urlog = {'url': item['url'], 'grabtime': item['grabtime']}
            self.collectionurllog.insert(urlog)
            return item

    def close_spider(self, spider):
        self.connection.close()
        self.fa.close()
        self.mailer.send(to=["huzhangyong@haistand.com.cn"], subject=settings['MONGODB_COLLECTION'], body="Scrapy Finished!",
                         cc=["hzhy_1@163.com"])
