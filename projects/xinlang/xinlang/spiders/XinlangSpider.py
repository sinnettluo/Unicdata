# -*- coding: utf-8 -*-
import re
import time
from copy import deepcopy

import scrapy
import json
from glom import glom
from uuid import uuid4

from xinlang.items import XinlangItem


class XinlangspiderSpider(scrapy.Spider):
    name = 'XinlangSpider'
    # allowed_domains = ['weibo.cn']
    def __init__(self, **kwargs):
        super(XinlangspiderSpider, self).__init__(**kwargs)
        self.counts = 0
        # self.brand_list = ['华晨中华', '奇瑞', '长安汽车', '众泰', '江淮', '北汽威旺', '北汽昌河', '北汽幻速', '比亚迪', '北京汽车', '本田', '上汽荣威', '哈弗', '哪吒', '雪铁龙', '吉利', '猎豹', '广汽', '东风', '领克']
        self.brand_list = ['宝骏', '雪佛兰']
        self.page_num = 217

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {}, priority='spider')

    is_debug = True
    custom_debug_settings = {
        'MONGODB_SERVER': "192.168.1.94",
        'MONGODB_DB': 'luntan',
        'MONGODB_COLLECTION': 'weibo_baojun',
        'CrawlCar_Num': 800000,
        'CONCURRENT_REQUESTS': 16,
        'DOWNLOAD_DELAY': 0,
    }

    def start_requests(self):
        # for brand in self.brand_list:
        # url = f"https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D60%26q%3D华晨中华%26t%3D0&page_type=searchall&page=2"
        url = f"https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D62%26q%3D华晨中华%26t%3D0&page_type=searchall"
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'MWeibo-Pwa': '1'
        }

        yield scrapy.Request(url=url, headers=headers, callback=self.parse_brand)

    def parse_brand(self, response):
        for brand in self.brand_list:
            # print(brand)
            # print("*"*100)
            # item["_id"] = uuid4().__str__()
            url = f"https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D62%26q%3D{brand}%26t%3D0&page_type=searchall"
            yield scrapy.Request(
                url=url,
                callback=self.parse,
                meta={"brand": brand}
            )

    def parse(self, response):
        brand = response.meta["brand"]
        """获取-更多-微博的接口id"""
        result = json.loads(response.text)
        total = result["data"]["cardlistInfo"]["total"]
        page_num = int(total/12)
        print(total)
        print("*"*100)
        for i in range(1, page_num):
            url1 = f"https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D62%26q%3D{brand}%26t%3D0&page_type=searchall&page={i}"
            url2 = f"https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D60%26q%3D{brand}%26t%3D0&page_type=searchall&page={i}"
            yield scrapy.Request(
                url=url1,
                callback=self.parse_detail,
                meta={"brand": deepcopy(brand)}
            )
            yield scrapy.Request(
                url=url2,
                callback=self.parse_detail,
                meta={"brand": deepcopy(brand)}
            )

    def parse_detail(self, response):
        item = XinlangItem()
        brand = response.meta["brand"]
        content = json.loads(response.text)
        detail_info = content["data"]["cards"]
        if len(detail_info) > 0:
            for info in detail_info:
                # item = XinlangItem()
                if glom(info, 'card_type') == 9:
                    item["brand"] = brand
                    item["_id"] = uuid4().__str__()
                    item["screen_name"] = info["mblog"]["user"]["screen_name"]
                    item["gender"] = info["mblog"]["user"]["gender"]
                    item["user_id"] = info["mblog"]["user"]["id"]
                    item["create_time"] = info["mblog"]["created_at"]
                    item["reposts_count"] = info["mblog"]["reposts_count"]
                    item["comments_count"] = info["mblog"]["comments_count"]
                    item["attitudes_count"] = info["mblog"]["attitudes_count"]
                    item["grabtime"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    info_id = info["mblog"]["id"]
                    item["url"] = f"https://m.weibo.cn/detail/{info_id}"
                    if info["mblog"]["isLongText"] is True:
                        item["text"] = info["mblog"]["longText"]["longTextContent"]
                        # print(item)
                        yield item
                    else:
                        text = info["mblog"]["text"]
                        result = re.findall(u'[\u4e00-\u9fa5]', text)
                        result = "".join(result)
                        item["text"] = result
                        # print(item)
                        yield item


