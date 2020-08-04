# -*- coding: utf-8 -*-
"""
C2017-31

"""

import scrapy
from carbuisness.items import YouxinpaiPicItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import random
import re
import pymongo
import urllib2
from selenium import webdriver
import urllib
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

website = 'youxinpai_pic'

class CarSpider(scrapy.Spider):

    name = website
    custom_settings = {
        'DOWNLOAD_TIMEOUT': '300',
    }
    def __init__(self, **kwargs):
        super(CarSpider, self).__init__(**kwargs)
        self.mailer = MailSender.from_settings(settings)
        self.counts = 0
        self.carnum = 3000000
        # Mongo
        settings.set('CrawlCar_Num', self.carnum, priority='cmdline')
        settings.set('MONGODB_DB', 'carbusiness', priority='cmdline')
        settings.set('MONGODB_COLLECTION', website, priority='cmdline')

    def start_requests(self):
        # for id in range(31450, 1862000):          # 优信拍数据库可能会增加，以后维护的时候要检查这里的上限是否扩大
        # for id in range(51070, 1862000):          # 程序从51070结束运行，因为没有图片可以下载。从110001开始继续运行
        # for id in range(110001, 1862000):         # 第一个可以下载图片的点
        for id in range(574099 , 1862000):
            url = "http://i.youxinpai.com/auctionhall/Detailforop.aspx?id=" + str(id)
            #url = "http://i.youxinpai.com/auctionhall/Detailforop.aspx?id=1219997"
            #url = "http://i.youxinpai.com/auctionhall/Detailforop.aspx?id=123420"
            #url = "http://i.youxinpai.com/auctionhall/Detailforop.aspx?id=1024"
            #url = "http://i.youxinpai.com/auctionhall/Detailforop.aspx?id=31545"
            yield scrapy.Request(url, callback=self.parse)

    def openbrowser(self, url):
        """
        url是需要访问的url
        返回渲染后的html源码
        """
        driver = webdriver.PhantomJS(r"D:\phantomjs.exe")
        driver.set_page_load_timeout(60)

        try:
            driver.get(url)
        except Exception as e:
            print(e)
        time.sleep(2)
        html = driver.page_source
        driver.close()
        return html

    def parse(self, response):
        print "do parse"
        #print response.url
        item = YouxinpaiPicItem()
        html = self.openbrowser(response.url)
        html_xpath = scrapy.Selector(text=html)

        h1_base = html_xpath.xpath('//h1/text()').extract_first()
        h1_list = h1_base.strip().split(" ")
        flag = ""
        try:
            flag_test = h1_list[5]  # 仅仅为了测试是否标题有六个字段
            flag = h1_list[4]
        except:
            print "abnormal of the title" + response.url
        if flag:        #页面存在有价值信息
            item['city'] = re.findall(u"【(.*?)】", h1_list[0])[0]
            item['brandname'] = h1_list[1]
            item['familyname'] = h1_list[2]

            ###########################      页面信息提取，示例页面 http://i.youxinpai.com/auctionhall/Detailforop.aspx?id=123420       #############################################################################################################################################################################################################
            if html_xpath.xpath('//div[@class="newcar_content"]'):
                if html_xpath.xpath('//div[@class="car-abstract"]/div[@class="con"]/p/text()'):
                    vehicle_summary = ""
                    vehicle_summary_list = html_xpath.xpath('//div[@class="car-abstract"]/div[@class="con"]//text()').extract()
                    for x in vehicle_summary_list:
                        vehicle_summary += x.strip()
                    item['vehicle_summary'] = vehicle_summary

                if html_xpath.xpath('//div[@class="car-abstract"]/div/div[@class="degree-ico"]/text()'):
                    item['vehicle_level'] = html_xpath.xpath('//div[@class="car-abstract"]/div/div[@class="degree-ico"]/text()').extract_first().strip()

                if html_xpath.xpath(u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"车辆信息")]/../following-sibling::td[1]/span/text()'):
                    item['essential_information'] = html_xpath.xpath(u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"车辆信息")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"表显里程")]/../following-sibling::td[1]/span/text()'):
                    item['apparent_mileage'] = html_xpath.xpath(u'//table[@class="mb20"]/tbody/tr/th/span[contains(text(),"表显里程")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"车辆库存地")]/../following-sibling::td[1]/span/text()'):
                    item['city'] = html_xpath.xpath(u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"车辆库存地")]/../following-sibling::td[1]/span/text()').extract_first().strip()


                if html_xpath.xpath(u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"车辆出厂日期")]/../following-sibling::td[1]/span/text()'):
                    item['date_of_production'] = html_xpath.xpath(u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"车辆出厂日期")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"车辆注册日期")]/../following-sibling::td[1]/span/text()'):
                    item['registration_date'] = html_xpath.xpath(u'//table[@class="mb20"]/tbody/tr//th/span[contains(text(),"车辆注册日期")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"使用性质")]/../following-sibling::td[1]/span/text()'):
                    item['use_properties'] = html_xpath.xpath(u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"使用性质")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"车辆所有人性质")]/../following-sibling::td[1]/span/text()'):
                    item['owner_nature'] = html_xpath.xpath(u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"车辆所有人性质")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"新车质保")]/../following-sibling::td[1]/span/text()'):
                    item['new_car_warranty'] = html_xpath.xpath(u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"新车质保")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"年审有效期")]/../following-sibling::td[1]/span/text()'):
                    item['validity_period_of_examination'] = html_xpath.xpath(u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"年审有效期")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"商业险")]/../following-sibling::td[1]/span/text()'):
                    item['commercial_insurance'] = html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"商业险")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"交强险到期日")]/../following-sibling::td[1]/span/text()'):
                    item['compulsory_insurance'] = html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"交强险到期日")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"是否一手车")]/../following-sibling::td[1]/span/text()'):
                    item['is_one'] = html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"是否一手车")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"保养手册记录")]/../following-sibling::td[1]/span/text()'):
                    item['maintenance_record'] = html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"保养手册记录")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"车船税到期日")]/../following-sibling::td[1]/span/text()'):
                    item['vehicle_and_vessel_tax'] = html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"车船税到期日")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"车辆标准配置")]/../following-sibling::td[1]/span/text()'):
                    item['standard_configuration'] = html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"车辆标准配置")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"车主个性化配置")]/../following-sibling::td[1]/span/text()'):
                    item['personalized_configuration'] = html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"车主个性化配置")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"燃油类型")]/../following-sibling::td[1]/span/text()'):
                    item['fuel_type'] = html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"燃油类型")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"发动机号")]/../following-sibling::td[1]/span/text()'):
                    item['engine_number'] = html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"发动机号")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"车辆VIN码")]/../following-sibling::td[1]/span/text()'):
                    item['VIN_num'] = html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"车辆VIN码")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"车牌号码")]/../following-sibling::td[1]/span/text()'):
                    item['license_plate'] = html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"车牌号码")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"车辆原色")]/../following-sibling::td[1]/span/text()'):
                    item['color'] = html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"车辆原色")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"车辆是否改装")]/../following-sibling::td[1]/span/text()'):
                    item['is_refit'] = html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"车辆是否改装")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"登记证")]/../following-sibling::td[1]/span/text()'):
                    item['registration'] = html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"登记证")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"行驶本")]/../following-sibling::td[1]/span/text()'):
                    item['driving_book'] = html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"行驶本")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"原始购车发票")]/../following-sibling::td[1]/span/text()'):
                    item['invoice'] = html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"原始购车发票")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"购置税")]/../following-sibling::td[1]/span/text()'):
                    item['purchase_tax'] = html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"购置税")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"车钥匙")]/../following-sibling::td[1]/span/text()'):
                    item['key'] = html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"车钥匙")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"说明书")]/../following-sibling::td[1]/span/text()'):
                    item['instructions'] = html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"说明书")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"补充说明")]/../following-sibling::td[1]/span/text()'):
                    item['supplementary_notes'] = html_xpath.xpath(
                        u'//table[@class="mb20"]/tbody//tr/th/span[contains(text(),"补充说明")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"起动机/转向系统")]/../following-sibling::td[1]/span/text()'):
                    item['starter_steering'] = html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"起动机/转向系统")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"车身灯具")]/../following-sibling::td[1]/span/text()'):
                    item['body_lamp'] = html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"车身灯具")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"发动机")]/../following-sibling::td[1]/span/text()'):
                    item['engine'] = html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"发动机")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"工具状态")]/../following-sibling::td[1]/span/text()'):
                    item['tool_state'] = html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"工具状态")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"变速器")]/../following-sibling::td[1]/span/text()'):
                    item['transmission'] = html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"变速器")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"备胎状态")]/../following-sibling::td[1]/span/text()'):
                    item['spare_wheel_status'] = html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"备胎状态")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"避震器")]/../following-sibling::td[1]/span/text()'):
                    item['shock_absorber'] = html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"避震器")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"门手")]/../following-sibling::td[1]/span/text()'):
                    item['door_handle'] = html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"门手")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"底盘/行驶")]/../following-sibling::td[1]/span/text()'):
                    item['chassis'] = html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"底盘/行驶")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"车钥匙")]/../following-sibling::td[1]/span/text()'):
                    item['car_keys'] = html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"车钥匙")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"制动器")]/../following-sibling::td[1]/span/text()'):
                    item['brake'] = html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"制动器")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"排气系统")]/../following-sibling::td[1]/span/text()'):
                    item['exhaust_system'] = html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"排气系统")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"电器系统")]/../following-sibling::td[1]/span/text()'):
                    item['electrical_system'] = html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"电器系统")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                if html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"车辆补充说明")]/../following-sibling::td[1]/span/text()'):
                    item['supplement'] = html_xpath.xpath(
                        u'//div[@class="newcar_content"]/table[3]/tbody//tr/th/span[contains(text(),"车辆补充说明")]/../following-sibling::td[1]/span/text()').extract_first().strip()

                #图片下载，下载最右边的图片的最后一张，包含较多有用信息
                status = response.url   # 暂留，后面有用
                if html_xpath.xpath('//div[@id="divPicList"]//ul//li/a/@rel'):
                    print("yes"  + "$$$$$$$$$$$$$$$$$$$$$$$$")
                    right_pic_list = html_xpath.xpath('//div[@id="divPicList"]//ul//li/a/@rel').extract()
                    print(str(right_pic_list) + "$$$$$$$$$$$$$$$$$$$$$$$$")
                    pic_test = ""
                    try:
                        pic_test = right_pic_list[len(right_pic_list)-1]
                    except:
                        pic_test = ""

                    if pic_test:
                        right_pic = re.findall(u"smallimage: \'(.*?)\'", right_pic_list[-1])[0]
                        print(right_pic + "$$$$$$$$$$$$$$$$$$$$$$$$")

                        id = re.findall("id=(\d+)", response.url)[0]
                        status_base = right_pic.split("/")
                        status = status_base[-1]
                        picname = flag

                        file_name_base = id + picname + status
                        file_name = file_name_base.replace("/", "-")
                        file_path = os.path.join(r"D:\BaiduNetdiskDownload\null\youxinpai_images", file_name)
                        print(file_path + "$$$$$$$$$$$$$$$$$$$$$$$$")
                        urllib.urlretrieve(right_pic, file_path)

                item['url'] = response.url
                item['website'] = website
                item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
                item['status'] = status

            ###########################      基本信息提取完毕       #############################################################################################################################################################################################################

            ###########################      第二种页面信息提取，示例页面 http://i.youxinpai.com/auctionhall/Detailforop.aspx?id=1219997       #############################################################################################################################################################################################################
            elif html_xpath.xpath('//table[@class="tinfo"]'):
                if html_xpath.xpath(u'//tbody//td[contains(text(),"基本信息：")]/label/text()'):
                    item['essential_information'] = html_xpath.xpath(u'//tbody//td[contains(text(),"基本信息：")]/label/text()').extract_first()

                if html_xpath.xpath(u'//tbody//td[contains(text(),"证件手续：")]/label/text()'):
                    item['document_formalities'] = html_xpath.xpath(u'//tbody//td[contains(text(),"证件手续：")]/label/text()').extract_first()

                if html_xpath.xpath(u'//tbody//td[contains(text(),"车牌号：")]/label/text()'):
                    item['license_plate_number'] = html_xpath.xpath(u'//tbody//td[contains(text(),"车牌号：")]/label/text()').extract_first()

                if html_xpath.xpath(u'//tbody//td[contains(text(),"违章说明：")]/label/text()'):
                    item['description_violation'] = html_xpath.xpath(u'//tbody//td[contains(text(),"违章说明：")]/label/text()').extract_first()

                if html_xpath.xpath(u'//tbody//td[contains(text(),"漆面说明：")]/label/text()'):
                    item['paint_description'] = html_xpath.xpath(u'//tbody//td[contains(text(),"漆面说明：")]/label/text()').extract_first()

                if html_xpath.xpath(u'//tbody//td[contains(text(),"其他配置：")]/label/text()'):
                    item['other_requipment'] = html_xpath.xpath(u'//tbody//td[contains(text(),"其他配置：")]/label/text()').extract_first()

                if html_xpath.xpath(u'//tbody//td[contains(text(),"补充说明：")]/label/text()'):
                    item['complement'] = html_xpath.xpath(u'//tbody//td[contains(text(),"补充说明：")]/label/text()').extract_first()

                if html_xpath.xpath(u'//td[contains(text(),"机油检查")]/following-sibling::td[1]/label/text()'):
                    item['lubricant_check'] = html_xpath.xpath(u'//td[contains(text(),"机油检查")]/following-sibling::td[1]/label/text()').extract_first()

                if html_xpath.xpath(u'//td[contains(text(),"排烟检查")]/following-sibling::td[1]/label/text()'):
                    item['smoke_check'] = html_xpath.xpath(u'//td[contains(text(),"排烟检查")]/following-sibling::td[1]/label/text()').extract_first()

                if html_xpath.xpath(u'//td[contains(text(),"防冻液检查")]/following-sibling::td[1]/label/text()'):
                    item['antifreeze_check'] = html_xpath.xpath(u'//td[contains(text(),"防冻液检查")]/following-sibling::td[1]/label/text()').extract_first()

                if html_xpath.xpath(u'//td[contains(text(),"运转检查")]/following-sibling::td[1]/label/text()'):
                    item['run_check'] = html_xpath.xpath(u'//td[contains(text(),"运转检查")]/following-sibling::td[1]/label/text()').extract_first()

                if html_xpath.xpath(u'//td[contains(text(),"刹车油检查")]/following-sibling::td[1]/label/text()'):
                    item['brake_check'] = html_xpath.xpath(u'//td[contains(text(),"刹车油检查")]/following-sibling::td[1]/label/text()').extract_first()

                if html_xpath.xpath(u'//td[contains(text(),"发动机检查")]/following-sibling::td[1]/label/text()'):
                    item['engine_check'] = html_xpath.xpath(u'//td[contains(text(),"发动机检查")]/following-sibling::td[1]/label/text()').extract_first()

                if html_xpath.xpath(u'//td[contains(text(),"助力油检查")]/following-sibling::td[1]/label/text()'):
                    item['booster_oil'] = html_xpath.xpath(u'//td[contains(text(),"助力油检查")]/following-sibling::td[1]/label/text()').extract_first()

                if html_xpath.xpath(u'//td[contains(text(),"改装说明")]/following-sibling::td[1]/label/text()'):
                    item['refit_check'] = html_xpath.xpath(u'//td[contains(text(),"改装说明")]/following-sibling::td[1]/label/text()').extract_first()

                if html_xpath.xpath(u'//td[contains(text(),"电池检查")]/following-sibling::td[1]/label/text()'):
                    item['battery_check'] = html_xpath.xpath(u'//td[contains(text(),"电池检查")]/following-sibling::td[1]/label/text()').extract_first()

                if html_xpath.xpath(u'//td[contains(text(),"内控电器")]/following-sibling::td[1]/label/text()'):
                    item['internally_piloting'] = html_xpath.xpath(u'//td[contains(text(),"内控电器")]/following-sibling::td[1]/label/text()').extract_first()

                if html_xpath.xpath(u'//td[contains(text(),"皮带检查")]/following-sibling::td[1]/label/text()'):
                    item['belt_check'] = html_xpath.xpath(u'//td[contains(text(),"皮带检查")]/following-sibling::td[1]/label/text()').extract_first()

                if html_xpath.xpath(u'//td[contains(text(),"备胎")]/following-sibling::td[1]/label/text()'):
                    item['spare_tire'] = html_xpath.xpath(u'//td[contains(text(),"备胎")]/following-sibling::td[1]/label/text()').extract_first()

                if html_xpath.xpath(u'//td[contains(text(),"启动机检查")]/following-sibling::td[1]/label/text()'):
                    item['start_machine_check'] = html_xpath.xpath(u'//td[contains(text(),"启动机检查")]/following-sibling::td[1]/label/text()').extract_first()

                if html_xpath.xpath(u'//td[contains(text(),"工具")]/following-sibling::td[1]/label/text()'):
                    item['requipment'] = html_xpath.xpath(u'//td[contains(text(),"工具")]/following-sibling::td[1]/label/text()').extract_first()

                if html_xpath.xpath(u'//td[contains(text(),"车钥匙")]/following-sibling::td[1]/label/text()'):
                    item['carkey'] = html_xpath.xpath(u'//td[contains(text(),"车钥匙")]/following-sibling::td[1]/label/text()').extract_first()

                if html_xpath.xpath(u'//td[contains(text(),"变速箱检查")]/following-sibling::td[1]/label/text()'):
                    item['gearcheck'] = html_xpath.xpath(u'//td[contains(text(),"变速箱检查")]/following-sibling::td[1]/label/text()').extract_first()

                if html_xpath.xpath(u'//td[contains(text(),"转向助力检查")]/following-sibling::td[1]/label/text()'):
                    item['rotate_booster_check'] = html_xpath.xpath(u'//td[contains(text(),"转向助力检查")]/following-sibling::td[1]/label/text()').extract_first()

                if html_xpath.xpath(u'//span[@class="fl"]/text()'):
                    item['apparent_mileage'] = html_xpath.xpath(u'//span[@class="fl"]/text()').extract_first()

                status = response.url
                if html_xpath.xpath('//div[@id="ProceduresDetails"]/div[contains(@class,pic)]/p/..'):   #   页面下面的十来张图片
                    piclist = html_xpath.xpath('//div[@id="ProceduresDetails"]/div[contains(@class,pic)]/p/..')
                    for pic in piclist:
                        picname = pic.xpath('p/text()').extract_first()
                        picurl = pic.xpath('a/img/@src').extract_first()
                        id = re.findall("id=(\d+)", response.url)[0]
                        status_base = picurl.split("/")
                        status = status_base[-1]
                        file_name_base = id + picname + status
                        file_name = file_name_base.replace("/", "-")
                        file_path = os.path.join(r"D:\BaiduNetdiskDownload\null\youxinpai_images", file_name)
                        urllib.urlretrieve(picurl, file_path)

                if html_xpath.xpath('//div[@id="divPicList"]//ul//li/a/@rel'):  # 页面右边图片的最后一张
                    right_pic_list = html_xpath.xpath('//div[@id="divPicList"]//ul//li/a/@rel').extract()
                    pic_test = ""
                    try:
                        pic_test = right_pic_list[7]
                    except:
                        pic_test = ""
                    if pic_test:
                        right_pic = re.findall(u"smallimage: \'(.*?)\'", right_pic_list[-1])[0]
                        id = re.findall("id=(\d+)", response.url)[0]
                        status_base = right_pic.split("/")
                        status_right = status_base[-1]
                        picname = flag

                        file_name_right_base = id + picname + status_right
                        file_name_right = file_name_right_base.replace("/", "-")
                        file_path_right = os.path.join(r"D:\BaiduNetdiskDownload\null\youxinpai_images", file_name_right)
                        urllib.urlretrieve(right_pic, file_path_right)

                item['url'] = response.url
                item['website'] = website
                item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
                item['status'] = status
            ###########################      第二种页面基本信息提取完毕       #############################################################################################################################################################################################################

            # 打印id，用于程序中断续跑
            try:
                id = str(re.findall("\d+", response.url)[0])
                print "******  " + id + "  ******"
            except:
                pass

            yield item

