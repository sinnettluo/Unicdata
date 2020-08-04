# -*- coding: utf-8 -*-
"""
C2017-41
bochewang 博车网

"""
import scrapy
from carbuisness.items import ChezhiwangRankItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5
import calendar

website='chezhiwang_rank'

class CarSpider(scrapy.Spider):
    name=website
    # start_urls=['http://www.12365auto.com/ranking/']


    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=100000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    def start_requests(self):
        for y in range(2017, 2019):
            for m in range(1, 13):
                day = calendar.monthrange(y,m)[1]
                data = {
                    "stime": str(y) + "-" + str(m) + "-" + "1",
                    "etime": str(y) + "-" + str(m) + "-" + str(day),
                }
                url = "http://www.12365auto.com/ranking/index.aspx"
                yield scrapy.FormRequest(method="post", url=url, formdata=data, meta=data)

    def parse(self,response):
        trs = response.xpath("//*[@class='ar_ft']/tbody/tr")
        print(trs)

        for tr in trs[1:-1]:
            item = dict()
            item["rank"] = tr.xpath("td[1]/text()").extract_first()
            item["brand"] = tr.xpath("td[2]/text()").extract_first()
            item["familyname"] = tr.xpath("td[3]/a/text()").extract_first()
            item["familyid"] = tr.xpath("td[3]/@sid").extract_first()
            item["type"] = tr.xpath("td[4]/text()").extract_first()
            item["brandtype"] = tr.xpath("td[5]/text()").extract_first()
            item["country"] = tr.xpath("td[6]/text()").extract_first()
            item["number"] = tr.xpath("td[8]/text()").extract_first()
            item["status"] = item["rank"]
            item['stime'] = response.meta["stime"]
            item['etime'] = response.meta["etime"]
            url = "http://www.12365auto.com/server/forRankingT.ashx?sid=%s&act=getTopRaking_Ne&ba=0&bt=-1&cp=0&z=0&st=%s&et=%s" % (item["familyid"], item["stime"], item["etime"])
            yield scrapy.Request(url=url, meta={"item":item}, callback=self.parse_final)

    def parse_final(self, response):
        problem_list = list()
        problems = json.loads(response.text)["config"][0]["config"]
        for problem in problems:
            problem_list.append(problem["CtiInfo"])
        item = ChezhiwangRankItem()
        item["grabtime"] = time.strftime('%Y-%m-%d %X', time.localtime())
        item["url"] = response.url
        item["rank"] = response.meta["item"]["rank"]
        item["brand"] = response.meta["item"]["brand"]
        item["familyname"] = response.meta["item"]["familyname"]
        item["familyid"] = response.meta["item"]["familyid"]
        item["type"] = response.meta["item"]["type"]
        item["brandtype"] = response.meta["item"]["brandtype"]
        item["country"] = response.meta["item"]["country"]
        item["number"] = response.meta["item"]["number"]
        item["status"] = response.meta["item"]["rank"] + "-" + response.url
        item["problems"] = ",".join(problem_list)
        item["stime"] = response.meta["item"]["stime"]
        item["etime"] = response.meta["item"]["etime"]

        yield item



