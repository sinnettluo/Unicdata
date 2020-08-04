import re
import requests
from lxml import etree
import time
from io import BytesIO
from selenium import webdriver
from selenium.webdriver import ChromeOptions

url = 'https://www.hx2car.com/details/1416247347'
headers = {
    # 'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/84.0.4147.89',
    'Connection': 'keep-alive'
}


def getProxy():
    s = requests.session()
    s.keep_alive = False

    url = 'http://120.27.216.150:5000'
    headers = {
        'Connection': 'close',
    }
    proxy = s.get(url=url, headers=headers, auth=('admin', 'zd123456')).text[0:-6]
    return proxy


proxy = {'http': getProxy()}
response = requests.get(url=url, headers=headers, proxies=proxy)
# print(response.text)
i = re.findall(r'carType :\'(\d+)\'', response.text)[0]
print(i)
