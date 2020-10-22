# -*- coding: utf-8 -*-
"""
@File    : doutu.py
@Time    : 2020/8/16 
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
import os
import re

import requests
from lxml import etree
import chardet
from fake_useragent import UserAgent
from urllib.request import urlretrieve
ua = UserAgent()
HEADERS = {"user-agent": ua.random}  # 指定浏览器 user-agent
def get_page(url):
    response = requests.get(url, headers=HEADERS)
    try:
        if response.status_code == 200:
            response.encoding = chardet.detect(response.content)['encoding']
            return response.text
        return None
    except requests.exceptions.ConnectionError as e:
        print(e.args)

def parse_page(content):
    data = etree.HTML(content)
    imgs = data.xpath('//div[@class="page-content text-center"]//img')
    for img in imgs:
        img_url = img.get('data-original')
        name = img.get('alt')
        # 去除图片名的特殊字符
        name = re.sub(r'[\?？\.,。,！!]','',name)
        # 获取后缀名
        suffix = os.path.splitext(img_url)[1]
        filename = name + suffix
        img_path = 'images'
        if not os.path.exists(img_path):
            os.makedirs(img_path)
        urlretrieve(img_url,img_path+ os.path.sep +filename)

def main():
    for page in range(1,21):
        url = 'https://www.doutula.com/photo/list/?page={}'.format(page)
        data= get_page(url)
        parse_page(data)
        # print(url)
        # print(content)

if __name__ == '__main__':
    main()
