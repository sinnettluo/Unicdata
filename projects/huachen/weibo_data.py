import pandas as pd
import pymysql
from sqlalchemy import create_engine
import re
from pybloom_live import ScalableBloomFilter
from hashlib import md5

num = 1000000
bf = ScalableBloomFilter(initial_capacity=num, error_rate=0.001)
def not_empty(s):
    return s and s.strip()

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
# sql = "select * from content_senti where tag='luntan'"
# sql = "select * from content_senti where tag='luntan'"
sql = "select * from content_senti where tag='weibo'"

pd.set_option('display.max_columns', None)
df = pd.read_sql_query(sql, conn)

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

# key = "sword"
key = "match_regex"
wg_list = df_wg[key].drop_duplicates().values.tolist()
ssd_list = df_ssd[key].drop_duplicates().values.tolist()
ck_list = df_ck[key].drop_duplicates().values.tolist()
xjb_list = df_xjb[key].drop_duplicates().values.tolist()
yh_list = df_yh[key].drop_duplicates().values.tolist()
dl_list = df_dl[key].drop_duplicates().values.tolist()
kj_list = df_kj[key].drop_duplicates().values.tolist()
ns_list = df_ns[key].drop_duplicates().values.tolist()

weidu_dic = {"外观":wg_list, "舒适性":ssd_list, "操控":ck_list, "性价比":xjb_list, "油耗":yh_list, "动力":dl_list, "空间":kj_list, "内饰":ns_list}

df1 = df
# 遍历df
full_data_list = list()
for index, row in df1.iterrows():
    print("*" * 100)
    count = 0
    # 遍历weidu_list
    str_list = re.split(" |!|\?|，|。", row["value"])
    new_str_list = list(filter(not_empty, str_list))
    data_dic = dict()
    for k, v in weidu_dic.items():
        #         # 判断df["value"]是否包含有tab list中关键词
        # data_list = list()
        if k in row["value"]:
            for s in new_str_list:
                if k in s:
                    match_str = "|".join(v)
                    content = re.findall(match_str, s)
                    #                     print(content)
                    if len(content) > 0:
                        data_dic["variable"] = row["variable"]
                        data_dic["row_names"] = row["row_names"]
                        data_dic["value"] = row["value"]
                        data_dic["tag"] = row["tag"]
                        data_dic["weidu"] = k
                        data_dic["content"] = content[0]
                        status = k + '_' + content[0]
                        #                         print(data_dic)
                        i = md5(status.encode("utf8")).hexdigest()
                        returndf = bf.add(i)

                        if not returndf:
                            items = list()
                            items.append(data_dic)
                            save_df = pd.DataFrame(items)
                            save_df.to_sql(name='content_weibo_middle', con=conn, if_exists="append", index=False)
                        else:
                            print("重复数据!")

        else:
            count += 1
            if count == 8:
                data_dic["variable"] = row["variable"]
                data_dic["row_names"] = row["row_names"]
                data_dic["value"] = row["value"]
                data_dic["tag"] = row["tag"]
                data_dic["weidu"] = None
                items = list()
                items.append(data_dic)
                save_df = pd.DataFrame(items)
                save_df.to_sql(name='content_weibo_null', con=conn, if_exists="append", index=False)
                    # data_dic["content"] = content[0]
#                     for xr in sword_list:
#                     for xr in match_list:
#                         match_str = xr
#                         content = re.findall(match_str, s)
#                         if len(content)>0:
#                             print(content)
#                         if xr in s:
#                             match_tab = k + xr
#                             data_dic["weidu"] = k
#                             data_dic["sword"] = xr
#                             data_dic["taidu"] = v[v["sword"]==xr]["taidu"].iloc[[0][0]]
#                             data_dic["variable"] = row["variable"]
#                             data_dic["row_names"] = row["row_names"]
#                             data_dic["value"] = row["value"]
#                             status = row["row_names"]+'_'+k+'_'+xr
#                             b_status = row["row_names"]+'_'+k+'_'+"大"
#                             bb_status = row["row_names"]+'_'+k+'_'+"大大"
#                             s_status = row["row_names"]+'_'+k+'_'+"小"
#                             ss_status = row["row_names"]+'_'+k+'_'+"小小"
#                             if status == b_status or status == bb_status:
#                                 full_data_list.append(s_status)
#                                 full_data_list.append(ss_status)
#                             if status not in full_data_list:
#                                 full_data_list.append(status)
# #                                 print(data_dic)
#                                 items = list()
#                                 items.append(data_dic)
#                                 save_df = pd.DataFrame(items)
#                                 save_df.to_sql(name='content_luntan', con=conn, if_exists="append", index=False)
#                             else:
#                                 print("重复数据")


# weidu_dics = {"外观":df_wg, "舒适性":df_ssd, "操控":df_ck, "性价比":df_xjb, "油耗":df_yh, "动力":df_dl, "空间":df_kj, "内饰":df_ns}

# df1 = df
# # 遍历df
# full_data_list = list()
# for index, row in df1.iterrows():
#     print("*" * 100)
#     count = 0
#     # 遍历weidu_list
#     str_list = re.split(" |!|\?|，|。", row["value"])
#     new_str_list = list(filter(not_empty, str_list))
#     data_dic = dict()
#     for k, v in weidu_dics.items():
#         #         # 判断df["value"]是否包含有tab list中关键词
#         if k in row["value"]:
#             #             comment = row["value"]
#             #             print(comment)
#             #             print(new_str_list)
#             #             print("*"*100)
#             #             weidu = k
#
#             sword_list = v["sword"].drop_duplicates().values.tolist()
#             #             print(sword_list)
#             data_list = list()
#             for s in new_str_list:
#                 if k in s:
#                     # #                     match_str = "|".join(v)
#                     # #                     content = re.findall(match_str, s)
#                     # #                     print(content)
#                     for xr in sword_list:
#                         if xr in s:
#                             match_tab = k + xr
#                             data_dic["weidu"] = k
#                             data_dic["sword"] = xr
#                             data_dic["taidu"] = v[v["sword"] == xr]["taidu"].iloc[[0][0]]
#                             data_dic["variable"] = row["variable"]
#                             data_dic["row_names"] = row["row_names"]
#                             data_dic["value"] = row["value"]
#                             status = row["row_names"] + '_' + k + '_' + xr
#                             if status not in full_data_list:
#                                 full_data_list.append(status)
#                                 print(data_dic)
#                                 items = list()
#                                 items.append(data_dic)
#                                 save_df = pd.DataFrame(items)
#                                 save_df.to_sql(name='content_luntan', con=conn, if_exists="append", index=False)
#                             else:
#                                 print("重复数据")






