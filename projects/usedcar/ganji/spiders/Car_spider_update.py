#-*- coding: UTF-8 -*-
import scrapy
from SpiderInit import spider_update_Init

class update(scrapy.Spider):

    #basesetting
    name = 'update'

    def __init__(self,**kwargs):
        # args
        super(update, self).__init__(**kwargs)
        ##setting
        self.size=100
        self.reqcounts=0
        self.urllist=[]

    def start_requests(self):
        requstlist = []
        self.size = min(self.carnum,self.size)
        for i in range(0,self.size):
            url = self.urllist[i]
            if url:
                list = scrapy.Request(url,callback=self.parse_car, errback=self.error_parse)
                requstlist.append(list)
        self.reqcounts = self.reqcounts + self.size
        return (requstlist)

    def request_next(self):
        request_count = self.crawler.stats.get_value('downloader/request_count')
        addcounts = False
        if request_count >= self.reqcounts - self.size / 10 and self.reqcounts < self.carnum:
            self.size = min(self.size, self.carnum - self.reqcounts)
            if request_count >= self.reqcounts:
                self.reqcounts = self.reqcounts + self.size
            addcounts = True
        return addcounts

    def error_parse(self, response):
        addcounts = self.request_next()
        if addcounts:
            self.size = min(self.size, self.carnum - self.reqcounts)
            for i in range(self.reqcounts, self.reqcounts + self.size):
                url = self.urllist[i]
                if url:
                    yield scrapy.Request(url, callback=self.parse_car, errback=self.error_parse)