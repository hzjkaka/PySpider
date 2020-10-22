# -*- coding: utf-8 -*-
"""
@File    : 1.jwtdenglu.py
@Time    : 2020/8/13
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
# json web token登陆，爬取页面数据
from fake_useragent import UserAgent
import random
import requests
from pymongo import MongoClient
from urllib.parse import urljoin
import time


'''
第一，模拟网站登录操作的请求，比如携带用户名和密码信息请求登录接口，获取服务器返回结果，这个结果中通常包含 JWT 字符串的信息，保存下来即可。
第二，后续的请求携带 JWT 访问即可，一般情况在 JWT 不过期的情况下都能正常访问和执行对应的操作。携带方式多种多样，因网站而异。
第三，如果 JWT 过期了，可能需要重复步骤一，重新获取 JWT。
'''
# 随机化请求头和请求IP
# 最常用的方式
# 写爬虫最实用的是可以随意变换headers，一定要有随机性。支持随机生成请求头
ua = UserAgent()
HEADERS = {"user-agent": ua.random}  # 指定浏览器 user-agent
TIME = random.randint(1, 3)

BASE_URL = 'https://login3.scrape.cuiqingcai.com'
LOGIN_URL = urljoin(BASE_URL, '/api/login')
USERNAME = 'admin'
PASSWORD = 'admin'
TOTAL_PAGE = 10

# 数据库存储
MONGO_CONNECTION = 'mongodb://localhost:27017/'
MONGO_DB_NAME = 'Scrape'
MONGO_COLLECTION_NAME = 'movies3'


class Scrape3Spider():
    def __init__(self):
        self.login_url = LOGIN_URL
        self.username = USERNAME
        self.password = PASSWORD
        self.headers = HEADERS

    def login(self):
        json = {'username': self.username,
                'password': self.password}
        r_login = requests.post(
            self.login_url,
            json=json,
            headers=self.headers)
        data = r_login.json()
        # print('Response JSON', data)
        jwt = data.get('token')
        # print('JWT:', jwt)
        return jwt

    def get_index(self, offset, jwt):
        headers = {
            "user-agent": ua.random,
            'Authorization': f'jwt {jwt}'
        }
        url = f'{BASE_URL}/api/book/?limit=18&offset={offset}'
        print(url)
        r = requests.get(url, headers=headers)
        try:
            if r.status_code == 200:
                return r.json()
            return None
        except requests.exceptions.ConnectionError as e:
            print(e.args)

    def parse_index(self, content):
        datas = content.get('results')
        data_list =[]
        for data in datas:
            name = data.get('name')
            authors = str(
                data.get('authors')).replace(
                '\\n',
                ' ').replace(
                ' ',
                '')
            cover = data.get('cover')
            score = data.get('score')
            if len(str(score))!=0 and len(str(authors)) != 0:
                item ={
                    'name': name,
                    'authors': authors,
                    'cover': cover,
                    'score': score
                }
                data_list.append(item)
        return data_list


    def save_data(self, data):
        clinet = MongoClient(MONGO_CONNECTION)
        db = clinet[MONGO_DB_NAME]
        col = db[MONGO_COLLECTION_NAME]
        # 做到即插及更新upsert=True
        # col.insert_many(data)
        col.update_many({'name': data.get('name')}, {
            "$set": data}, upsert=True)

    def main(self):
        jwt = self.login()
        for offset in range(0, TOTAL_PAGE):
            content = self.get_index(offset * 18, jwt)
            data = self.parse_index(content)
            for i in data:
               self.save_data(i)



if __name__ == '__main__':
    response = Scrape3Spider()
    response.main()
    time.sleep(TIME)
