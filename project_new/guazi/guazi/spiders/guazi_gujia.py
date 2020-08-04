# -*- coding: utf-8 -*-
import pymongo
import scrapy
from pandas import DataFrame

connection = pymongo.MongoClient('192.168.2.149', 27017)
db = connection["guazi"]
collection = db["guazi_car"]
model_data = collection.find({},
                             {"brand_id": 1, "brandname": 1, "family_id": 1, "famliyname": 1, "vehicle": 1,
                              "vehicle_id": 1, "years": 1, "_id": 0})

car_msg_list = list(model_data)
car_msg_df = DataFrame(car_msg_list)
car_msg_df_new = car_msg_df.drop_duplicates('vehicle_id')


class GuaziGujiaSpider(scrapy.Spider):
    name = 'guazi_gujia'
    allowed_domains = ['guazi.com']
    start_urls = ['http://guazi.com/']

    @classmethod
    def update_settings(cls, settings):
        settings.setdict(
            getattr(cls, 'custom_debug_settings' if getattr(cls, 'is_debug', False) else 'custom_settings', None) or {},
            priority='spider')

    def __init__(self, **kwargs):
        super(GuaziGujiaSpider, self).__init__(**kwargs)
        self.counts = 0
        self.car_msg_df_new = car_msg_df_new

    is_debug = True
    custom_debug_settings = {
        'MYSQL_SERVER': '192.168.1.94',
        'MYSQL_DB': 'chexiu',
        'MYSQL_TABLE': 'chexiu',
        'MONGODB_SERVER': '192.168.2.149',
        'MONGODB_DB': 'guazi',
        'MONGODB_COLLECTION': 'guazi_car',
        'CONCURRENT_REQUESTS': 8,
        'DOWNLOAD_DELAY': 0,
        'LOG_LEVEL': 'DEBUG',

    }

    def start_requests(self):
        for index, rows in self.car_msg_df_new.iterrows():
            brand_id = rows['brand_id']
            brandname = rows['brandname']
            family_id = rows['family_id']
            familyname = rows['famliyname']
            vehicle = rows['vehicle']
            vehicle_id = rows['vehicle_id']
            years = int(rows['years'])
            # print(index, brand_id, brandname, family_id, familyname, vehicle, vehicle_id, years)
            localyears = int(datetime.now().year)
            localmonth = int(datetime.now().month)
            areaCodes = ['110100', '310100', '440100', '510100']
            for year in range(years - 1, localyears + 1):
                if year == localyears:
                    month = localmonth - 1
                    mile = '0.1'
                else:
                    month = localmonth
                    mile = (localyears - year) * 2
                for areaCode in areaCodes:
                    url = f'http://www.hx2car.com/tools/assessDetail.htm?serialOne={brand_id}&year={year}&month={month}&mile={mile}&areaCode={areaCode}&serid={family_id}&keyword={brandname},{familyname},{vehicle}&carType={vehicle_id}'
                    yield scrapy.Request(url=url, meta={"info": (vehicle_id, year, month, mile, areaCode)})

    def parse(self, response):
        pass
