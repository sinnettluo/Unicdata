__author__ = 'cagey'
import pandas as pd
import pymysql
from sqlalchemy import create_engine
from pybloom_live import ScalableBloomFilter
from hashlib import md5
import re
from multiprocessing import Process
from multiprocessing import Pool
import os, time, random

def not_empty(s):
    return s and s.strip()

# num = 1000000
# bf = ScalableBloomFilter(initial_capacity=num, error_rate=0.001)

settings = {
    "MYSQL_USER": "dataUser94",
    "MYSQL_PWD": "94dataUser@2020",
    "MYSQL_SERVER": "192.168.1.94",
    "MYSQL_PORT": "3306",
    "MYSQL_DB": "huachen",
    "MYSQL_TABLE": "content_senti",
    # "MONGODB_SERVER": "192.168.1.94",
    # "MONGODB_PORT": 27017,
    # "MONGODB_DB": "luntan",
    # "MONGODB_COLLECTION": "tousu"
}

tabs_list = [
    {"good":["仪表盘","外形","时尚","内饰","时尚","车身","性价比","外观","尾灯","用料","空间","动力","操控","舒适性","座椅","空调","操控","安全","底盘","动力","天窗","屏幕"]},
    {"bad":["后排","大灯","动力","起步","油耗","空间","发动机","仪表盘","外形","时尚","内饰","时尚","车身","性价比","外观","尾灯","用料","空间","动力","操控","舒适性","座椅","空调","操控","安全","底盘","动力","天窗","屏幕"]},
]

conn = create_engine(f'mysql+pymysql://{settings["MYSQL_USER"]}:{settings["MYSQL_PWD"]}@{settings["MYSQL_SERVER"]}:{settings["MYSQL_PORT"]}/{settings["MYSQL_DB"]}?charset=utf8')

sql = "select * from content_koubei"
pd.set_option('display.max_columns', None)
df1 = pd.read_sql_query(sql, conn)



df = df1[1:10000]
# df
num = 1000000
bf = ScalableBloomFilter(initial_capacity=num, error_rate=0.001)

def work(content):
    if "最满意" in content or "最不满意" in content:
        str_list = re.split(" |!|\?|，|。", row["value"])
        new_str_list = list(filter(not_empty, str_list))
        data_dic = dict()
        for text in new_str_list:
            if "最满意" in text:
                for my in tabs_list[0]["good"]:
                    #                 for  in tabs_list:
                    if my in text:
                        data_dic["sword"] = my
                        data_dic["weidu"] = 'good'
                        data_dic["variable"] = row["variable"]
                        data_dic["row_names"] = row["row_names"]
                        #                         data_dic["value"] = row["value"]
                        data_dic["content"] = text
                        status = row["variable"] + '_' + row["row_names"] + '_' + text
                        #                         print(data_dic)
                        i = md5(status.encode("utf8")).hexdigest()
                        returndf = bf.add(i)
                        if not returndf:
                            items = list()
                            items.append(data_dic)
                            save_df = pd.DataFrame(items)
                            save_df.to_sql(name='content_koubei_gb', con=conn, if_exists="append", index=False)
                            print("-" * 50 + "insert data" + "-" * 50)
                        #                             print(data_dic)

                        else:
                            print("重复数据!")

            if "最不满意" in text:
                for bmy in tabs_list[1]["bad"]:
                    if bmy in text:
                        data_dic["sword"] = bmy
                        data_dic["weidu"] = 'bad'
                        data_dic["variable"] = row["variable"]
                        data_dic["row_names"] = row["row_names"]
                        #                         data_dic["value"] = row["value"]
                        data_dic["content"] = text
                        status = row["variable"] + '_' + row["row_names"] + '_' + text
                        #                         print(data_dic)
                        i = md5(status.encode("utf8")).hexdigest()
                        returndf = bf.add(i)
                        if not returndf:
                            items = list()
                            items.append(data_dic)
                            save_df = pd.DataFrame(items)
                            save_df.to_sql(name='content_koubei_gb', con=conn, if_exists="append", index=False)
                            print("-" * 50 + "insert data" + "-" * 50)
                        #                             print(data_dic)

                        else:
                            print("重复数据!")



for index, row in df.iterrows():
    #     for k,v in weidu_dic.items():
    content = row["value"]
    work(content)
    # if "最满意" in content or "最不满意" in content:
    #     str_list = re.split(" |!|\?|，|。", row["value"])
    #     new_str_list = list(filter(not_empty, str_list))
    #     data_dic = dict()
    #     for text in new_str_list:
    #         if "最满意" in text:
    #             for my in tabs_list[0]["good"]:
    #                 #                 for  in tabs_list:
    #                 if my in text:
    #                     data_dic["sword"] = my
    #                     data_dic["weidu"] = 'good'
    #                     data_dic["variable"] = row["variable"]
    #                     data_dic["row_names"] = row["row_names"]
    #                     #                         data_dic["value"] = row["value"]
    #                     data_dic["content"] = text
    #                     status = row["variable"] + '_' + row["row_names"] + '_' + text
    #                     #                         print(data_dic)
    #                     i = md5(status.encode("utf8")).hexdigest()
    #                     returndf = bf.add(i)
    #                     if not returndf:
    #                         items = list()
    #                         items.append(data_dic)
    #                         save_df = pd.DataFrame(items)
    #                         save_df.to_sql(name='content_koubei_gb', con=conn, if_exists="append", index=False)
    #                         print("-" * 50 + "insert data" + "-" * 50)
    #                     #                             print(data_dic)
    #
    #                     else:
    #                         print("重复数据!")
    #
    #         if "最不满意" in text:
    #             for bmy in tabs_list[1]["bad"]:
    #                 if bmy in text:
    #                     data_dic["sword"] = bmy
    #                     data_dic["weidu"] = 'bad'
    #                     data_dic["variable"] = row["variable"]
    #                     data_dic["row_names"] = row["row_names"]
    #                     #                         data_dic["value"] = row["value"]
    #                     data_dic["content"] = text
    #                     status = row["variable"] + '_' + row["row_names"] + '_' + text
    #                     #                         print(data_dic)
    #                     i = md5(status.encode("utf8")).hexdigest()
    #                     returndf = bf.add(i)
    #                     if not returndf:
    #                         items = list()
    #                         items.append(data_dic)
    #                         save_df = pd.DataFrame(items)
    #                         save_df.to_sql(name='content_koubei_gb', con=conn, if_exists="append", index=False)
    #                         print("-" * 50 + "insert data" + "-" * 50)
    #                     #                             print(data_dic)
    #
    #                     else:
    #                         print("重复数据!")



