__author__ = 'cagey'

import pandas as pd
import pymysql
from sqlalchemy import create_engine
from pybloom_live import ScalableBloomFilter
from hashlib import md5

num = 1000000
bf = ScalableBloomFilter(initial_capacity=num, error_rate=0.001)

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
conn = create_engine(f'mysql+pymysql://{settings["MYSQL_USER"]}:{settings["MYSQL_PWD"]}@{settings["MYSQL_SERVER"]}:{settings["MYSQL_PORT"]}/{settings["MYSQL_DB"]}?charset=utf8')
# sql = "select * from content_senti where tag='weibo'"
sql = "select * from content_luntan_middle"
pd.set_option('display.max_columns', None)

df1 = pd.read_sql_query(sql, conn)


table = "wp_tags_light"
sql_wg = f"select * from {table} where weidu='外观'"
sql_ssd = f"select * from {table} where weidu='舒适性'"
sql_ck = f"select * from {table} where weidu='操控'"
sql_xjb = f"select * from {table} where weidu='性价比'"
sql_yh = f"select * from {table} where weidu='油耗'"
sql_dl = f"select * from  {table} where weidu='动力'"
sql_kj = f"select * from  {table} where weidu='空间'"
sql_ns = f"select * from  {table} where weidu='内饰'"

df_wg = pd.read_sql_query(sql_wg, conn)
df_ssd = pd.read_sql_query(sql_ssd, conn)
df_ck = pd.read_sql_query(sql_ck, conn)
df_xjb = pd.read_sql_query(sql_xjb, conn)
df_yh = pd.read_sql_query(sql_yh, conn)
df_dl = pd.read_sql_query(sql_dl, conn)
df_kj = pd.read_sql_query(sql_kj, conn)
df_ns = pd.read_sql_query(sql_ns, conn)


key = "sword"
# key = "match_regex"
wg_list = df_wg[key].drop_duplicates().values.tolist()
ssd_list = df_ssd[key].drop_duplicates().values.tolist()
ck_list = df_ck[key].drop_duplicates().values.tolist()
xjb_list = df_xjb[key].drop_duplicates().values.tolist()
yh_list = df_yh[key].drop_duplicates().values.tolist()
dl_list = df_dl[key].drop_duplicates().values.tolist()
kj_list = df_kj[key].drop_duplicates().values.tolist()
ns_list = df_ns[key].drop_duplicates().values.tolist()
weidu_dic = {"外观":wg_list, "舒适性":ssd_list, "操控":ck_list, "性价比":xjb_list, "油耗":yh_list, "动力":dl_list, "空间":kj_list, "内饰":ns_list}

tabs_list = [
    {"weidu":"空间","zm": ["空间大", "空间宽敞", "空间不错", "空间舒适", "空间好", "空间满意", "空间舒服", "空间多", "空间可以", "空间充足", "空间赞", "空间足够"], "zmxr": ["大", "宽敞", "不错", "舒适", "好", "满意", "舒服", "多", "可以", "充足", "赞", "足够"], "zx": ["高度可调", "空间不大不小", "空间隐蔽", "设计运动", "空间常见", "空间不常见"], "zxxr": ["可调", "不大不小", "隐蔽", "运动", "常见", "不常见"], "fm": ["空间小", "空间不大", "空间一般", "空间不满意", "空间局促", "空间不够", "空间压抑", "空间不多", "面积小", "空间不足", "空间狭小", "空间差"], "fmxr": ["小", "不大", "一般", "不满意", "局促", "不够", "压抑", "不多", "小", "不足", "狭小", "差"]},
    {"weidu":"动力","zm": ["动力不错", "动力强劲", "动力好", "动力强", "动力充沛", "动力足", "动力源源不断", "动力快", "动力足够", "动力给力", "动力充足", "动力大"], "zmxr": ["不错", "强劲", "好", "强", "充沛", "足", "源源不断", "快", "足够", "给力", "充足", "大"], "zx": ["动力不足", "动力马马虎虎", "动力中等", "动力不普遍", "配置常见", "动力常见"], "zxxr": ["不足", "马马虎虎", "中等", "不普遍", "常见", "常见"], "fm": ["动力肉", "动力不足", "动力弱", "动力一般", "动力差", "动力小", "动力不够", "配置低", "动力不大", "动力少", "动力纠结", "动力不好"], "fmxr": ["肉", "不足", "弱", "一般", "差", "小", "不够", "低", "不大", "少", "纠结", "不好"]},
    {"weidu":"操控","zm": ["操控好", "操控不错", "操控精准", "操控满意", "操控灵活", "操控舒适", "操控优秀", "操控舒服", "操控稳", "操控方便", "操控棒", "操控出色"], "zmxr": ["好", "不错", "精准", "满意", "灵活", "舒适", "优秀", "舒服", "稳", "方便", "棒", "出色"], "zx": ["操控运动"], "zxxr": ["运动"], "fm": ["操控差", "操控一般", "操控不好", "操控不灵活", "操控麻烦", "操控弱", "操控不强", "操控难", "操控不牛", "操控模糊", "稳定性差", "操控不敢恭维"], "fmxr": ["差", "一般", "不好", "不灵活", "麻烦", "弱", "不强", "难", "不牛", "模糊", "差", "不敢恭维"]},
    {"weidu":"油耗","zm": ["油耗平均", "油耗低", "油耗满意", "油耗不错", "油耗不高", "油耗好", "油耗可以", "油耗省油", "油耗习惯", "油耗省", "油耗正常", "油耗实际"], "zmxr": ["平均", "低", "满意", "不错", "不高", "好", "可以", "省油", "习惯", "省", "正常", "实际"], "zx": ["油耗普遍", "油耗不满意"], "zxxr": ["普遍", "不满意"], "fm": ["油耗高", "油耗大", "油耗多", "油耗不低", "油耗吓人", "油耗差", "油耗不爽", "油耗一般", "油耗不少", "油耗不准", "油耗费油", "油耗不满意"], "fmxr": ["高", "大", "多", "不低", "吓人", "差", "不爽", "一般", "不少", "不准", "费油", "不满意"]},
    {"weidu":"舒适性","zm": ["舒适性不错", "舒适性好", "舒适性高", "舒适性良好", "舒适性大", "舒适性满意", "舒适性棒", "舒适性重要", "舒适性强", "舒适性关键", "舒适性完美", "舒适性不差"], "zmxr": ["不错", "好", "高", "良好", "大", "满意", "棒", "重要", "强", "关键", "完美", "不差"], "zx": ["普遍"], "zxxr": ["普遍"], "fm": ["舒适性差", "舒适性一般", "舒适性不好", "舒适性不强", "舒适性不够", "舒适性不满意", "舒适性不高", "舒适性不出色"], "fmxr": ["差", "一般", "不好", "不强", "不够", "不满意", "不高", "不出色"]},
    {"weidu":"外观","zm": ["外观大气", "外观不错", "外观霸气", "外观耐看", "外观好看", "外观稳重", "外观漂亮", "外观时尚", "外观神", "外观满意", "外观沉稳", "颜色齐全"], "zmxr": ["大气", "不错", "霸气", "耐看", "好看", "稳重", "漂亮", "时尚", "神", "满意", "沉稳", "齐全"], "zx": ["外观运动", "风格运动", "高度可调", "外观见仁见智", "外观仁者见仁智者见智", "造型运动", "颜色少见", "设计运动", "外观不运动", "外观普普通通", "颜色淡", "风格不传统"], "zxxr": ["运动", "运动", "可调", "见仁见智", "仁者见仁智者见智", "运动", "少见", "运动", "不运动", "普普通通", "淡", "不传统"], "fm": ["外观中庸", "外观小", "外观老气", "外观一般", "外观不好看", "外观不大", "外观普通", "外观小气", "外观不张扬", "外观老", "外观丑", "外观不感冒"], "fmxr": ["中庸", "小", "老气", "一般", "不好看", "不大", "普通", "小气", "不张扬", "老", "丑", "不感冒"]},
    {"weidu":"性价比","zm": ["性价比高", "性价比不错", "性价比好", "性价比最好", "性价比出色", "性价比满意", "性价比大", "性价比重要", "性价比豪华", "性价比合适", "性价比关键", "性价比超值"], "zmxr": ["高", "不错", "好", "最好", "出色", "满意", "大", "重要", "豪华", "合适", "关键", "超值"], "zx": ["普遍"], "zxxr": ["普遍"], "fm": ["性价比不高", "性价比低", "性价比差", "性价比一般", "性价比不给力", "性价比不好", "性价比弱", "性价比不合理", "性价比不出色", "性价比不满意", "性价比不划算", "性价比错"], "fmxr": ["不高", "低", "差", "一般", "不给力", "不好", "弱", "不合理", "不出色", "不满意", "不划算", "错"]},
    {"weidu":"动力","zm": ["动力不错", "动力强劲", "油耗平均", "动力好", "油耗低", "动力强", "动力充沛", "动力足", "油耗满意", "动力源源不断", "油耗不错", "动力快"], "zmxr": ["不错", "强劲", "平均", "好", "低", "强", "充沛", "足", "满意", "源源不断", "不错", "快"], "zx": ["动力不足", "发动机常见", "重量轻", "调教运动", "速度常见", "重量小", "重量重", "动力马马虎虎", "油耗普遍", "重量高", "重量不重", "重量大"], "zxxr": ["不足", "常见", "轻", "运动", "常见", "小", "重", "马马虎虎", "普遍", "高", "不重", "大"], "fm": ["油耗高", "动力肉", "油耗大", "排量小", "油耗多", "动力不足", "动力弱", "声音大", "噪声大", "转速低", "动力一般", "动力差"], "fmxr": ["高", "肉", "大", "小", "多", "不足", "弱", "大", "大", "低", "一般", "差"]},
]

df = df1[1:100]

for index, row in df.iterrows():

    #     for k,v in weidu_dic.items():
    for tab in tabs_list:
        #         if tab["weidu"]
        data_dic = dict()
        content = row["content"]
        if tab["weidu"] in content:
            count = 0
            for zmxr in tab["zmxr"]:
                if zmxr in content:
                    count += 1
                    data_dic["weidu"] = tab["weidu"]
                    data_dic["sword"] = zmxr
                    data_dic["taidu"] = 'good'
                    data_dic["variable"] = row["variable"]
                    data_dic["row_names"] = row["row_names"]
                    data_dic["value"] = row["value"]
                    status = row["row_names"] + '_' + tab["weidu"] + '_' + zmxr
                    i = md5(status.encode("utf8")).hexdigest()
                    returndf = bf.add(i)
                    if not returndf:
                        items = list()
                        items.append(data_dic)
                        save_df = pd.DataFrame(items)
                        save_df.to_sql(name='content_luntan_test1', con=conn, if_exists="append", index=False)
                        print("-" * 50 + "insert data" + "-" * 50)
                    else:
                        print("重复数据!")
            if count == 0:
                for z in tab["zxxr"]:
                    if z in content:
                        count += 1
                        data_dic["weidu"] = tab["weidu"]
                        data_dic["sword"] = z
                        data_dic["taidu"] = 'comm'
                        data_dic["variable"] = row["variable"]
                        data_dic["row_names"] = row["row_names"]
                        data_dic["value"] = row["value"]
                        status = row["row_names"] + '_' + tab["weidu"] + '_' + z
                        i = md5(status.encode("utf8")).hexdigest()
                        returndf = bf.add(i)

                        if not returndf:
                            items = list()
                            items.append(data_dic)
                            save_df = pd.DataFrame(items)
                            save_df.to_sql(name='content_luntan_test1', con=conn, if_exists="append", index=False)
                            print("-" * 50 + "insert data" + "-" * 50)
                        else:
                            print("重复数据!")
            else:
                for fmxr in tab["fmxr"]:
                    if fmxr in content:
                        count += 1
                        data_dic["weidu"] = tab["weidu"]
                        data_dic["sword"] = fmxr
                        data_dic["taidu"] = 'bad'
                        data_dic["variable"] = row["variable"]
                        data_dic["row_names"] = row["row_names"]
                        data_dic["value"] = row["value"]
                        status = row["row_names"] + '_' + tab["weidu"] + '_' + fmxr
                        i = md5(status.encode("utf8")).hexdigest()
                        returndf = bf.add(i)

                        if not returndf:
                            items = list()
                            items.append(data_dic)
                            save_df = pd.DataFrame(items)
                            save_df.to_sql(name='content_luntan_test1', con=conn, if_exists="append", index=False)
                            print("-" * 50 + "insert data" + "-" * 50)
                        else:
                            print("重复数据!")








