import random
import time
from io import BytesIO

import requests
from PIL import Image
from redis import Redis
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# from  .niuniu_jiema import dama
# from .niuniu_jiema import dama
from niuniucar.niuniu_jiema import dama

BORDER = 6


# 注册
class CrackGeetest():
    def __init__(self, phone):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--window-size=1903x523')
        # chrome_options.add_argument('--disable-gpu')
        self.url = 'http://www.niuniuqiche.com/login'
        self.browser = webdriver.Chrome('E:\Chromedriver\chromedriver.exe', chrome_options=chrome_options)
        #
        # self.browser = webdriver.Chrome(r"E:\Chromedriver\chromedriver.exe",options=chrome_options)
        # self.browser.set_window_size(1903, 523)
        #
        self.browser.maximize_window()
        self.wait = WebDriverWait(self.browser, 20)
        self.phone = phone
        # --------------------------------------------------------------------------
        self.redis_cli = Redis(host="192.168.1.248", port=6379, db=3)
        # self.redis_cli = Redis(host="192.168.1.249", port=6379, db=2)
        self.fa_cookie = open("cookie.text", "a")

        self.cookie = {}

    # 程序完成，自动结束程序
    def __del__(self):
        self.browser.close()
        self.fa_cookie.close()

    def open(self):
        """
        打开网页
        :return: None
        """
        self.browser.get(self.url)
        self.browser.find_element_by_xpath("//ul/li[2]/a").click()
        self.browser.find_element_by_xpath(
            "//div[@id='modal_sign_up']//div[@class='form-group']//input[@id='user_mobile']").send_keys(
            self.phone)
        # self.browser.find_element_by_xpath("//div[@class='form-group']//input[@id='user_password']").send_keys(
        #     "1002076417")

    def get_geetest_button(self):
        """
        获取初始验证按钮
        :return:
        """
        # 验证按钮
        # button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip')))
        button = self.browser.find_element_by_xpath(
            "//div[@id='sign_up_captcha']//div[@class='geetest_btn']//div[@class='geetest_radar_tip']")
        # button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_radar_tip_content')))
        return button

    def get_position(self):
        """
        获取验证码位置
        :return: 验证码位置元组
        """
        img = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'geetest_canvas_img')))
        print('img')
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return (top, bottom, left, right)

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot

    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return slider

    def get_geetest_image(self, name='captcha.png'):
        """
        获取验证码图片
        :return: 图片对象
        """
        top, bottom, left, right = self.get_position()
        print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def delete_style(self):
        '''
        执行js脚本，获取无滑块图
        :return None
        '''
        # js = 'document.querySelector("canvas")[3].style=""'
        time.sleep(5)
        js = "document.getElementsByClassName('geetest_canvas_fullbg geetest_fade geetest_absolute')[0].style=\'null\'"
        # js = 'document.querySelectorAll("canvas")[3].style=""'
        a = self.browser.execute_script(js)
        time.sleep(5)
        print(a)
        print("js已经失效")

    # def change_to_slide(self):
    #     '''
    #     切换为滑动认证
    #     :return 滑动选项对象
    #     '''
    #     huadong = self.wait.until(
    #         EC.element_to_be_clickable((By.CSS_SELECTOR, '.products-content ul > li:nth-child(2)'))
    #     )
    #     return huadong

    def get_gap(self, image1, image2):
        """
        获取缺口偏移量
        :param image1: 带缺口图片
        :param image2: 不带缺口图片
        :return:
        """
        left = 60
        print(image1.size[0])
        print(image1.size[1])
        for i in range(left, image1.size[0]):
            # print(1)
            for j in range(image1.size[1]):

                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left + 1
        return left

    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 60
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_track(self, distance):
        track = []
        current = 0
        mid = distance * 3 / 4
        t = random.randint(3, 4) / 10
        v = 0
        while current < distance:
            if current < mid:
                a = 2
            else:
                a = -3
            v0 = v
            v = v0 + a * t
            move = v0 * t + 1 / 2 * a * t * t
            current += move
            track.append(round(move))
        return track

    # 生成拖拽移动轨迹

    def move_to_gap(self, slider, track):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        """
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()

    # def wait_pic(self):
    #     '''
    #     等待验证图片加载完成
    #     :return None
    #     '''
    #     self.wait.until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, '.geetest_popup_wrap'))
    #     )
    def send_msg(self):
        self.browser.find_element_by_xpath('//*[@id="btn_valid_code"]').click()
        try:
            yizhuce = self.browser.find_element_by_xpath('//*[@id="modal_sign_up"]/div/div/div[2]/div').text
        except:
            yizhuce = 'success'
        if yizhuce == '该手机号已注册,请重新输入':
            print("该手机号已注册,请重新输入")
            return yizhuce
        #     ************************** 需要跳转到登陆页面
        else:
            print("该手机号可以注册")
            return yizhuce

    def Fill_msg(self, code):
        self.browser.find_element_by_xpath('//*[@id="valid_code"]').send_keys(code)
        self.browser.find_element_by_xpath('//*[@id="sign_up_next"]').click()
        time.sleep(3)
        self.login()

    def login(self):

        self.browser.find_element_by_xpath('//*[@id="new_user"]/fieldset[1]/div[1]/input').send_keys("1002076417")
        self.browser.find_element_by_xpath('//*[@id="new_user"]/fieldset[1]/div[2]/input').send_keys('1002076417')
        self.browser.find_element_by_xpath('//*[@id="new_user"]/fieldset[1]/div[3]/input').send_keys(
            str(random.randint(1000, 200000)) + str(random.randint(0, 100)))
        self.browser.find_element_by_xpath('//select/option[{}]'.format(str(random.randint(2, 20)))).click()
        time.sleep(3)
        self.browser.find_element_by_xpath('//*[@id="sign_up_finish"]').click()
        time.sleep(5)
        self.cookie = self.browser.get_cookies()
        self.save_cookie()

    def crack(self):
        try:
            # 点击注册 然后发送手机号
            self.open()
            print("手机号已经输入")
            # 点击验证按钮
            # s_button = self.change_to_slide()
            # time.sleep(1)
            # s_button.click()
            button = self.get_geetest_button()
            button.click()
            print("已经点击了滑块")
            time.sleep(1)
            # 确认图片加载完成
            # self.wait_pic()
            # 获取滑块
            slider = self.get_slider()
            # 获取带缺口验证码图片
            image1 = self.get_geetest_image('captcha1.png')
            # 获取不带缺口的验证码图片
            self.delete_style()
            time.sleep(3)
            image2 = self.get_geetest_image('captcha2.png')
            # self.delete_style_test()
            # 获取缺口位置
            gap = self.get_gap(image2, image1)
            print('缺口位置', gap)
            # 减去缺口位移
            gap -= BORDER
            # 获取移动轨迹
            track = self.get_track(gap)
            print('滑动轨迹', track)
            time.sleep(1)
            # 拖动滑块
            self.move_to_gap(slider, track)
            time.sleep(2)
            # 判断是否滑动成功
            # try:
            # success = self.wait.until(
            #     EC.text_to_be_present_in_element_value((By.CLASS_NAME, 'geetest_success_radar_tip_content'), '验证成功')
            # )
            success = self.browser.find_element_by_xpath(
                '//*[@id="sign_up_captcha"]/div/div[2]/div[2]/div/div[2]/span[1]').text
            print(success, "*" * 50)

            if success == '验证成功':
                print("验证成功")
            else:
                print("验证失败，重新在来一次")
                print(1 / 0)
            # print("验证成功")
            # 验证成功之后，需要输入动态验证码
            # print(success)

            # get_cookie = self.send_msg()
            # print(success)
            time.sleep(1)
        except:
            print('失败，再来一次')
            self.crack()

    def save_cookie(self):
        try:
            for i in self.cookie:
                if i['name'] == '_niu_niu_session':
                    self.fa_cookie.write(str(i['value']) + "\r\n")
                    self.redis_cli.sadd("niuniu_cookie", str(i['value']))
                    print("cookie--------------------",str(i['value']))
                    break
        except:
            print(self.cookie, "这个cookie可能有问题")
            self.redis_cli.sadd("niuniu_cookie", str(self.cookie))


if __name__ == '__main__':
    # --------------------------------------------------------------------------
    redis_cli1 = Redis(host="192.168.1.248", port=6379, db=3)
    # redis_cli1 = Redis(host="127.0.0.1", port=6379, db=2)
    sum = redis_cli1.scard("niuniu_cookie")
    time_cookie = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    if sum < 100:
        print("更新cookie的时间{}*****************************".format(time_cookie))
        jiema = dama("1002076418", "2232881")
        jiema.get_token()
        for i in range(20):
            jiema.get_number()
            crack = CrackGeetest(jiema.number)
            crack.crack()
            state = crack.send_msg()
            time.sleep(15)
            msg_state = jiema.get_msg()
            if msg_state == None:
                time.sleep(15)
                msg_state = jiema.get_msg()
            if msg_state == None:
                print("验证码一直获取不到")
                print(state)
            elif state == 'success' and msg_state != None:
                crack.Fill_msg(jiema.msg)
                # jiema.release()
                print(jiema.number, jiema.token)
                print(crack.cookie)
                # crack.__del__()
            else:
                print("手机号已经注册过了")
                # crack.__del__()
    else:
        print("cookie 还有50个   应该够用")
