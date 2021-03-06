# -*- coding: utf-8 -*-
"""

C2017-39


"""
import scrapy
from carbuisness.items import AutohomeLocalDealerPriceItem
import time
from scrapy.conf import settings
from scrapy.mail import MailSender
import logging
import json
import re
import random
import hashlib
from hashlib import md5
from carbuisness.getip import getProxy
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy.conf import settings
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


website='autohome_local_dealer_price'

class CarSpider(scrapy.Spider):

    name=website
    custom_settings = {
        "DOWNLOAD_DELAY":0.1
    }
    city_str = {
        "CityItems": [{"I": 110100, "N": "北京", "P": "Beijing", "S": 110000},
                      {"I": 120100, "N": "天津", "P": "Tianjin", "S": 120000},
                      {"I": 130100, "N": "石家庄", "P": "Shijiazhuang", "S": 130000},
                      {"I": 130200, "N": "唐山", "P": "Tangshan", "S": 130000},
                      {"I": 130300, "N": "秦皇岛", "P": "Qinhuangdao", "S": 130000},
                      {"I": 130400, "N": "邯郸", "P": "Handan", "S": 130000},
                      {"I": 130500, "N": "邢台", "P": "Xingtai", "S": 130000},
                      {"I": 130600, "N": "保定", "P": "Baoding", "S": 130000},
                      {"I": 130700, "N": "张家口", "P": "Zhangjiakou", "S": 130000},
                      {"I": 130800, "N": "承德", "P": "Chengde", "S": 130000},
                      {"I": 130900, "N": "沧州", "P": "Cangzhou", "S": 130000},
                      {"I": 131000, "N": "廊坊", "P": "Langfang", "S": 130000},
                      {"I": 131100, "N": "衡水", "P": "Hengshui", "S": 130000},
                      {"I": 139900, "N": "其它", "P": "Qita", "S": 130000},
                      {"I": 140100, "N": "太原", "P": "Taiyuan", "S": 140000},
                      {"I": 140200, "N": "大同", "P": "Datong", "S": 140000},
                      {"I": 140300, "N": "阳泉", "P": "Yangquan", "S": 140000},
                      {"I": 140400, "N": "长治", "P": "Changzhi", "S": 140000},
                      {"I": 140500, "N": "晋城", "P": "Jincheng", "S": 140000},
                      {"I": 140600, "N": "朔州", "P": "Shuozhou", "S": 140000},
                      {"I": 140700, "N": "晋中", "P": "Jinzhong", "S": 140000},
                      {"I": 140800, "N": "运城", "P": "Yuncheng", "S": 140000},
                      {"I": 140900, "N": "忻州", "P": "Xinzhou", "S": 140000},
                      {"I": 141000, "N": "临汾", "P": "Linfen", "S": 140000},
                      {"I": 141100, "N": "吕梁", "P": "Lvliang", "S": 140000},
                      {"I": 149900, "N": "其它", "P": "Qita", "S": 140000},
                      {"I": 150100, "N": "呼和浩特", "P": "Hohhot", "S": 150000},
                      {"I": 150200, "N": "包头", "P": "Baotou", "S": 150000},
                      {"I": 150300, "N": "乌海", "P": "Wuhai", "S": 150000},
                      {"I": 150400, "N": "赤峰", "P": "Chifeng", "S": 150000},
                      {"I": 150500, "N": "通辽", "P": "Tongliao", "S": 150000},
                      {"I": 150600, "N": "鄂尔多斯", "P": "Ordos", "S": 150000},
                      {"I": 150700, "N": "呼伦贝尔", "P": "Hulunber", "S": 150000},
                      {"I": 150800, "N": "巴彦淖尔", "P": "Bayan Nur", "S": 150000},
                      {"I": 150900, "N": "乌兰察布", "P": "Ulanqab", "S": 150000},
                      {"I": 152200, "N": "兴安盟", "P": "Hinggan", "S": 150000},
                      {"I": 152500, "N": "锡林郭勒盟", "P": "Xilin Gol", "S": 150000},
                      {"I": 152900, "N": "阿拉善盟", "P": "Alxa", "S": 150000},
                      {"I": 159900, "N": "其它", "P": "Qita", "S": 150000},
                      {"I": 210100, "N": "沈阳", "P": "Shenyang", "S": 210000},
                      {"I": 210200, "N": "大连", "P": "Dalian", "S": 210000},
                      {"I": 210300, "N": "鞍山", "P": "Anshan", "S": 210000},
                      {"I": 210400, "N": "抚顺", "P": "Fushun", "S": 210000},
                      {"I": 210500, "N": "本溪", "P": "Benxi", "S": 210000},
                      {"I": 210600, "N": "丹东", "P": "Dandong", "S": 210000},
                      {"I": 210700, "N": "锦州", "P": "Jinzhou", "S": 210000},
                      {"I": 210800, "N": "营口", "P": "Yingkou", "S": 210000},
                      {"I": 210900, "N": "阜新", "P": "Fuxin", "S": 210000},
                      {"I": 211000, "N": "辽阳", "P": "Liaoyang", "S": 210000},
                      {"I": 211100, "N": "盘锦", "P": "Panjin", "S": 210000},
                      {"I": 211200, "N": "铁岭", "P": "Tieling", "S": 210000},
                      {"I": 211300, "N": "朝阳", "P": "Chaoyang", "S": 210000},
                      {"I": 211400, "N": "葫芦岛", "P": "Huludao", "S": 210000},
                      {"I": 219900, "N": "其它", "P": "Qita", "S": 210000},
                      {"I": 220100, "N": "长春", "P": "Changchun", "S": 220000},
                      {"I": 220200, "N": "吉林", "P": "Jilin", "S": 220000},
                      {"I": 220300, "N": "四平", "P": "Siping", "S": 220000},
                      {"I": 220400, "N": "辽源", "P": "Liaoyuan", "S": 220000},
                      {"I": 220500, "N": "通化", "P": "Tonghua", "S": 220000},
                      {"I": 220600, "N": "白山", "P": "Baishan", "S": 220000},
                      {"I": 220700, "N": "松原", "P": "Songyuan", "S": 220000},
                      {"I": 220800, "N": "白城", "P": "Baicheng", "S": 220000},
                      {"I": 222400, "N": "延边", "P": "Yanbian", "S": 220000},
                      {"I": 229900, "N": "其它", "P": "Qita", "S": 220000},
                      {"I": 230100, "N": "哈尔滨", "P": "Harbin", "S": 230000},
                      {"I": 230200, "N": "齐齐哈尔", "P": "Qiqihar", "S": 230000},
                      {"I": 230300, "N": "鸡西", "P": "Jixi", "S": 230000},
                      {"I": 230400, "N": "鹤岗", "P": "Hegang", "S": 230000},
                      {"I": 230500, "N": "双鸭山", "P": "Shuangyashan", "S": 230000},
                      {"I": 230600, "N": "大庆", "P": "Daqing", "S": 230000},
                      {"I": 230700, "N": "伊春", "P": "Yichun", "S": 230000},
                      {"I": 230800, "N": "佳木斯", "P": "Jiamusi", "S": 230000},
                      {"I": 230900, "N": "七台河", "P": "Qitaihe", "S": 230000},
                      {"I": 231000, "N": "牡丹江", "P": "Mudanjiang", "S": 230000},
                      {"I": 231100, "N": "黑河", "P": "Heihe", "S": 230000},
                      {"I": 231200, "N": "绥化", "P": "Suihua", "S": 230000},
                      {"I": 232700, "N": "大兴安岭", "P": "DaXingAnLing", "S": 230000},
                      {"I": 239900, "N": "其它", "P": "Qita", "S": 230000},
                      {"I": 310100, "N": "上海", "P": "Shanghai", "S": 310000},
                      {"I": 320100, "N": "南京", "P": "Nanjing", "S": 320000},
                      {"I": 320200, "N": "无锡", "P": "Wuxi", "S": 320000},
                      {"I": 320300, "N": "徐州", "P": "Xuzhou", "S": 320000},
                      {"I": 320400, "N": "常州", "P": "Changzhou", "S": 320000},
                      {"I": 320500, "N": "苏州", "P": "Suzhou", "S": 320000},
                      {"I": 320600, "N": "南通", "P": "Nantong", "S": 320000},
                      {"I": 320700, "N": "连云港", "P": "Lianyungang", "S": 320000},
                      {"I": 320800, "N": "淮安", "P": "Huai\'an", "S": 320000},
                      {"I": 320900, "N": "盐城", "P": "Yancheng", "S": 320000},
                      {"I": 321000, "N": "扬州", "P": "Yangzhou", "S": 320000},
                      {"I": 321100, "N": "镇江", "P": "Zhenjiang", "S": 320000},
                      {"I": 321200, "N": "泰州", "P": "Taizhou", "S": 320000},
                      {"I": 321300, "N": "宿迁", "P": "Suqian", "S": 320000},
                      {"I": 329900, "N": "其它", "P": "Qita", "S": 320000},
                      {"I": 330100, "N": "杭州", "P": "Hangzhou", "S": 330000},
                      {"I": 330200, "N": "宁波", "P": "Ningbo", "S": 330000},
                      {"I": 330300, "N": "温州", "P": "Wenzhou", "S": 330000},
                      {"I": 330400, "N": "嘉兴", "P": "Jiaxing", "S": 330000},
                      {"I": 330500, "N": "湖州", "P": "Huzhou", "S": 330000},
                      {"I": 330600, "N": "绍兴", "P": "Shaoxing", "S": 330000},
                      {"I": 330700, "N": "金华", "P": "Jinhua", "S": 330000},
                      {"I": 330800, "N": "衢州", "P": "Quzhou", "S": 330000},
                      {"I": 330900, "N": "舟山", "P": "Zhoushan", "S": 330000},
                      {"I": 331000, "N": "台州", "P": "Taizhou", "S": 330000},
                      {"I": 331100, "N": "丽水", "P": "Lishui", "S": 330000},
                      {"I": 339900, "N": "其它", "P": "Qita", "S": 330000},
                      {"I": 340100, "N": "合肥", "P": "Hefei", "S": 340000},
                      {"I": 340200, "N": "芜湖", "P": "Wuhu", "S": 340000},
                      {"I": 340300, "N": "蚌埠", "P": "Bengbu", "S": 340000},
                      {"I": 340400, "N": "淮南", "P": "Huainan", "S": 340000},
                      {"I": 340500, "N": "马鞍山", "P": "Ma'anshan", "S": 340000},
                      {"I": 340600, "N": "淮北", "P": "Huaibei", "S": 340000},
                      {"I": 340700, "N": "铜陵", "P": "Tongling", "S": 340000},
                      {"I": 340800, "N": "安庆", "P": "Anqing", "S": 340000},
                      {"I": 341000, "N": "黄山", "P": "Huangshan", "S": 340000},
                      {"I": 341100, "N": "滁州", "P": "Chuzhou", "S": 340000},
                      {"I": 341200, "N": "阜阳", "P": "Fuyang", "S": 340000},
                      {"I": 341300, "N": "宿州", "P": "Suzhou", "S": 340000},
                      {"I": 341500, "N": "六安", "P": "Lu'an", "S": 340000},
                      {"I": 341600, "N": "亳州", "P": "Bozhou", "S": 340000},
                      {"I": 341700, "N": "池州", "P": "Chizhou", "S": 340000},
                      {"I": 341800, "N": "宣城", "P": "Xuancheng", "S": 340000},
                      {"I": 349900, "N": "其它", "P": "Qita", "S": 340000},
                      {"I": 350100, "N": "福州", "P": "Fuzhou", "S": 350000},
                      {"I": 350200, "N": "厦门", "P": "Xiamen", "S": 350000},
                      {"I": 350300, "N": "莆田", "P": "Putian", "S": 350000},
                      {"I": 350400, "N": "三明", "P": "Sanming", "S": 350000},
                      {"I": 350500, "N": "泉州", "P": "Quanzhou", "S": 350000},
                      {"I": 350600, "N": "漳州", "P": "Zhangzhou", "S": 350000},
                      {"I": 350700, "N": "南平", "P": "Nanping", "S": 350000},
                      {"I": 350800, "N": "龙岩", "P": "Longyan", "S": 350000},
                      {"I": 350900, "N": "宁德", "P": "Ningde", "S": 350000},
                      {"I": 359900, "N": "其它", "P": "Qita", "S": 350000},
                      {"I": 360100, "N": "南昌", "P": "Nanchang", "S": 360000},
                      {"I": 360200, "N": "景德镇", "P": "Jingdezhen", "S": 360000},
                      {"I": 360300, "N": "萍乡", "P": "Pingxiang", "S": 360000},
                      {"I": 360400, "N": "九江", "P": "Jiujiang", "S": 360000},
                      {"I": 360500, "N": "新余", "P": "Xinyu", "S": 360000},
                      {"I": 360600, "N": "鹰潭", "P": "Yingtan", "S": 360000},
                      {"I": 360700, "N": "赣州", "P": "Ganzhou", "S": 360000},
                      {"I": 360800, "N": "吉安", "P": "Ji\'an", "S": 360000},
                      {"I": 360900, "N": "宜春", "P": "Yichun", "S": 360000},
                      {"I": 361000, "N": "抚州", "P": "Fuzhou", "S": 360000},
                      {"I": 361100, "N": "上饶", "P": "Shangrao", "S": 360000},
                      {"I": 369900, "N": "其它", "P": "Qita", "S": 360000},
                      {"I": 370100, "N": "济南", "P": "Jinan", "S": 370000},
                      {"I": 370200, "N": "青岛", "P": "Qingdao", "S": 370000},
                      {"I": 370300, "N": "淄博", "P": "Zibo", "S": 370000},
                      {"I": 370400, "N": "枣庄", "P": "Zaozhuang", "S": 370000},
                      {"I": 370500, "N": "东营", "P": "Dongying", "S": 370000},
                      {"I": 370600, "N": "烟台", "P": "Yantai", "S": 370000},
                      {"I": 370700, "N": "潍坊", "P": "Weifang", "S": 370000},
                      {"I": 370800, "N": "济宁", "P": "Jining", "S": 370000},
                      {"I": 370900, "N": "泰安", "P": "Tai\'an", "S": 370000},
                      {"I": 371000, "N": "威海", "P": "Weihai", "S": 370000},
                      {"I": 371100, "N": "日照", "P": "Rizhao", "S": 370000},
                      {"I": 371200, "N": "莱芜", "P": "Laiwu", "S": 370000},
                      {"I": 371300, "N": "临沂", "P": "Linyi", "S": 370000},
                      {"I": 371400, "N": "德州", "P": "Dezhou", "S": 370000},
                      {"I": 371500, "N": "聊城", "P": "Liaocheng", "S": 370000},
                      {"I": 371600, "N": "滨州", "P": "Binzhou", "S": 370000},
                      {"I": 371700, "N": "菏泽", "P": "Heze", "S": 370000},
                      {"I": 379900, "N": "其它", "P": "Qita", "S": 370000},
                      {"I": 410100, "N": "郑州", "P": "Zhengzhou", "S": 410000},
                      {"I": 410200, "N": "开封", "P": "Kaifeng", "S": 410000},
                      {"I": 410300, "N": "洛阳", "P": "Luoyang", "S": 410000},
                      {"I": 410400, "N": "平顶山", "P": "Pingdingshan", "S": 410000},
                      {"I": 410500, "N": "安阳", "P": "Anyang", "S": 410000},
                      {"I": 410600, "N": "鹤壁", "P": "Hebi", "S": 410000},
                      {"I": 410700, "N": "新乡", "P": "Xinxiang", "S": 410000},
                      {"I": 410800, "N": "焦作", "P": "Jiaozuo", "S": 410000},
                      {"I": 410900, "N": "濮阳", "P": "Puyang", "S": 410000},
                      {"I": 411000, "N": "许昌", "P": "Xuchang", "S": 410000},
                      {"I": 411100, "N": "漯河", "P": "Luohe", "S": 410000},
                      {"I": 411200, "N": "三门峡", "P": "Sanmenxia", "S": 410000},
                      {"I": 411300, "N": "南阳", "P": "Nanyang", "S": 410000},
                      {"I": 411400, "N": "商丘", "P": "Shangqiu", "S": 410000},
                      {"I": 411500, "N": "信阳", "P": "Xinyang", "S": 410000},
                      {"I": 411600, "N": "周口", "P": "Zhoukou", "S": 410000},
                      {"I": 411700, "N": "驻马店", "P": "Zhumadian", "S": 410000},
                      {"I": 419001, "N": "济源", "P": "Jiyuan", "S": 410000},
                      {"I": 419900, "N": "其它", "P": "Qita", "S": 410000},
                      {"I": 420100, "N": "武汉", "P": "Wuhan", "S": 420000},
                      {"I": 420200, "N": "黄石", "P": "Huangshi", "S": 420000},
                      {"I": 420300, "N": "十堰", "P": "Shiyan", "S": 420000},
                      {"I": 420500, "N": "宜昌", "P": "Yichang", "S": 420000},
                      {"I": 420600, "N": "襄阳", "P": "Xiangyang", "S": 420000},
                      {"I": 420700, "N": "鄂州", "P": "Ezhou", "S": 420000},
                      {"I": 420800, "N": "荆门", "P": "Jingmen", "S": 420000},
                      {"I": 420900, "N": "孝感", "P": "Xiaogan", "S": 420000},
                      {"I": 421000, "N": "荆州", "P": "Jingzhou", "S": 420000},
                      {"I": 421100, "N": "黄冈", "P": "Huanggang", "S": 420000},
                      {"I": 421200, "N": "咸宁", "P": "Xianning", "S": 420000},
                      {"I": 421300, "N": "随州", "P": "Suizhou", "S": 420000},
                      {"I": 422800, "N": "恩施", "P": "Enshi", "S": 420000},
                      {"I": 429004, "N": "仙桃", "P": "Xiantao", "S": 420000},
                      {"I": 429005, "N": "潜江", "P": "Qianjiang", "S": 420000},
                      {"I": 429006, "N": "天门", "P": "Tianmen", "S": 420000},
                      {"I": 429021, "N": "神农架", "P": "Shennongjia", "S": 420000},
                      {"I": 429900, "N": "其它", "P": "Qita", "S": 420000},
                      {"I": 430100, "N": "长沙", "P": "Changsha", "S": 430000},
                      {"I": 430200, "N": "株洲", "P": "Zhuzhou", "S": 430000},
                      {"I": 430300, "N": "湘潭", "P": "Xiangtan", "S": 430000},
                      {"I": 430400, "N": "衡阳", "P": "Hengyang", "S": 430000},
                      {"I": 430500, "N": "邵阳", "P": "Shaoyang", "S": 430000},
                      {"I": 430600, "N": "岳阳", "P": "Yueyang", "S": 430000},
                      {"I": 430700, "N": "常德", "P": "Changde", "S": 430000},
                      {"I": 430800, "N": "张家界", "P": "Zhangjiajie", "S": 430000},
                      {"I": 430900, "N": "益阳", "P": "Yiyang", "S": 430000},
                      {"I": 431000, "N": "郴州", "P": "Chenzhou", "S": 430000},
                      {"I": 431100, "N": "永州", "P": "Yongzhou", "S": 430000},
                      {"I": 431200, "N": "怀化", "P": "Huaihua", "S": 430000},
                      {"I": 431300, "N": "娄底", "P": "Loudi", "S": 430000},
                      {"I": 433100, "N": "湘西", "P": "Xiangxi", "S": 430000},
                      {"I": 439900, "N": "其它", "P": "Qita", "S": 430000},
                      {"I": 440100, "N": "广州", "P": "Guangzhou", "S": 440000},
                      {"I": 440200, "N": "韶关", "P": "Shaoguan", "S": 440000},
                      {"I": 440300, "N": "深圳", "P": "Shenzhen", "S": 440000},
                      {"I": 440400, "N": "珠海", "P": "Zhuhai", "S": 440000},
                      {"I": 440500, "N": "汕头", "P": "Shantou", "S": 440000},
                      {"I": 440600, "N": "佛山", "P": "Foshan", "S": 440000},
                      {"I": 440700, "N": "江门", "P": "Jiangmen", "S": 440000},
                      {"I": 440800, "N": "湛江", "P": "Zhanjiang", "S": 440000},
                      {"I": 440900, "N": "茂名", "P": "Maoming", "S": 440000},
                      {"I": 441200, "N": "肇庆", "P": "Zhaoqing", "S": 440000},
                      {"I": 441300, "N": "惠州", "P": "Huizhou", "S": 440000},
                      {"I": 441400, "N": "梅州", "P": "Meizhou", "S": 440000},
                      {"I": 441500, "N": "汕尾", "P": "Shanwei", "S": 440000},
                      {"I": 441600, "N": "河源", "P": "Heyuan", "S": 440000},
                      {"I": 441700, "N": "阳江", "P": "Yangjiang", "S": 440000},
                      {"I": 441800, "N": "清远", "P": "Qingyuan", "S": 440000},
                      {"I": 441900, "N": "东莞", "P": "Dongguan", "S": 440000},
                      {"I": 442000, "N": "中山", "P": "Zhongshan", "S": 440000},
                      {"I": 445100, "N": "潮州", "P": "Chaozhou", "S": 440000},
                      {"I": 445200, "N": "揭阳", "P": "Jieyang", "S": 440000},
                      {"I": 445300, "N": "云浮", "P": "Yunfu", "S": 440000},
                      {"I": 449900, "N": "其它", "P": "Qita", "S": 440000},
                      {"I": 450100, "N": "南宁", "P": "Nanning", "S": 450000},
                      {"I": 450200, "N": "柳州", "P": "Liuzhou", "S": 450000},
                      {"I": 450300, "N": "桂林", "P": "Guilin", "S": 450000},
                      {"I": 450400, "N": "梧州", "P": "Wuzhou", "S": 450000},
                      {"I": 450500, "N": "北海", "P": "Beihai", "S": 450000},
                      {"I": 450600, "N": "防城港", "P": "Fangchenggang", "S": 450000},
                      {"I": 450700, "N": "钦州", "P": "Qinzhou", "S": 450000},
                      {"I": 450800, "N": "贵港", "P": "Guigang", "S": 450000},
                      {"I": 450900, "N": "玉林", "P": "Yulin", "S": 450000},
                      {"I": 451000, "N": "百色", "P": "Baise", "S": 450000},
                      {"I": 451100, "N": "贺州", "P": "Hezhou", "S": 450000},
                      {"I": 451200, "N": "河池", "P": "Hechi", "S": 450000},
                      {"I": 451300, "N": "来宾", "P": "Laibin", "S": 450000},
                      {"I": 451400, "N": "崇左", "P": "Chongzuo", "S": 450000},
                      {"I": 459900, "N": "其它", "P": "Qita", "S": 450000},
                      {"I": 460100, "N": "海口", "P": "Haikou", "S": 460000},
                      {"I": 460200, "N": "三亚", "P": "Sanya", "S": 460000},
                      {"I": 460300, "N": "三沙", "P": "Sansha", "S": 460000},
                      {"I": 460400, "N": "儋州", "P": "Danzhou", "S": 460000},
                      {"I": 469001, "N": "五指山", "P": "Wuzhishan", "S": 460000},
                      {"I": 469002, "N": "琼海", "P": "Qionghai", "S": 460000},
                      {"I": 469005, "N": "文昌", "P": "Wenchang", "S": 460000},
                      {"I": 469006, "N": "万宁", "P": "Wanning", "S": 460000},
                      {"I": 469007, "N": "东方", "P": "Dongfang", "S": 460000},
                      {"I": 469021, "N": "定安", "P": "Ding\'an", "S": 460000},
                      {"I": 469022, "N": "屯昌", "P": "Tunchang", "S": 460000},
                      {"I": 469023, "N": "澄迈", "P": "Chengmai", "S": 460000},
                      {"I": 469024, "N": "临高", "P": "Lingao", "S": 460000},
                      {"I": 469025, "N": "白沙", "P": "Baisha", "S": 460000},
                      {"I": 469026, "N": "昌江", "P": "Changjiang", "S": 460000},
                      {"I": 469027, "N": "乐东", "P": "Ledong", "S": 460000},
                      {"I": 469028, "N": "陵水", "P": "Lingshui", "S": 460000},
                      {"I": 469029, "N": "保亭", "P": "Baoting", "S": 460000},
                      {"I": 469030, "N": "琼中", "P": "Qiongzhong", "S": 460000},
                      {"I": 469900, "N": "其它", "P": "Qita", "S": 460000},
                      {"I": 500100, "N": "重庆", "P": "Chongqing", "S": 500000},
                      {"I": 510100, "N": "成都", "P": "Chengdu", "S": 510000},
                      {"I": 510300, "N": "自贡", "P": "Zigong", "S": 510000},
                      {"I": 510400, "N": "攀枝花", "P": "Panzhihua", "S": 510000},
                      {"I": 510500, "N": "泸州", "P": "Luzhou", "S": 510000},
                      {"I": 510600, "N": "德阳", "P": "Deyang", "S": 510000},
                      {"I": 510700, "N": "绵阳", "P": "Mianyang", "S": 510000},
                      {"I": 510800, "N": "广元", "P": "Guangyuan", "S": 510000},
                      {"I": 510900, "N": "遂宁", "P": "Suining", "S": 510000},
                      {"I": 511000, "N": "内江", "P": "Neijiang", "S": 510000},
                      {"I": 511100, "N": "乐山", "P": "Leshan", "S": 510000},
                      {"I": 511300, "N": "南充", "P": "Nanchong", "S": 510000},
                      {"I": 511400, "N": "眉山", "P": "Meishan", "S": 510000},
                      {"I": 511500, "N": "宜宾", "P": "Yibin", "S": 510000},
                      {"I": 511600, "N": "广安", "P": "Guang\'an", "S": 510000},
                      {"I": 511700, "N": "达州", "P": "Dazhou", "S": 510000},
                      {"I": 511800, "N": "雅安", "P": "Ya\'an", "S": 510000},
                      {"I": 511900, "N": "巴中", "P": "Bazhong", "S": 510000},
                      {"I": 512000, "N": "资阳", "P": "Ziyang", "S": 510000},
                      {"I": 513200, "N": "阿坝", "P": "Aba", "S": 510000},
                      {"I": 513300, "N": "甘孜", "P": "Garze", "S": 510000},
                      {"I": 513400, "N": "凉山", "P": "Liangshan", "S": 510000},
                      {"I": 519900, "N": "其它", "P": "Qita", "S": 510000},
                      {"I": 520100, "N": "贵阳", "P": "Guiyang", "S": 520000},
                      {"I": 520200, "N": "六盘水", "P": "Liupanshui", "S": 520000},
                      {"I": 520300, "N": "遵义", "P": "Zunyi", "S": 520000},
                      {"I": 520400, "N": "安顺", "P": "Anshun", "S": 520000},
                      {"I": 520500, "N": "毕节", "P": "Bijie", "S": 520000},
                      {"I": 520600, "N": "铜仁", "P": "Tongren", "S": 520000},
                      {"I": 522300, "N": "黔西南", "P": "Qianxinan", "S": 520000},
                      {"I": 522600, "N": "黔东南", "P": "Qiandongnan", "S": 520000},
                      {"I": 522700, "N": "黔南", "P": "Qiannan", "S": 520000},
                      {"I": 529900, "N": "其它", "P": "Qita", "S": 520000},
                      {"I": 530100, "N": "昆明", "P": "Kunming", "S": 530000},
                      {"I": 530300, "N": "曲靖", "P": "Qujing", "S": 530000},
                      {"I": 530400, "N": "玉溪", "P": "Yuxi", "S": 530000},
                      {"I": 530500, "N": "保山", "P": "Baoshan", "S": 530000},
                      {"I": 530600, "N": "昭通", "P": "Zhaotong", "S": 530000},
                      {"I": 530700, "N": "丽江", "P": "Lijiang", "S": 530000},
                      {"I": 530800, "N": "普洱", "P": "Pu\'er", "S": 530000},
                      {"I": 530900, "N": "临沧", "P": "Lincang", "S": 530000},
                      {"I": 532300, "N": "楚雄", "P": "Chuxiong", "S": 530000},
                      {"I": 532500, "N": "红河", "P": "Honghe", "S": 530000},
                      {"I": 532600, "N": "文山", "P": "Wenshan", "S": 530000},
                      {"I": 532800, "N": "西双版纳", "P": "Xishuangbanna", "S": 530000},
                      {"I": 532900, "N": "大理", "P": "Dali", "S": 530000},
                      {"I": 533100, "N": "德宏", "P": "Dehong", "S": 530000},
                      {"I": 533300, "N": "怒江", "P": "Nujiang", "S": 530000},
                      {"I": 533400, "N": "迪庆", "P": "Deqen", "S": 530000},
                      {"I": 539900, "N": "其它", "P": "Qita", "S": 530000},
                      {"I": 540100, "N": "拉萨", "P": "Lhasa", "S": 540000},
                      {"I": 540200, "N": "日喀则", "P": "Rikaze", "S": 540000},
                      {"I": 540300, "N": "昌都", "P": "Qamdo", "S": 540000},
                      {"I": 540400, "N": "林芝", "P": "Nyingchi", "S": 540000},
                      {"I": 540500, "N": "山南", "P": "Shannan", "S": 540000},
                      {"I": 542400, "N": "那曲", "P": "Nagqu", "S": 540000},
                      {"I": 542500, "N": "阿里", "P": "Ngari", "S": 540000},
                      {"I": 549900, "N": "其它", "P": "Qita", "S": 540000},
                      {"I": 610100, "N": "西安", "P": "Xi\'an", "S": 610000},
                      {"I": 610200, "N": "铜川", "P": "Tongchuan", "S": 610000},
                      {"I": 610300, "N": "宝鸡", "P": "Baoji", "S": 610000},
                      {"I": 610400, "N": "咸阳", "P": "Xianyang", "S": 610000},
                      {"I": 610500, "N": "渭南", "P": "Weinan", "S": 610000},
                      {"I": 610600, "N": "延安", "P": "Yan\'an", "S": 610000},
                      {"I": 610700, "N": "汉中", "P": "Hanzhong", "S": 610000},
                      {"I": 610800, "N": "榆林", "P": "Yulin", "S": 610000},
                      {"I": 610900, "N": "安康", "P": "Ankang", "S": 610000},
                      {"I": 611000, "N": "商洛", "P": "Shangluo", "S": 610000},
                      {"I": 619900, "N": "其它", "P": "Qita", "S": 610000},
                      {"I": 620100, "N": "兰州", "P": "Lanzhou", "S": 620000},
                      {"I": 620200, "N": "嘉峪关", "P": "Jiayuguan", "S": 620000},
                      {"I": 620300, "N": "金昌", "P": "Jinchang", "S": 620000},
                      {"I": 620400, "N": "白银", "P": "Baiyin", "S": 620000},
                      {"I": 620500, "N": "天水", "P": "Tianshui", "S": 620000},
                      {"I": 620600, "N": "武威", "P": "Wuwei", "S": 620000},
                      {"I": 620700, "N": "张掖", "P": "Zhangye", "S": 620000},
                      {"I": 620800, "N": "平凉", "P": "Pingliang", "S": 620000},
                      {"I": 620900, "N": "酒泉", "P": "Jiuquan", "S": 620000},
                      {"I": 621000, "N": "庆阳", "P": "Qingyang", "S": 620000},
                      {"I": 621100, "N": "定西", "P": "Dingxi", "S": 620000},
                      {"I": 621200, "N": "陇南", "P": "Longnan", "S": 620000},
                      {"I": 622900, "N": "临夏", "P": "Linxia", "S": 620000},
                      {"I": 623000, "N": "甘南", "P": "Gannan", "S": 620000},
                      {"I": 629900, "N": "其它", "P": "Qita", "S": 620000},
                      {"I": 630100, "N": "西宁", "P": "Xining", "S": 630000},
                      {"I": 630200, "N": "海东", "P": "Haidong", "S": 630000},
                      {"I": 632200, "N": "海北", "P": "Haibei", "S": 630000},
                      {"I": 632300, "N": "黄南", "P": "Huangnan", "S": 630000},
                      {"I": 632500, "N": "海南", "P": "Hainan", "S": 630000},
                      {"I": 632600, "N": "果洛", "P": "Golog", "S": 630000},
                      {"I": 632700, "N": "玉树", "P": "Yushu", "S": 630000},
                      {"I": 632800, "N": "海西", "P": "Haixi", "S": 630000},
                      {"I": 639900, "N": "其它", "P": "Qita", "S": 630000},
                      {"I": 640100, "N": "银川", "P": "Yinchuan", "S": 640000},
                      {"I": 640200, "N": "石嘴山", "P": "Shizuishan", "S": 640000},
                      {"I": 640300, "N": "吴忠", "P": "Wuzhong", "S": 640000},
                      {"I": 640400, "N": "固原", "P": "Guyuan", "S": 640000},
                      {"I": 640500, "N": "中卫", "P": "Zhongwei", "S": 640000},
                      {"I": 649900, "N": "其它", "P": "Qita", "S": 640000},
                      {"I": 650100, "N": "乌鲁木齐", "P": "Urumqi", "S": 650000},
                      {"I": 650200, "N": "克拉玛依", "P": "Karamay", "S": 650000},
                      {"I": 650400, "N": "吐鲁番", "P": "Turpan", "S": 650000},
                      {"I": 650500, "N": "哈密", "P": "Hami", "S": 650000},
                      {"I": 652300, "N": "昌吉", "P": "Changji", "S": 650000},
                      {"I": 652700, "N": "博尔塔拉", "P": "Bortala", "S": 650000},
                      {"I": 652800, "N": "巴音郭楞", "P": "Bayingol", "S": 650000},
                      {"I": 652900, "N": "阿克苏", "P": "Aksu", "S": 650000},
                      {"I": 653000, "N": "克孜勒苏", "P": "Kizilsu", "S": 650000},
                      {"I": 653100, "N": "喀什", "P": "Kashgar", "S": 650000},
                      {"I": 653200, "N": "和田", "P": "Hotan", "S": 650000},
                      {"I": 654000, "N": "伊犁", "P": "Ili", "S": 650000},
                      {"I": 654200, "N": "塔城", "P": "Qoqek", "S": 650000},
                      {"I": 654300, "N": "阿勒泰", "P": "Altay", "S": 650000},
                      {"I": 659001, "N": "石河子", "P": "Shihezi", "S": 650000},
                      {"I": 659002, "N": "阿拉尔", "P": "Aral", "S": 650000},
                      {"I": 659003, "N": "图木舒克", "P": "Tumxuk", "S": 650000},
                      {"I": 659004, "N": "五家渠", "P": "Wujiaqu", "S": 650000},
                      {"I": 659005, "N": "北屯", "P": "Beitun", "S": 650000},
                      {"I": 659006, "N": "铁门关", "P": "Tiemenguan", "S": 650000},
                      {"I": 659007, "N": "双河", "P": "Shuanghe", "S": 650000},
                      {"I": 659008, "N": "可克达拉", "P": "Kokdala", "S": 650000},
                      {"I": 659009, "N": "昆玉", "P": "Kunyu", "S": 650000},
                      {"I": 659900, "N": "其它", "P": "Qita", "S": 650000},
                      {"I": 710100, "N": "台北", "P": "Taipei", "S": 710000},
                      {"I": 810100, "N": "香港", "P": "Hong Kong Island", "S": 810000},
                      {"I": 820100, "N": "澳门", "P": "MacauPeninsula", "S": 820000},
                      {"I": 910100, "N": "海外", "P": "Haiwai", "S": 910000},
                      {"I": 999900, "N": "其它", "P": "Qita", "S": 990000}]}
    city_required = {"深圳", "长春", "郑州", "成都", "北京", "苏州", "武汉", "沈阳", "重庆", "上海", "大连", "杭州", "天津", "宁波", "广州", "南京",
                     "石家庄", "太原", "厦门", "青岛", "济南", "西安", "昆明", "贵阳", "长沙", "合肥", "常州", "台州", "潍坊"}

    def __init__(self,**kwargs):
        super(CarSpider,self).__init__(**kwargs)
        self.mailer=MailSender.from_settings(settings)
        self.counts=0
        self.carnum=800000

        settings.set('CrawlCar_Num',self.carnum,priority='cmdline')
        settings.set('MONGODB_DB','carbusiness',priority='cmdline')
        settings.set('MONGODB_COLLECTION',website,priority='cmdline')


    def start_requests(self):
        # yield scrapy.Request(url="https://carif.api.autohome.com.cn/dealer/LoadDealerPrice.ashx?_callback=dealerCallback&type=2&specid=32904&city=340100")
        for city in self.city_str["CityItems"]:
            if city["N"] in self.city_required:
                for i in range(0, 40000) + range(1000000, 1010000):
                    yield scrapy.Request(url="https://carif.api.autohome.com.cn/dealer/LoadDealerPrice.ashx?_callback=dealerCallback&type=2&specid=%d&city=%s" % (i, city["I"]))


    def parse(self, response):
        data = json.loads((response.body)[15:-1].decode("gbk"))["body"]["item"][0]
        if data != []:
            item = AutohomeLocalDealerPriceItem()
            item['grabtime'] = time.strftime('%Y-%m-%d %X', time.localtime())
            item['url'] = response.url
            item['autohomeId'] = data['SpecId']
            item['seriesId'] = data['SeriesId']
            item['price'] = data['Price']
            item['minPrice'] = data['MinPrice']
            item['carModelUrl'] = data['Url']
            item['dealerId'] = data['DealerId']
            item['cityName'] = data['CityName']
            item['cityId'] = data['CityId']
            item['status'] = response.url
            yield item