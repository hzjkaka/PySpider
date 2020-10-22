import time
# from io import BytesIO

import requests
from selenium import webdriver
from selenium.webdriver import ChromeOptions, ActionChains
# from PIL import Image
import cv2 as cv
import numpy as np

class HuaKuai():
    def __init__(self):
        # 配置webdriver菜单
        self.option = ChromeOptions()
        self.option.add_experimental_option(
            "excludeSwitches", ["enable-automation"])  # 开发者模式
        self.option.add_experimental_option(
            'useAutomationExtension', False)  # 取消chrome受自动控制提示
        # 创建浏览器对象
        self.driver = webdriver.Chrome(options=self.option)
        self.driver.implicitly_wait(3)
        self.login_url = 'https://dun.163.com/trial/sense'
        # 账号密码
        # self.user = 'admin'
        # self.password = 'admin'

    def login(self):
        self.driver.get(self.login_url)
        self.driver.find_element_by_xpath('//li[@captcha-type="jigsaw"]').click()
        time.sleep(1)
        self.driver.find_element_by_xpath('//div[@class="yidun_intelli-tips"]').click()
        time.sleep(1)

    def imageurl(self):
        '''
        获取屏幕截图
        '''
        b_img = self.driver.find_element_by_xpath('//div[@class="yidun_bgimg"]/img[1]').get_attribute('src')
        h_img = self.driver.find_element_by_xpath('//div[@class="yidun_bgimg"]/img[2]').get_attribute('src')
        return b_img,h_img

    def get_image(self):
        '''
        获取两张验证码图片
        '''
        # 下载两张验证码到本地
        b_url,h_url = self.imageurl()
        #背景图
        captcha1 = requests.get(b_url).content
        with open('captcha1.jpg', 'wb') as f:
             f.write(captcha1)
        #滑块图
        captcha2 = requests.get(h_url).content
        with open('captcha2.png', 'wb') as f:
            f.write(captcha2)
        # 屏幕截图
        # shot1 = self.get_screenshot()
        # # 抠出没有滑块和阴影的验证码图片
        # captcha1 = shot1.crop(posi)
        # with open('captcha.png', 'wb') as f:
        #     captcha1.save(f)

    def do_captcha(self):
        '''
        处理图片识别缺口
        :return
        '''
        bg = cv.imread('captcha1.jpg')
        hg = cv.imread('captcha2.png')

        #灰度处理
        bg = cv.cvtColor(bg,cv.COLOR_BGR2GRAY)
        hg = cv.cvtColor(hg,cv.COLOR_BGR2GRAY)

        #截取滑块
        hg = hg[hg.any(1)]

        # 匹配缺口
        result = cv.matchTemplate(bg,hg,cv.TM_CCOEFF_NORMED)#精度高但是慢

        print(result[0])
        result2 = np.argmax(result) # 返回的是一维的
        # print(result2)
        #反着推最大值的位置
        x,y=np.unravel_index(result2,result.shape)
        # print(x,y)
        w,h = hg.shape
        cv.rectangle(bg,(y,x),(y+w,x+h),(38,38,38),2)
        # cv.imshow('gray',bg)
        # cv.imshow('gray1',hg)
        # cv.waitKey(0)
        # cv.destroyAllWindows()
        slider = self.driver.find_element_by_xpath('//div[@class="yidun_slider"]')
        ActionChains(self.driver).drag_and_drop_by_offset(slider,xoffset=y,yoffset=0).perform()
if __name__ == '__main__':
    res = HuaKuai()
    # res.login()
    # res.get_image()
    res.do_captcha()

''':arg
A = np.random.randint(1,100,size=(2,3,5))
# 声明一个size=(3,3,3,2)的数组
print(A)
array([[[98, 29, 32, 73, 90],
        [36, 52, 24,  2, 37],
        [66, 80, 23, 29, 98]],

       [[17, 32, 58, 99, 74],
        [53,  3, 20, 48, 28],
        [53,  7, 74, 34, 68]]])

ind_max = np.argmax(A)
print(ind_max)
18
# 此时得到的索引是将A数组flattern(展成一维数组)后的索引，如何得到对应的原数组的索引呢？


ind_max_src = np.unravel_index(ind_max, A.shape)
print(ind_max_src)
(1, 0, 3)

# 函数numpy.unravel_index(indices, dims)返回的索引值从0开始计数。
print(A[ind_max_src])
99
'''