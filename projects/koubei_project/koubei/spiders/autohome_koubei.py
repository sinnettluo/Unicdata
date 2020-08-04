# -*- coding: utf-8 -*-
import scrapy
import re
import json
import time
from koubei.items import YicheKoubeiItem
# from scrapy.conf import settings
import pymongo

# 修改了过滤规则
website ='autohome_koubei_new'

class KoubeiSpider(scrapy.Spider):
    name = website
    # allowed_domains = ['www.bitauto.com']
    start_urls = ['https://www.autohome.com.cn/beijing/']

    def __init__(self, **kwargs):
        super(KoubeiSpider, self).__init__(**kwargs)

        self.carnum = 1000000
        self.settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        self.settings.set('MONGODB_DB', 'koubei', priority='cmdline')
        self.settings.set('MONGODB_COLLECTION', website, priority='cmdline')


    def parse(self, response):

        connection = pymongo.MongoClient("192.168.1.94", 27017)
        db = connection["newcar"]
        collection = db["autohome_newcar"]

        result = collection.distinct("autohomeid")

        for r in result:
            url = "https://dealer.autohome.com.cn/Ajax/GetPraise?specId=%s&pageIndex=1&pageSize=1" % (r)
            # print(url)
            yield scrapy.Request(url, meta={"autohomeid":r}, callback=self.parse_paging)

    def parse_paging(self, response):
        paging_obj = json.loads(response.text)
        paging = paging_obj["result"]["paging"]

        totalCount = paging["totalCount"]

        if totalCount > 0:
            for i in range(1, totalCount+1):
                url = "https://dealer.autohome.com.cn/Ajax/GetPraise?specId=%s&pageIndex=%d&pageSize=1" % (response.meta["autohomeid"], i)
                yield scrapy.Request(url, callback=self.parse_info, dont_filter=True)

    def parse_info(self, response):
        info_obj = json.loads(response.text)
        item = YicheKoubeiItem()

        item['url'] = response.url
        # item['website'] = website
        # item['status'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())

        item['familyname'] = info_obj["result"]["seriesName"]
        # item['brand'] = None
        item['familynameid'] = info_obj["result"]["seriesId"]
        item['shortdesc'] = info_obj["result"]["specName"]

        item['buy_date'] = info_obj["result"]["koubei"][0]["purchasing"]["boughtDate"]
        item['buy_location'] = info_obj["result"]["koubei"][0]["purchasing"]["boughtProvinceName"] + " " + info_obj["result"]["koubei"][0]["purchasing"]["boughtCityName"]
        item['buy_pure_price'] = info_obj["result"]["koubei"][0]["purchasing"]["price"]
        item['buyerid'] = info_obj["result"]["koubei"][0]["author"]["userId"]
        item['buyername'] = info_obj["result"]["koubei"][0]["author"]["nickName"]

        item['mileage'] = info_obj["result"]["koubei"][0]["evaluation"]["drivenKiloms"]
        item['oil_consume'] = info_obj["result"]["koubei"][0]["evaluation"]["actualOilConsumption"]

        item['score'] = info_obj["result"]["koubei"][0]["evaluation"]["average"]
        item['score_appearance'] = info_obj["result"]["koubei"][0]["evaluation"]["apperance"]
        item['score_comfort'] = info_obj["result"]["koubei"][0]["evaluation"]["comfortableness"]
        item['score_control'] = info_obj["result"]["koubei"][0]["evaluation"]["maneuverability"]
        item['score_cost'] = info_obj["result"]["koubei"][0]["evaluation"]["costEfficient"]
        item['score_fuel'] = info_obj["result"]["koubei"][0]["evaluation"]["oilConsumption"]
        item['score_power'] = info_obj["result"]["koubei"][0]["evaluation"]["power"]
        item['score_space'] = info_obj["result"]["koubei"][0]["evaluation"]["space"]
        item['score_trim'] = info_obj["result"]["koubei"][0]["evaluation"]["internal"]

        # item['ucid'] = None
        item['guideprice'] = None
        usage = []
        for i in range(len(info_obj["result"]["koubei"][0]["evaluation"]["purposes"])):
            usage.append(info_obj["result"]["koubei"][0]["evaluation"]["purposes"][i]["name"])
        item['usage'] = "|".join(usage)
        item['fuel'] = None
        item['comment_detail'] = None
        item['comment_people'] = None
        item['isGoodComment'] = None
        item['picurl'] = None
        item['score_star'] = None

        item['visitCount'] = info_obj["result"]["koubei"][0]["interactivation"]["visitCount"]
        item['helpfulCount'] = info_obj["result"]["koubei"][0]["interactivation"]["helpfulCount"]
        item['commentCount'] = info_obj["result"]["koubei"][0]["interactivation"]["commentCount"]
        item['post_time'] = info_obj["result"]["koubei"][0]["created"]
        item['spec_id'] = info_obj["result"]["specId"]
        item['description'] = None

        feeling = info_obj["result"]["koubei"][0]["evaluation"]["feeling"]
        satisfied = re.findall("【最满意的一点】(.*?)【", feeling, re.S)
        if satisfied:
            item['satisfied'] = re.findall("【最满意的一点】(.*?)【", feeling, re.S)[0].strip()
        unsatisfied = re.findall("【最不满意的一点】(.*?)【", feeling, re.S)
        if unsatisfied:
            item['unsatisfied'] = re.findall("【最不满意的一点】(.*?)【", feeling, re.S)[0].strip()
        score_appearance_compare = re.findall("【外观】(.*?)【", feeling, re.S)
        if score_appearance_compare:
            item['score_appearance_compare'] = re.findall("【外观】(.*?)【", feeling, re.S)[0].strip()
        score_comfort_compare = re.findall("【舒适性】(.*?)【", feeling, re.S)
        if score_comfort_compare:
            item['score_comfort_compare'] = re.findall("【舒适性】(.*?)【", feeling, re.S)[0].strip()
        score_control_compare = re.findall("【操控】(.*?)【", feeling, re.S)
        if score_control_compare:
            item['score_control_compare'] = re.findall("【操控】(.*?)【", feeling, re.S)[0].strip()
        score_cost_compare = re.findall("【性价比】(.*?)【", feeling, re.S)
        if score_cost_compare:
            item['score_cost_compare'] = re.findall("【性价比】(.*?)【", feeling, re.S)[0].strip()
        score_fuel_compare = re.findall("【油耗】(.*?)【", feeling, re.S)
        if score_fuel_compare:
            item['score_fuel_compare'] = re.findall("【油耗】(.*?)【", feeling, re.S)[0].strip()
        score_power_compare = re.findall("【动力】(.*?)【", feeling, re.S)
        if score_power_compare:
            item['score_power_compare'] = re.findall("【动力】(.*?)【", feeling, re.S)[0].strip()
        score_space_compare = re.findall("【空间】(.*?)【", feeling, re.S)
        if score_space_compare:
            item['score_space_compare'] = re.findall("【空间】(.*?)【", feeling, re.S)[0].strip()
        score_trim_compare = re.findall("【内饰】(.*?)【", feeling, re.S)
        if score_trim_compare:
            item['score_trim_compare'] = re.findall("【内饰】(.*?)【", feeling, re.S)[0].strip()
        item['status'] = str(item['spec_id']) + "-" + str(item['buyerid']) + "-" + str(item['buy_location']) + "-" + str(item['buy_date']) + "-" + str(item['buy_pure_price']) + "-" + str(item['visitCount']) + "-" + str(item['helpfulCount']) + "-" + str(item['commentCount'])
        yield item