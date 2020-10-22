# -*- coding: utf-8 -*-
"""
@File    : 1-滑块.py
@Time    : 2020/9/6
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
import time
from io import BytesIO
from selenium import webdriver
from selenium.webdriver import ChromeOptions, ActionChains
from PIL import Image



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
        self.login_url = 'https://captcha1.scrape.center/'
        # 账号密码
        self.user = 'admin'
        self.password = 'admin'

    def login(self):
        self.driver.get(self.login_url)

        user_input = self.driver.find_element_by_xpath('//input[@type="text"]')
        user_input.send_keys(self.user)
        pwd_input = self.driver.find_element_by_xpath(
            '//input[@type="password"]')
        pwd_input.send_keys(self.password)
        button = self.driver.find_element_by_xpath('//button[@type="button"]')
        button.click()

    def get_screenshot(self):
        '''
        获取屏幕截图
        '''
        shot = self.driver.get_screenshot_as_png()
        shot = Image.open(BytesIO(shot))
        return shot

    def position(self):
        """
        用户获取验证码的四条边
        :return
        """
        # # 定位锁按钮，模拟点击
        # el_lock = self.driver.find_element_by_xpath('...')
        # el_lock.click()
        # 定位图片对象
        img = self.driver.find_element_by_xpath(
            '//div[@class="geetest_slicebg geetest_absolute"]')
        time.sleep(2)
        # 获取图片对象的坐标
        location = img.location
        print(location)

        # 获取图片对象尺寸
        size = img.size
        print(size)
        # print(str(size))
        # screenshot =self.get_screenshot()
        # print(screenshot.size)

        left, top, right, bottom = int(location['x']), int(location['y']), int(
            location['x'] + size['width']), int(location['y'] + size['height'])
        # 计算图片的截取区域
        return left, top, right, bottom

    def get_image(self):
        '''
        获取两张验证码图片
        '''
        # 获取验证码的位置
        posi = self.position()
        # 屏幕截图
        shot1 = self.get_screenshot()
        # 抠出没有滑块和阴影的验证码图片
        captcha1 = shot1.crop(posi)
        with open('captcha.png', 'wb') as f:
            captcha1.save(f)
        # 点击验证码拖动按钮
        el_button = self.driver.find_element_by_class_name(
            'geetest_slider_button')
        el_button.click()
        # 以下是在第一次点击验证码时，没有出现缺口才进行的操作
        # 等待错误提示信息
        time.sleep(4)
        # 屏幕截图
        shot2 = self.get_screenshot()
        # 抠验证码图
        captcha2 = shot2.crop(posi)
        with open('captcha2.png', 'wb') as f:
            captcha2.save(f)
        # 返回两个验证码对象
        return captcha1, captcha2, el_button

    def is_pixel_equal(self, img1, img2, x, y):
        """
        判断两个像素是否相同
        :param image1: 图片 1
        :param image2: 图片 2
        :param x: 位置 x
        :param y: 位置 y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pixel1 = img1.load()[x, y]
        pixel2 = img2.load()[x, y]
        threshold = 60
        if abs(
                pixel1[0] -
                pixel2[0]) < threshold and abs(
            pixel1[1] -
            pixel2[1]) < threshold and abs(
            pixel1[2] -
            pixel2[2]) < threshold:
            return True
        else:
            return False

    def get_gap(self, image1, image2):
        '''
        比对两个验证码的相同位置的元素，找出像素偏差的最大值，
        返回其x值.
        :param img1:没有缺口的验证码
        :param img2:有缺口的验证码
        :return:对比之后的偏移值
        '''
        left = 60
        for i in range(left, image1.size[0]):
            for j in range(image2.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    def get_track(self, offset):
        """
        根据偏移量获取移动轨迹
        :param offset: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = offset * 4 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0

        while current < offset:
            if current < mid:
                # 加速度为正 2
                a = 2
            else:
                # 加速度为负 3
                a = -3
            # 初速度 v0
            v0 = v
            # 当前速度 v = v0 + at
            v = v0 + a * t
            # 移动距离 x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def move_to_gap(self, el_button, tracks):
        """
        拖动滑块到缺口处
        :param el_button: 滑块
        :param tracks: 轨迹
        :return:
        """
        ActionChains(self.driver).click_and_hold(el_button).perform()
        # 模拟人的操作
        ActionChains(
            self.driver).move_by_offset(
            xoffset=100,
            yoffset=0).perform()
        ActionChains(
            self.driver).move_by_offset(
            xoffset=-
            100,
            yoffset=0).perform()
        for x in tracks:
            ActionChains(
                self.driver).move_by_offset(
                xoffset=x,
                yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.driver).release().perform()

    def do_captcha(self):
        '''
           实现验证码的处理
        '''
        # 1.获取验证码图片&有阴影拼图的验证码图片
        image1 = self.get_image()
        image2 = self.get_image()

        el_button = self.get_image()
        # 2.比较两个验证码图片获取滑块的偏移量
        offset = self.get_gap(image1, image2)
        # 3.使用偏移量计算移动操作
        track = self.get_track(offset)
        # 4.操作滑块按钮，模拟拖动滑块做验证码登陆
        self.move_to_gap(track, el_button)

    def main(self):
        '''
        主逻辑
        '''
        # 1.登录页面输入密码
        self.login()
        # 2.处理验证码
        self.do_captcha()


if __name__ == '__main__':
    res = HuaKuai()
    res.main()
