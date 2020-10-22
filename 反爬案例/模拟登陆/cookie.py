# -*- coding: utf-8 -*-
"""
@File    : cookie.py
@Time    : 2020/8/23 
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
# cookies='UM_distinctid=173bed1bcee6b5-0eb288a4cf2bc7-4313f6a-144000-173bed1bcef67d=1; CNZZDATA709406=cnzz_eid%3D1187917301-1596630303-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1598145662; Hm_lvt_3212511d67978fc36e99a8ba103a1cc8=1596634284,1598149021; Hm_lpvt_3212511d67978fc36e99a8ba103a1cc8=1598149021; CNZZDATA5642869=cnzz_eid%3D1725589002-1598148784-https%253A%252F%252Fwww.zhibo8.cc%252F%26ntime%3D1598148784'
# cookie1 = {data.split('=',1)[0]:data.split('=',1)[-1] for data in cookies.split(';')}
# cookie2 = {data.split('=',1)[0]:data.split('=',1)[1] for data in cookies.split(';')}
# line = cookies.split(';')
# cookie={}
# for i in line:
#     key,value = i.split('=',1)
#     cookie[key] = value
# print(cookie)
# print(cookie1)
# print(cookie2)
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
# print(browser.get_cookies())
cookies_list = browser.get_cookies()
cookies ={}
for cookie in cookies_list:
        str_cookie = '{0}={1};'
        str_cookie = str_cookie.format(cookie.get('name'), cookie.get('value'))
        cookies += str_cookie
print(cookies)
cookie_dict ={}
# 格式化打印cookie
for cookie in cookies_list:
    cookie_dict[cookie['name']]=cookie['value']
# list_cookies = driver.get_cookies()
# cookies = {}
# for s in list_cookies:
# cookies[s['name']] = s['value']
print(cookie_dict)


