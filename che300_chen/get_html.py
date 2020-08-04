import requests
from lxml import etree
import time
from io import BytesIO
from selenium import webdriver
from selenium.webdriver import ChromeOptions

url = 'https://www.che300.com/partner/result.php?prov=22&city=22&brand=30&series=386&model=21359&registerDate=2014-1&mileAge=13.17&intention=0&partnerId=douyin&unit=1&sn=93a15125acc736ab66bb791a1e37ae1a&sld=cd'
headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/84.0.4147.89',
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


ip = getProxy()
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_argument(('--proxy-server=' + ip))
driver = webdriver.Chrome(r'C:\Users\13164\Desktop\chromedriver.exe', chrome_options=option)
driver.get(url=url)
time.sleep(20)
driver.quit()
