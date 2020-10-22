# -*- coding: utf-8 -*-
"""
@File    : cookies.py
@Time    : 2020/8/14 
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
# import os
# import requests
# from urllib.parse import urlencode
# from hashlib import md5
# from multiprocessing.pool import Pool
from selenium import webdriver
def get_cookies(url):
    str = ''
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    browser = webdriver.Chrome(options=options)
    browser.get(url)
    for i in browser.get_cookies():
        try:
            name = i.get('name')
            value = i.get('value')
            str = str + name + '=' + value + ';'
            print(str)
        except ValueError as e:
            print(e)
    return str



if __name__ == '__main__':
    URL = 'https://www.toutiao.com/'
    get_cookies(URL)
