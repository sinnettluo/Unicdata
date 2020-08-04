#-*- coding: UTF-8 -*-
import scrapy
from ..items import che300_price
import time
from hashlib import md5
from SpiderInit import spider_original_Init
from SpiderInit import spider_new_Init
from SpiderInit import spider_update_Init
from SpiderInit import dfcheck
from SpiderInit import dffile
from Car_spider_update import update
import csv
import datetime
import json
import MySQLdb
import random

website ='che300_price_daily'
spidername_new = 'che300_price_daily_new'
spidername_update = 'che300_price_daily_update_old'
from scrapy.conf import settings
update_code = settings["UPDATE_CODE"]

#main
class CarSpider(scrapy.Spider):
    name = website
    allowed_domains = ["che300.com"]

    def __init__(self,part=0, parts=1,*args,**kwargs):
        # args
        super(CarSpider, self).__init__(*args, **kwargs)
        # setting
        self.tag = 'original'
        self.counts = 0
        self.carnum = 20000000
        self.dbname = 'usedcar_evaluation'
        # spider setting
        spider_original_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        self.df = 'none'
        self.fa = 'none'
        self.part=int(part)
        self.parts=int(parts)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
        }


    #pro_city select
    #brandselect
    def start_requests(self):
        #this month
        thismonth =datetime.date.today().month
        #modellist
        with open('blm/'+self.dbname+'/modellist.csv', 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            modellist = [row for row in reader]
        #citylist
        with open('blm/'+self.dbname+'/citylist.csv', 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            citylist = [row for row in reader]
        step=len(modellist)/self.parts+1
        starti = self.part * step
        if self.part==self.parts-1:
            step = len(modellist) - starti
        #urllist
        # for city in citylist[2:3]:
        #     for model in modellist[starti:(starti+step)]:
        #         for year in range(int(model['min_reg_year']),int(model['max_reg_year'])+1):
        #             for month in range(1,13):
        #                 date = str(year)+'-'+str(month)
        #                 mile = 0.1
        mysqlconnection = MySQLdb.connect("192.168.1.94", "root", "Datauser@2017", 'for_android', 3306)
        dbc = mysqlconnection.cursor()
        mysqlconnection.set_character_set('utf8')
        dbc.execute('SET NAMES utf8;')
        dbc.execute('SET CHARACTER SET utf8;')
        dbc.execute('SET character_set_connection=utf8;')

        sql = "select * from che300_api_table"
        dbc.execute(sql)
        res = dbc.fetchall()

        with open("/root/che300.json") as f:
        # with open("D:/che300.json") as f:
            fix_list_str = f.read()
            f.close()
        fix_list = json.loads(fix_list_str)
        print(fix_list)

        for row in res:
            # devicd_id = int(random.random() * 100000000000000)
            # str_list = list("AiYFDzzOetCTfRcEelKjETIGc4v5i1ohdmOSL0q8e9P")
            # random.shuffle(str_list)
            # device_token = ''.join(str_list) + "_"
            # rlat = round(random.random() * 10, 2)
            # rlng = round(random.random() * 100, 2)
            # url ="https://dingjia.che300.com/app/EvalResult/newGetBaseEvalPrice?" \
            #      "&prov=" + str(row[1]) +"&city=" + str(row[2]) + \
            #      "&brand=" + str(row[3]) + "&series=" + str(row[4]) + \
            #      "&model=" + str(row[5]) + "&regDate=" + row[6] + "&mile=" + str(row[7]) + "&sign=" + str(row[9]) + "&from=android&device_id=" + str(devicd_id)
            # url = url + "&lat=%d&lng=%d" % (rlat, rlng)
            # url = url + "&device_token=%s" % device_token

            if row[5] in fix_list:

                for m in modellist:
                    if m["salesdescid"] == row[5]:
                        max_year = m["max_reg_year"]
                        min_year = m["min_reg_year"]

                sample = "1234567890abcd"
                random_str = ""
                for i in range(12):
                    random_str = random_str + sample[random.randint(0,11)]
                print(random_str)

                data = {
                    "sign": row[9],
                    "device_id": "android_aba79407-4d8d-3b39-9072-%s" % random_str,
                    "params": '{"brand":"%s","city":"%s","max_reg_Year":%s,"mile":"%s","min_reg_year":%s,"model":"%s","prov":"%s","reg_date":"%s","series":"%s","type":"2"}' % (str(row[3]), str(row[2]), str(max_year), str(row[7]), str(min_year), str(row[5]), str(row[1]), str(row[6]), str(row[4])),
                    "app_type": "android_price",
                }


                url = "https://dingjia.che300.com/demo/evaluate/getSignedBaseEvalPriceByJson"
                # if not (dfcheck(self.df, url, self.tag)):
                meta =dict()
                meta['provid']= row[1]
                meta['cityid']= row[2]
                meta['salesdescid']= row[5]
                meta['regDate']= row[6]
                meta['mile']= str(row[7])

                yield scrapy.Request(method="get", url=url, meta={"datainfo":meta, "data":data}, headers=self.headers, callback=self.parse, dont_filter=True)
                # yield  scrapy.FormRequest(method="post", url=url, meta={"datainfo":meta}, formdata=data, headers=self.headers, callback=self.parse, dont_filter=True)

    def parse(self, response):
        item = che300_price()
        item = dict(item ,**response.meta['datainfo'])
        item['url'] = response.url

        # if response.text.find("签名有误") >= 0:
        #     with open("/root/sign_error_log.log", "a") as f:
        #         f.write(response.url)
        #         f.write("-")
        #         f.write(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))
        #         f.write("\n")
        #         f.close()
        #     return


        # data = json.loads(response.text.replace('"{"', '{"').replace('"}"', '"}'))
        data = json.loads(response.text)
        # print(data)
        # if response.xpath('//p/text()').re('\{\"success.*\}\]\}'):
        #     # dffile
        #     dffile(self.fa, response.url, self.tag)
        #     data = json.loads(response.xpath('//p/text()').re('\{\"success.*\}\]\}')[0])['success']



        try:
            item['price1'] = data["data"]["evalResult"]["dealer_low_buy_price"]
            item['price2'] = data["data"]["evalResult"]["dealer_buy_price"]
            item['price3'] = data["data"]["evalResult"]["individual_low_sold_price"]
            item['price4'] = data["data"]["evalResult"]["individual_price"]
            item['price5'] = data["data"]["evalResult"]["dealer_low_sold_price"]
            item['price6'] = data["data"]["evalResult"]["dealer_price"]
            item['price7'] = data["data"]["evalResult"]["dealer_high_sold_price"]
        except Exception as e:
            # yield scrapy.Request(url=response.url, meta={"datainfo": response.meta}, headers=self.headers, callback=self.parse, dont_filter=True)
            return

        item["default"] = data["data"]["factors"]["default"]
        item["excellent"] = data["data"]["factors"]["excellent"]
        item["good"] = data["data"]["factors"]["good"]
        item["normal"] = data["data"]["factors"]["normal"]

        try:
            item["label_two_price"] = data["data"]["newCarPrice"]["price"]
        except Exception as e:
            item["label_two_price"] = "-"

        item["b2c_price"] = data["data"]["b2c_price"]

        # item['saleRate1'] = data[0]['saleRate']
        # item['saleRate2'] = data[1]['saleRate']
        # item['saleRate3'] = data[2]['saleRate']
        # item['saleRate4'] = data[3]['saleRate']
        # item['saleRate5'] = data[4]['saleRate']
        # item['saleRate6'] = data[5]['saleRate']
        # item['saleRate7'] = data[6]['saleRate']
        # item['saleDateRange1'] = data[0]['saleDateRange']
        # item['saleDateRange2'] = data[1]['saleDateRange']
        # item['saleDateRange3'] = data[2]['saleDateRange']
        # item['saleDateRange4'] = data[3]['saleDateRange']
        # item['saleDateRange5'] = data[4]['saleDateRange']
        # item['saleDateRange6'] = data[5]['saleDateRange']
        # item['saleDateRange7'] = data[6]['saleDateRange']
        item['status'] = md5(".".join(str(item.values())) + "-" + update_code).hexdigest()
        item['grabtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

        # print(item)
        yield item


# new
class CarSpider_new(CarSpider):

    # basesetting
    name = spidername_new

    def __init__(self,part=0, parts=1,*args,**kwargs):
        # args
        super(CarSpider_new, self).__init__(**kwargs)
        # tag
        self.tag = 'new'
        # spider setting
        self.df = spider_new_Init(
            spidername=spidername_new,
            dbname=self.dbname,
            website=website,
            carnum=self.carnum)
        filename = 'blm/' + self.dbname + '/' + spidername_new + ".blm"
        self.fa = open(filename, "a")
        self.part = int(part)
        self.parts = int(parts)

#update
class CarSpider_update(CarSpider,update):

    #basesetting
    name = spidername_update

    def __init__(self,part=0, parts=1,*args,**kwargs):
        # load
        super(CarSpider_update, self).__init__(**kwargs)
        #settings
        self.urllist = spider_update_Init(
            dbname=self.dbname,
            website=website,
            carnum=self.carnum
        )
        self.carnum = len(self.urllist)
        self.tag='update'
        self.part = int(part)
        self.parts = int(parts)
        #do
        super(update, self).start_requests()
