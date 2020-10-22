# -*- coding: utf-8 -*-
"""
@File    : 4.ip.py
@Time    : 2020/8/30 
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""


from fake_useragent import UserAgent
import requests
from parsel import Selector
import time
import random
# 使用随机的身份标识
headers = {'User-Agent':UserAgent().random}
url = 'https://antispider5.scrape.center/'
# 向目标网址发起网络请求，但将客户端身份标识切换为上述设置的随机身份
res = requests.get(url=url,headers=headers)
# 打印输出状态码
print(res.status_code)
#应对爬取频率过快问题
time.sleep(random.randint(1,2))
# 如果本次请求的状态码为200则继续，否则提示失败
if res.status_code == 200:
    sel = Selector(res.text)
    # 根据HTML标签和属性从响应正文中提取电影标题
    res = sel.css('.m-b-sm::text').getall()
    print(res)