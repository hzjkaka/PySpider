# -*- coding: utf-8 -*-
"""
@File    : 2.spa6.py
@Time    : 2020/8/28 
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
#JS混淆的案例
'''
这个 token 的构造逻辑如下：
传入的 /api/movie 会构造一个初始化列表，变量命名为 _0x3dde76。
获取当前的时间戳，命名为 _0x4c50b4，push 到 _0x3dde76 这个变量里面。
将 _0x3dde76 变量用“,”拼接，然后进行 SHA1 编码，命名为 _0x46ba68。
将 _0x46ba68 （SHA1 编码的结果）和 _0x4c50b4 （时间戳）用逗号拼接，命名为 _0x495a44。
将 _0x495a44 进行 Base64 编码，命名为 _0x2a93f2，得到最后的 token。
基本的思路就是：
先将 /api/movie 放到一个列表里面；
列表中加入当前时间戳；
将列表内容用逗号拼接；
将拼接的结果进行 SHA1 编码；
将编码的结果和时间戳再次拼接；
将拼接后的结果进行 Base64 编码
'''

import hashlib
import time
import base64
import requests
import jsonpath

INDEX_URL = 'https://dynamic6.scrape.cuiqingcai.com/api/movie?limit={limit}&offset={offset}&token={token}'
LIMIT = 10
OFFSET = 0

def get_token(args):
    timestamp = str(int(time.time()))
    args.append(timestamp)
    sign = hashlib.sha1(','.join(args).encode('utf-8')).hexdigest()
    token = base64.b64encode(','.join([sign, timestamp]).encode('utf-8')).decode('utf-8')
    return token
args = ['/api/movie']
token = get_token(args=args)
print(token)
index_url = INDEX_URL.format(limit=LIMIT, offset=OFFSET, token=token)
response = requests.get(index_url)
content = response.json()
names = jsonpath.jsonpath(content, '$..name')
alias = jsonpath.jsonpath(content, '$..alias')
categories = jsonpath.jsonpath(content, '$..categories')
covers = jsonpath.jsonpath(content, '$..cover')
published_at = jsonpath.jsonpath(content, '$..published_at')
minutes = jsonpath.jsonpath(content, '$..minute')
regions = jsonpath.jsonpath(content, '$..regions')
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
        scores):
    name, alia, category, cover, published_at, minute, region, score = value
    item = {
        "name": name,
        "alia": alia,
        'categorie': category,
        'cover': cover,
        'published_at': published_at,
        'minute': minute,
        'region': region,
        'score': score
    }
    data.append(item)
print(data)
#其中没有js混淆的
'''
function i() {
            for (var t = Math.round((new Date).getTime() / 1e3).toString(), e = arguments.length, r = new Array(e), i = 0; i < e; i++)
                r[i] = arguments[i];
            r.push(t);
            var o = n.SHA1(r.join(",")).toString(n.enc.Hex)
              , c = n.enc.Base64.stringify(n.enc.Utf8.parse([o, t].join(",")));
            return c
        }
        e["
'''