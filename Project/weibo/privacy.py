# -*- coding: utf-8 -*-
"""
@File    : privacy.py
@Time    : 2020/9/25 
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
import re

import requests
from  fake_useragent import UserAgent
import time
import random
from jsonpath import jsonpath

# 实例化 User-Agent 对象
ua = UserAgent()
# 随机浏览器 User-Agent
HEADERS = {'User-Agent': ua.random,
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'cookie':'_T_WM=67561273784; WEIBOCN_FROM=1110006030; XSRF-TOKEN=03b0f9; SCF=AjY2Zk3NNDhMIo74-89G0d1W5kAlW-Lz2pfDobEoonPcEhbBJpHGB6ydlfvEpPpUEOKS0tPdWr1yiuDcSz8pZ38.; SUB=_2A25yaSJzDeRhGeNO7VsY8SjOzj6IHXVRkk47rDV6PUJbktANLWHDkW1NTsq3S0r-JyWbzDjYwK0-jMGGaLZPjFr1; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFF.9.l4w9m5nXcsLvMjUeb5NHD95Qfehq41K2ceo-EWs4DqcjGCGD3Cc8uqBtt; SUHB=010GpPkoTf2cHh; SSOLoginState=1600999971; MLOGIN=1; M_WEIBOCN_PARAMS=oid%3D4551866664627187%26lfid%3D1076031732927460%26luicode%3D20000174%26uicode%3D20000174',
            'referer': 'https://m.weibo.cn/'
}

TIME = random.randint(1, 3)
BASIC_URl = 'https://m.weibo.cn'
# PROXY_POOL_URL = 'http://localhost:5555/random'
ID = '4551208402421931'
MID = '4551208402421931'
class  DoubanSpider():
    def __init__(self):
        self.url = f'{BASIC_URl}/comments/hotflow?id={ID}&mid={MID}'
        self.headers = HEADERS

    def weibo_comment(self):
        max_id = ""
        while True:
            if max_id == "":
                url = f"https://m.weibo.cn/comments/hotflow?id={ID}&mid={MID}"
            else:
                url = f"https://m.weibo.cn/comments/hotflow?id={ID}&mid={MID}&max_id=" + str(
                    max_id)
            # print(url)
            response = requests.get(url, headers=HEADERS)
            comment = response.json()

            if comment['ok'] == 0:
                break
            max_id = comment["data"]["max_id"]
            # print([data_1["text"] for data_1 in comment["data"]["data"]])
            line = []
            for comment_data in comment["data"]["data"]:
                data = comment_data["text"]
                p = re.compile(r'(<span.*>.*</span>)*(<a.*>.*</ a>)?')
                data = p.sub(r'', data)
                if len(data) != 0:
                    line.append(data)
            print(len(line))
            time.sleep(1)
            for li in line:
                print('=='*40+'\n'+li)

    def main(self):
        self.weibo_comment()
            # content = self.get_page(url)
            # max_id = self.parse_data(content)
            # # url = f'{BASIC_URl}/comments/hotflow?id={ID}&mid={MID}&max_id={max_id}'
            # content = self.get_page(url)
            # data = self.parse_data(content)
            # # print(list(data)[1])
            # for i in list(data)[1]:
            #     print('=='*40+'\n'+i)
            # # self.save_data(data)

if __name__ == '__main__':
    response = DoubanSpider()
    response.main()

