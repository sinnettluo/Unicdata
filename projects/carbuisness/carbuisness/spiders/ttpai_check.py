# -*- coding: utf-8 -*-
"""
C2017-35
天天拍车辆检测详情

"""
import scrapy
from carbuisness.items import TtpaiCheckItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import hashlib
from hashlib import md5
import MySQLdb

website='ttpai_check_zb'

class CarSpider(scrapy.Spider):
    name=website
    start_urls=['http://www.ttpai.cn/quanguo/list']


    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=1000000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')

    def parse(self,response):
        mysqlconnection = MySQLdb.connect("192.168.1.94", "root", "Datauser@2017", 'people_zb', 3306)
        dbc = mysqlconnection.cursor()
        mysqlconnection.set_character_set('utf8')
        dbc.execute('SET NAMES utf8;')
        dbc.execute('SET CHARACTER SET utf8;')
        dbc.execute('SET character_set_connection=utf8;')

        sql = u"select * from ttpai_check_url"
        dbc.execute(sql)
        res = dbc.fetchall()

        for row in res:
            yield scrapy.Request(url=row[1], callback=self.parse_info)

        # print "do parse"
        # # http://www.ttpai.cn/quanguo/list
        # car_list = response.xpath('//div[@class="car-list-con"]//li[@class="item"]/a')
        # for car_info in car_list:
        #     carurl_temp = car_info.xpath('@href').extract_first()
        #     car_id = re.findall("/(\d+)", carurl_temp)[0]
        #     url = "http://pai.ttpai.cn/auctionDetail.html?auctionId=" + str(car_id)
        #     yield scrapy.Request(url,callback=self.parse_info)
        # next = response.xpath(u'//li[@class="page-number"]/a[contains(text(),"下一页")]')
        # if next:
        #     next_page = next.xpath('@href').extract_first()
        #     next_url = response.urljoin(next_page)
        #     yield scrapy.Request(next_url, callback=self.parse)



    def parse_info(self,response):
        # print "do parse_car"
        # http://pai.ttpai.cn/auctionDetail.html?auctionId=26073577
        item = TtpaiCheckItem()
        item['website'] = website
        item['url'] = response.url
        item['status'] = response.url
        item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())

        if response.xpath('//div[@class="scene-time"]/span[1]/text()'):
            item['changci'] = response.xpath('//div[@class="scene-time"]/span[1]/text()').extract_first()
        else:
            item['changci'] = "-"

        if response.xpath('//div[@class="car-title"]/h1/span/text()'):
            item['title'] = response.xpath('//div[@class="car-title"]/h1/span/text()').extract_first()  # 标题
        else:
            item['title'] = "-"

        if response.xpath('//ul[@class="distance clearfix"]/li[1]/span/text()'):
            item['license_plate_address'] = response.xpath('//ul[@class="distance clearfix"]/li[1]/span/text()').extract_first()  # 车牌地址
        else:
            item['license_plate_address'] = "-"

        if response.xpath('//ul[@class="distance clearfix"]/li[2]/span/text()'):
            item['mileage'] = response.xpath('//ul[@class="distance clearfix"]/li[2]/span/text()').extract_first()    # 行驶里程
        else:
            item['mileage'] = "-"

        if response.xpath('//ul[@class="distance clearfix"]/li[3]/span/text()'):
            item['license_plate_type'] = response.xpath('//ul[@class="distance clearfix"]/li[3]/span/text()').extract_first()   # 车牌类型(公牌或者私牌)
        else:
            item['license_plate_type'] = "-"

        if response.xpath('//ul[@class="distance clearfix"]/li[4]/span/text()'):
            item['guideprice'] = response.xpath('//ul[@class="distance clearfix"]/li[4]/span/text()').extract_first()   # 厂商指导价
        else:
            item['guideprice'] = "-"

        if response.xpath('//div[@class="right-car-info"]/div[@class="section-degree"]/i/text()'):
            item['comprehensive_rating'] = response.xpath('//div[@class="right-car-info"]/div[@class="section-degree"]/i/text()').extract_first() # 综合评级
        else:
            item['comprehensive_rating'] = "-"

        if response.xpath(u'//div[@class="right-car-info"]//div/span[contains(text(),"骨架")]/text()'):
            skeleton = response.xpath(u'//div[@class="right-car-info"]//div/span[contains(text(),"骨架")]/text()').extract_first()
            item['skeleton'] = re.findall(u"\d+", skeleton)[0].strip()  # 骨架
        else:
            item['skeleton'] = "-"

        if response.xpath(u'//div[@class="right-car-info"]//div/span[contains(text(),"装置")]/text()'):
            device = response.xpath(u'//div[@class="right-car-info"]//div/span[contains(text(),"装置")]/text()').extract_first()
            item['device'] = re.findall(u"\d+", device)[0].strip()     # 装置
        else:
            item['device'] = "-"

        if response.xpath(u'//div[@class="right-car-info"]//div/span[contains(text(),"外观")]/text()'):
            appearance = response.xpath(u'//div[@class="right-car-info"]//div/span[contains(text(),"外观")]/text()').extract_first()
            item['appearance'] = re.findall(u"\d+", appearance)[0].strip()    #外观
        else:
            item['appearance'] = "-"

        if response.xpath(u'//div[@class="right-car-info"]//div/span[contains(text(),"内饰")]/text()'):
            interior = response.xpath(u'//div[@class="right-car-info"]//div/span[contains(text(),"内饰")]/text()').extract_first()
            item['interior'] = re.findall(u"\d+", interior)[0].strip()   # 内饰
        else:
            item['interior'] = "-"

        if response.xpath(u'//div[@class="right-car-info"]//div[@class="section-info"]/p/text()'):
            item['concise_description'] = response.xpath(u'//div[@class="right-car-info"]//div[@class="section-info"]/p/text()').extract_first()   # 简述
        else:
            item['concise_description'] = "-"

        if response.xpath('//div[@class="right-car-info"]//div[@class="car-num"]/text()'):
            car_id = response.xpath('//div[@class="right-car-info"]//div[@class="car-num"]/text()').extract_first()
            item['car_id'] = re.findall("\d+", car_id)[0]   # 车源编号
        else:
            item['car_id'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"车身颜色")]/../td[2]/text()'):
            item['color'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"车身颜色")]/../td[2]/text()').extract_first()   # 车身颜色
        else:
            item['color'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"车牌")]/../td[2]/text()'):
            item['carno'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"车牌")]/../td[2]/text()').extract_first().replace("\n","").replace("\t","")   # 车牌
        else:
            item['carno'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"首次上牌时间")]/../td[2]/text()'):
            item['first_card'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"首次上牌时间")]/../td[2]/text()').extract_first().replace("\n","").replace("\t","")   #首次上牌时间
        else:
            item['first_card'] = "-"

        # 这个字段前面已经有了
        # if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"牌照性质")]/../td[2]/span/text()'):
        #     item[''] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"牌照性质")]/../td[2]/span/text()').extract_first()   #牌照性质
        # else:
        #     item[''] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"使用性质")]/../td[2]/span/text()'):
            item['use_properties'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"使用性质")]/../td[2]/span/text()').extract_first()   #使用性质
        else:
            item['use_properties'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"核定载人数")]/../td[2]/text()'):
            item['authorized_number_of_passengers'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"核定载人数")]/../td[2]/text()').extract_first()   #核定载人数
        else:
            item['authorized_number_of_passengers'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"过户次数")]/../td[2]/text()'):
            item['change_times'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"过户次数")]/../td[2]/text()').extract_first().strip().replace("\n","").replace("\t","")   #过户次数
        else:
            item['change_times'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"新车指导价")]/../td[2]/text()'):
            item['newcar_guideprice'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"新车指导价")]/../td[2]/text()').extract_first()   #新车指导价
        else:
            item['newcar_guideprice'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"特殊车辆")]/../td[2]/span/text()'):
            item['special_vehicle'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"特殊车辆")]/../td[2]/span/text()').extract_first()   #特殊车辆
        else:
            item['special_vehicle'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"年检有效期")]/../td[2]/text()'):
            item['yearchecktime'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"年检有效期")]/../td[2]/text()').extract_first().strip()   #年检有效期
        else:
            item['yearchecktime'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"发证日期")]/../td[2]/text()'):
            item['carddate'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"发证日期")]/../td[2]/text()').extract_first().strip()   #发证日期
        else:
            item['carddate'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"出厂日期")]/../td[2]/text()'):
            item['producedate'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"出厂日期")]/../td[2]/text()').extract_first().strip()   #出厂日期
        else:
            item['producedate'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"交强险")]/../td[2]/text()'):
            item['insurance1_date'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"交强险")]/../td[2]/text()').extract_first().strip().replace("\n","").replace("\t","")   #交强险
        else:
            item['insurance1_date'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"车身颜色变更")]/../td[2]/span/text()'):
            item['color_change'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"车身颜色变更")]/../td[2]/span/text()').extract_first()   #车身颜色变更
        else:
            item['color_change'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"外观颜色")]/../td[2]/text()'):
            item['appearance_color'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"外观颜色")]/../td[2]/text()').extract_first()   #外观颜色
        else:
            item['appearance_color'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"内饰颜色")]/../td[2]/text()'):
            item['interior_color'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"内饰颜色")]/../td[2]/text()').extract_first()   #内饰颜色
        else:
            item['interior_color'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"排量（L/T）")]/../td[2]/text()'):
            item['output'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"排量（L/T）")]/../td[2]/text()').extract_first()   #排量
        else:
            item['output'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"排挡")]/../td[2]/text()'):
            item['gear'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"排挡")]/../td[2]/text()').extract_first()   #排挡
        else:
            item['gear'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"燃料")]/../td[2]/text()'):
            item['fuel'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"燃料")]/../td[2]/text()').extract_first()   #燃料
        else:
            item['fuel'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"记忆座椅")]/../td[2]/text()'):
            item['memory_seat'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"记忆座椅")]/../td[2]/text()').extract_first()   #记忆座椅
        else:
            item['memory_seat'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"气囊")]/../td[2]/text()'):
            item['gasbag'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"气囊")]/../td[2]/text()').extract_first()   #气囊
        else:
            item['gasbag'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"ABS")]/../td[2]/text()'):
            item['ABS'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"ABS")]/../td[2]/text()').extract_first()  #ABS
        else:
            item['ABS'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"电动钥匙数量")]/../td[2]/text()'):
            item['electric_keys_num'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"电动钥匙数量")]/../td[2]/text()').extract_first().replace("\n","").replace("\t","")  #电动钥匙数量
        else:
            item['electric_keys_num'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"手动钥匙数量")]/../td[2]/text()'):
            item['manual_keys_num'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"手动钥匙数量")]/../td[2]/text()').extract_first().replace("\n","").replace("\t","")  #手动钥匙数量
        else:
            item['manual_keys_num'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"空调")]/../td[2]/text()'):
            item['air_conditioner'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"空调")]/../td[2]/text()').extract_first()  #空调
        else:
            item['air_conditioner'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"转向助力")]/../td[2]/text()'):
            item['steering_assist'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"转向助力")]/../td[2]/text()').extract_first()  #转向助力
        else:
            item['steering_assist'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"电动门窗")]/../td[2]/text()'):
            item['electric_door_and_window'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"电动门窗")]/../td[2]/text()').extract_first()  #电动门窗
        else:
            item['electric_door_and_window'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"天窗")]/../td[2]/text()'):
            item['skylight'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"天窗")]/../td[2]/text()').extract_first()  #天窗
        else:
            item['skylight'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//div[@class="clearfix"]/div[3]//table[@class="table-striped"]//tr/td[contains(text(),"座椅")]/../td[2]/text()'):
            item['chair'] = response.xpath(u'//div[@id="car-info-nav"]//div[@class="clearfix"]/div[3]//table[@class="table-striped"]//tr/td[contains(text(),"座椅")]/../td[2]/text()').extract_first()  # 座椅
        else:
            item['chair'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"铝合金轮毂")]/../td[2]/text()'):
            item['aluminum_alloy_wheel_hub'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"铝合金轮毂")]/../td[2]/text()').extract_first()  #铝合金轮毂
        else:
            item['aluminum_alloy_wheel_hub'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"巡航")]/../td[2]/text()'):
            item['cruise'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"巡航")]/../td[2]/text()').extract_first()  #巡航
        else:
            item['cruise'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"驱动方式")]/../td[2]/text()'):
            item['drive_mode'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"驱动方式")]/../td[2]/text()').extract_first()  #驱动方式
        else:
            item['drive_mode'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"导航")]/../td[2]/text()'):
            item['navigation'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"导航")]/../td[2]/text()').extract_first()  #导航
        else:
            item['navigation'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"雷达")]/../td[2]/text()'):
            item['radar'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"雷达")]/../td[2]/text()').extract_first()  #雷达
        else:
            item['radar'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"影音系统")]/../td[2]/text()'):
            item['film_system'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"影音系统")]/../td[2]/text()').extract_first()  #影音系统
        else:
            item['film_system'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"电动座椅")]/../td[2]/text()'):
            item['power_seat'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"电动座椅")]/../td[2]/text()').extract_first()  #电动座椅
        else:
            item['power_seat'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"电加热座椅")]/../td[2]/text()'):
            item['electric_heating_seat'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"电加热座椅")]/../td[2]/text()').extract_first()  #电加热座椅
        else:
            item['electric_heating_seat'] = "-"

        if response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"备胎")]/../td[2]/text()'):
            item['spare_tire'] = response.xpath(u'//div[@id="car-info-nav"]//table[@class="table-striped"]//tr/td[contains(text(),"备胎")]/../td[2]/text()').extract_first()  #备胎
        else:
            item['spare_tire'] = "-"

        if response.xpath(u'//div[@class="base-box pull-left"]/div[contains(text(),"其他原装装置")]/../div[2]/text()'):
            item['other_original_device'] = response.xpath(u'//div[@class="base-box pull-left"]/div[contains(text(),"其他原装装置")]/../div[2]/text()').extract_first()  # 其他原装装置
        else:
            item['other_original_device'] = "-"

        if response.xpath(u'//div[@class="base-box pull-right"]/div[contains(text(),"加装装置")]/../div[2]/text()'):
            item['mounting_device'] = response.xpath(u'//div[@class="base-box pull-right"]/div[contains(text(),"加装装置")]/../div[2]/text()').extract_first()  # 加装装置
        else:
            item['mounting_device'] = "-"


        #################################################################################################################
        #                   下面这四个字段是损伤情况                                                                    #
        #################################################################################################################

        skeleton_damage = dict()
        device_damage = dict()
        appearance_damage = dict()
        interior_damage = dict()

        skeleton_damage_list = response.xpath('//div[@class="car-bone-damage show-tips-box clearfix"]//tr/td[1]/..')
        score = response.xpath('//div[@id="car-bone-damage"]/h3/i')
        num = 0
        for _ in score:
            num += 1
        if num:
            skeleton_damage['检测师总体评分'] = str(num)         # 总体评分
        else:
            skeleton_damage['检测师总体评分'] = "-"
        for i in skeleton_damage_list:
            k = i.xpath('td[1]/text()').extract_first()#.strip().replace("\n","").replace("\t","")
            v = i.xpath('td[2]/text()').extract_first()#.strip().replace("\n","").replace("\t","")
            skeleton_damage[k] = v

        device_damage_list = response.xpath('//div[@class="car-set-damage show-tips-box"]//tr')
        score = response.xpath('//div[@id="car-set-damage"]/h3/i')
        num = 0
        for _ in score:
            num += 1
        if num:
            device_damage['检测师总体评分'] = str(num)
        else:
            device_damage['检测师总体评分'] = "-"
        for i in device_damage_list:
            k = i.xpath('td[1]/text()').extract_first()#.replace("\n","").replace("\t","")
            v = i.xpath('td[2]/text()').extract_first()#.replace("\n","").replace("\t","")
            device_damage[k] = v

        appearance_damage_list = response.xpath('//div[@class="car-outside-damage show-tips-box clearfix"]//tr/td[1]/..')
        score = response.xpath('//div[@id="car-outside-damage"]/h3/i')
        num = 0
        for _ in score:
            num += 1
        if num:
            appearance_damage['检测师总体评分'] = str(num)
        else:
            appearance_damage['检测师总体评分'] = "-"
        for i in appearance_damage_list:
            k = i.xpath('td[1]/text()').extract_first()#.replace("\n","").replace("\t","")
            v = i.xpath('td[2]/text()').extract_first()#.replace("\n","").replace("\t","")
            appearance_damage[k] = v

        interior_damage_list = response.xpath('//div[@class="car-inside-damage show-tips-box clearfix"]//tr/td[1]/..')
        score = response.xpath('//div[@id="car-inside-damage"]/h3/i')
        num = 0
        for _ in score:
            num += 1
        if num:
            interior_damage['检测师总体评分'] = str(num)
        else:
            interior_damage['检测师总体评分'] = "-"
        for i in interior_damage_list:
            k = i.xpath('td[1]/text()').extract_first()#.replace("\n","").replace("\t","")
            v = i.xpath('td[2]/text()').extract_first()#.replace("\n","").replace("\t","")
            interior_damage[k] = v

        damage = {"skeleton_damage":skeleton_damage, "device_damage":device_damage, "appearance_damage":appearance_damage, "interior_damage":interior_damage}
        item['damage'] = damage
        ########################################################################################################################################3

        yield item



