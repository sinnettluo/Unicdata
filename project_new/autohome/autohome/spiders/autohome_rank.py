# -*- coding: utf-8 -*-
import json
import time

import scrapy


class AutohomeRankSpider(scrapy.Spider):
    name = 'autohome_rank'
    allowed_domains = ['autohome.com.cn']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(AutohomeRankSpider, self).__init__(**kwargs)

        self.carnum = 1000000

    is_debug = True
    custom_debug_settings = {
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'autohome_chen',
        'MONGODB_COLLECTION': 'autohome_rank',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',
    }

    def start_requests(self):
        pageindex = '1'
        pm = '2'
        typeid = '2'
        prices = ['', '0', '0-5', '5-8', '8-10', '10-15', '15-20', '20-25', '25-35', '35-50', '50-100', '100-5000']
        fcttypeids = ['0', '1', '2', '3']
        levelids = ['0', '1,2,3,4,5,6', '1', '2', '3', '4', '5', '6', '16,17,18,19,20', '16', '17', '18', '19', '20',
                    '201908', '7', '8', '11', '12', '13', '99']
        cityid = '0'
        provinceid = '0'
        for price in prices:
            for fcttypeid in fcttypeids:
                for levelid in levelids:
                    url = f'https://cars.app.autohome.com.cn/cars_v9.1.0/cars/getseriesranklist.ashx?pageindex={pageindex}&pm={pm}&pluginversion=10.3.0&typeid={typeid}&price={price}&fcttypeid={fcttypeid}&levelid={levelid}&cityid={cityid}&provinceid={provinceid}'
                    yield scrapy.Request(url=url, callback=self.parse,
                                         meta={"info": (pm, typeid, price, fcttypeid, levelid, cityid, provinceid)}, )

    def parse(self, response):
        item = {}
        pm, typeid, price, fcttypeid, levelid, cityid, provinceid = response.meta.get('info')
        typerank = str('')
        fcttype = str('')
        if typeid == '1':
            typerank = '?????????'
        elif typeid == '2':
            typerank = '?????????'
        elif typeid == '3':
            typerank = '?????????'
        elif typeid == '4':
            typerank = '?????????'

        if fcttypeid == '0':
            fcttype = '????????????'
        elif fcttypeid == '1':
            fcttype = '??????'
        elif fcttypeid == '2':
            fcttype = '??????'
        elif fcttypeid == '3':
            fcttype = '??????'
        data = response.text.split("callback(")[-1].replace(')', '')
        json_data = json.loads(data)
        for i in json_data['result']['list']:
            item['grabtime'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            item['typeid'] = typeid
            item['typerank'] = typerank
            item['pm'] = pm
            item['price'] = price
            item['fcttypeid'] = fcttypeid
            item['fcttype'] = fcttype
            item['rank'] = i['lefttitle']
            item['levelid'] = levelid
            item['seriesname'] = i['seriesname']
            item['seriesid'] = i['seriesid']
            item['Sort'] = i['Sort']
            item['url'] = response.url
            item['status'] = response.url + '-' + i['seriesimage']
            yield item
