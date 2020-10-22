# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html


from scrapy.http import HtmlResponse
from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium .webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions




class SeleniumMiddleware(object):
    def __init__(self):
        self.option = ChromeOptions()
        self.option.add_experimental_option(
            "excludeSwitches", ["enable-automation"])  # 避免被检测
        self.option.add_experimental_option(
            'useAutomationExtension', False)  # 取消chrome受自动控制提示
        self.driver = webdriver.Chrome(options=self.option)
        self.wait = WebDriverWait(self.driver, 3)

    def process_request(self, request, spider):
        url = 'https://image.so.com/z?ch=beauty'
        self.driver.get(url)
        time.sleep(1)
        try:
            while True:
                submit_1 = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, '//li[1]//img/@src')))
                submit_1.click()
                time.sleep(0.5)
                if not submit_1:
                    break
                else:
                    sumbit_2 = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'switcher next')))
                    sumbit_2.click()
                    time.sleep(0.5)
        except:
            pass
        response = HtmlResponse(url=request.url, body=self.driver.page_source, request=request, encoding='utf-8',
                                status=200)
        return response
