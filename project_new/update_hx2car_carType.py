import re
import requests
from pandas import DataFrame
import pymysql

coon = pymysql.connect(
    host='192.168.1.94',
    user='dataUser94',
    password='94dataUser@2020',
    database='usedcar_update',
    charset='utf8'
)
cursor = coon.cursor()
sql = '''
SELECT id,carid,url
FROM hx2car_online
'''
cursor.execute(sql)
countAll = cursor.fetchall()


# print(countAll)

# # panda库去重操作
# car_msg_list = list(countAll)
# car_msg_df = DataFrame(car_msg_list)
# car_msg_df_new = car_msg_df.drop_duplicates('carid')
# print(car_msg_df_new)
# url = 'https://www.hx2car.com/details/1416247347'


def getProxy():
    s = requests.session()
    s.keep_alive = False

    url = 'http://120.27.216.150:5000'
    headers = {
        'Connection': 'close',
    }
    proxy = s.get(url=url, headers=headers, auth=('admin', 'zd123456')).text[0:-6]
    return proxy


for id, carid, url in countAll:
    # print(carid, url)
    proxy = {'http': getProxy()}
    response = requests.get(url=url, proxies=proxy)
    carType = re.findall(r'carType :\'(\d+)\'', response.text)
    if carType != []:
        print(id, carid, url)
        newcarid = carType[0]
        # print(newcarid)
        sql_upd = 'update hx2car_online set newcarid =%s where carid =%s'
        cursor.execute(sql_upd, (newcarid, carid))
        coon.commit()

cursor.close()
coon.close()
