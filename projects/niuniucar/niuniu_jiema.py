import re
import time

import requests
from redis import Redis


class dama():
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.fa = open("./success_phone", "a")
        # --------------------------------------------------------------------------
        self.redis_cli = Redis(host="192.168.1.248", port=6379, db=3)
        # self.redis_cli = Redis(host="192.168.1.249", port=6379, db=2)

    def get_token(self):
        print("正在获取token", "*" * 50)
        # http://193.112.99.161:8000/api/sign/username=用户名&password=密码
        url = "http://193.112.99.161:8000/api/sign/username={}&password={}".format(self.user, self.password)
        dict1 = requests.get(url=url).content.decode('utf-8')
        print('token', dict1.split("|")[1], "-" * 50)
        # self.token = dict1["ret"]["token"]
        self.token = dict1.split("|")[1]

    def get_number(self):
        print("正在获取手机号", "*" * 50)
        # http://193.112.99.161:8000/api/yh_qh/id=项目ID&operator=0&Region=0&card=0&phone=&loop=1&token=登录返回token
        url = "http://193.112.99.161:8000/api/yh_qh/id={}&operator=0&Region=0&card=0&phone=&loop=1&token={}".format(
            16784, self.token, )
        dict1 = requests.get(url=url).content.decode('utf-8')
        print(dict1)
        if dict1.split("|")[0] == "1":

            print(dict1, "-" * 50)
            self.number = dict1.split("|")[1]

        elif(dict1.split("|")[0] == "0"):
            time.sleep(5)
            self.get_number()
            print("现在暂时没有账号，等待5秒----------------------------------------------------------------------")


    def get_msg(self):
        # time.sleep(30)
        print("正在获取短信验证码", "*" * 50)
        url = "http://193.112.99.161:8000/api/yh_qm/id={}&phone={}&t={}&token={}".format(16784, self.number, 1002076418,
                                                                                         self.token, )
        dict1 = requests.get(url=url).content.decode('utf-8')
        print(dict1, "-" * 50)
        if dict1.split("|") == '1':
            self.get_token()
            print("token 已经过期，重新登录----------------------------------------------------------------------")
        try:
            self.msg = re.findall("您的验证码是(\d+),该验", dict1.split("|")[1])[0]
            self.fa.writelines(self.number + '\n')
            self.redis_cli.sadd("niuniu_phone", self.number)
        except:
            print("还未发送验证码")
            self.msg = None
        else:
            return self.msg
        # else:
        #     if dict1.split("|")[1] == "未收到短信":
        #         print("还未发送验证码")
        #         self.msg = None
        #     else:
        #         # 0|【牛牛汽车】 您的验证码是4951,该验证码将在15分钟之后失效|模板错误请联系客服
        #         self.msg = dict1.split("|")["-1"]
        #         self.fa.writelines(self.number + '\n')
        #         self.redis_cli.sadd("niuniu_phone", self.number)
        #     return self.msg

    def release(self):
        print("正在释放手机号", "*" * 50)
        # http://193.112.99.161:8000/api/yh_sf/id=项目ID&phone=手机号码&token=登录返回token
        url = "http://193.112.99.161:8000/api/yh_sf/id={}&phone={}&token={}".format(16784, self.number, self.token,
                                                                                    )
        dict1 = requests.get(url=url).content.decode('utf-8')
        print(dict1, "-" * 50)
        # self.number = dict1["ret"]["number"]

    def __del__(self):
        # url = "http://api.yyyzmpt.com/index.php/clients/online/completeWork?token={}".format(
        #     self.token,
        # )
        # requests.get(url=url)
        self.fa.close()

# if __name__ =='__main__':
#  pass

# if __name__ == '__main__':
#     niuniu = dama("a1002076418", "2232881")
#     niuniu.get_token()
#     print(niuniu.token)
#     niuniu.get_number()
#     niuniu.get_msg()
#     pass
#     # niuniu =dama()
#     # dama.release("17501480705")
#     url = "http://api.yyyzmpt.com/index.php/clients/online/completeWork?token={}&number={}".format(
#         'ef987cfcd3e2d09fc005ab77a5d03d78', '18831731438'
#     )
#     dict1 = requests.get(url=url).json()
#
#     print(dict1)
#     url = "http://api.yyyzmpt.com/index.php/clients/online/completeWork?token={}".format(
#         'ef987cfcd3e2d09fc005ab77a5d03d78'
#     )
#     dict1 = requests.get(url=url).json()
#
#     print(dict1)
