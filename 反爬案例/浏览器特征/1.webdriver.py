# -*- coding: utf-8 -*-
"""
@File    : 1.浏览器特征.py
@Time    : 2020/8/30 
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
'''
对接webdriver反爬，若检测到是webdriver就不显示
'''
# 未开启selenium的webdriver屏蔽
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
#webdiver的屏蔽
BASE_URL = 'https://antispider1.scrape.center/'
INDEX_URL = urljoin(BASE_URL, '/page/1')
option = ChromeOptions()
option.add_argument('--headless')
option.add_experimental_option("excludeSwitches", ["enable-automation"])#开启selenium开发者模式
option.add_experimental_option(
            'useAutomationExtension', False)#取消自动化控制显示

# option.add_argument("--disable-extensions")
# option.add_experimental_option("debuggerAddress","127.0.0.1:9222")
browser = webdriver.Chrome(options=option)
wait = WebDriverWait(browser,10)
browser.get(INDEX_URL)
# 编写修改navigator.webdriver值的JavaScript代码来解决webdriver被屏蔽问题
# script = 'Object.defineProperty(navigator, "webdriver", {get: () => false,});'
# browser.execute_script(script)
# browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
#         "source": """
#         Object.defineProperty(navigator, 'webdriver', {
#           get: () => undefined
#         })
#       """
#     })
# print(browser.page_source)
# browser.execute_script('Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});')
browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
button = wait.until(EC.presence_of_element_located((By.CLASS_NAME,'btn-next')))
button.click()
time.sleep(10)

# res = browser.page_source()
# print(res)
# time.sleep(10)




