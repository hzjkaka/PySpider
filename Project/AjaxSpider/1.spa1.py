# -*- coding: utf-8 -*-
"""
@File    : 1.spa1.py
@Time    : 2020/8/28
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
import requests
import jsonpath
from fake_useragent import UserAgent
import time
from pymongo import MongoClient
HEADERS = {"User-Agent": UserAgent().random}  # 指定浏览器 User-Agent
TPAGE = 10
# 数据库存储
MONGO_CONNECTION = 'mongodb://localhost:27017/'
MONGO_DB_NAME = 'Scrape'
MONGO_COLLECTION_NAME = 'movies5'


class Crawler(object):
    def __init__(self):
        self.headers = HEADERS
        self.client = MONGO_CONNECTION
        self.db = MONGO_DB_NAME
        self.col = MONGO_COLLECTION_NAME

    def get_page(self, url):
        try:
            r = requests.get(url=url, headers=self.headers)
            if r.status_code == 200:
                # 返回json数据以便使用jsonpath来解析
                return r.json()
            return None
        except requests.exceptions.ConnectionError:
            print('连接错误')

    def parse_data(self, content):
        names = jsonpath.jsonpath(content, '$..name')
        alias = jsonpath.jsonpath(content, '$..alias')
        categories = jsonpath.jsonpath(content, '$..categories')
        covers = jsonpath.jsonpath(content, '$..cover')
        published_at = jsonpath.jsonpath(content, '$..published_at')
        minutes = jsonpath.jsonpath(content, '$..minute')
        regions = jsonpath.jsonpath(content, '$..regions')
        dramas = jsonpath.jsonpath(content, '$..drama')
        scores = jsonpath.jsonpath(content, '$..score')
        data = []
        for value in zip(
                names,
                alias,
                categories,
                covers,
                published_at,
                minutes,
                regions,
                dramas,
                scores):
            name, alia, category, cover, published_at, minute, region, drama, score = value
            item = {
                "name": name,
                "alia": alia,
                'categorie': category,
                'cover': cover,
                'published_at': published_at,
                'minute': minute,
                'region': region,
                'drama': drama,
                'score': score
            }
            data.append(item)
        time.sleep(1)

        # for value in zip(names,alias):
        #     names, alias= value
        #     item = {
        #             "names":names,
        #             "alias":alias,
        #
        #        }
        return data

    def save_mongo(self, data):
        client = MongoClient(self.client)
        db = client[self.db]
        col = db[self.col]
        # 做到即插及更新
        # col.update_one({'name': data.get('name')}, {
        #     "$set": data}, upsert=True)
        col.insert_many(data)

    def main(self):
        for page in range(1, 101):
            # url = f'https://spa1.scrape.center/api/movie/?limit=10&offset={page*10}'
            url = f'https://spa1.scrape.center/api/movie/{page}/'
            data = self.get_page(url)
            content = self.parse_data(data)
            self.save_mongo(content)


if __name__ == '__main__':
    response = Crawler()
    response.main()

