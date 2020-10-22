# -*- coding: utf-8 -*-
"""
@File    : doushi.py
@Time    : 2020/8/24
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
import csv
import json

import requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0.1; MuMu Build/V417IR; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36',
    'Cookie': 'duid=65718909',
    'Host': 'api.douguo.net',
    'uuid': '18383b68-572e-4ed4-a98b-c5db03609889',
    'language': 'zh'
}
data = {
    'client': 4,
    '_session': 1598255199711010000000249720,
    'keyword': '下饭菜',
    '_vs': 203,
    'sign_ran': '1fd67624ec86a659c048a3c7d0543d3b',
    'code': 'e9c78af42010f772'
}


def get_page(url):
    response = requests.post(url=url, headers=headers, data=data, verify=False)
    try:
        if response.status_code == 200:
            return response.json()
        return None
    except BaseException:
        print('请求错误！')


def parse_data(response):

    content = []
    for recipe in response['result']['recipes']:
        print(recipe)
        item = {}
        item['id'] = recipe['id']
        item['菜名'] = recipe['n']
        item['简介'] = recipe['cookstory']
        item['制作流程'] = recipe['tips']
        item['制作时间'] = recipe['cook_time']
        item['难度'] = recipe['cook_difficulty']
        content.append(item)
    return content


def save_data(data):
    with open('doushi.txt', 'a+', encoding='utf-8') as f:
        f.write(str(data))
        f.write('\n' + '*' * 40 + '\n')


def main():
    for page in range(0, 5):
        # if page == 0:
        #     url = 'https://api.douguo.net/search/universalnew/0/10'
        #     data = get_page(url)
        #     datas = parse_data(data)
        #     for data in datas:
        #         save_data(data)
        url = f'https://api.douguo.net/recipe/moresearch/{page*10+9}/10'
        data = get_page(url)
        datas = parse_data(data)
        for data in datas:
            save_data(data)


if __name__ == '__main__':
    main()
