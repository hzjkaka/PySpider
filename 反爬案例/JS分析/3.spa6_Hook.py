# -*- coding: utf-8 -*-
"""
@File    : 3.spa6_Hook.py
@Time    : 2020/8/28
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
'''
 var _0x1ade76 = 'ef34#teuq0btua#(-57w1q5o5--j@98xygimlyfxs*-!i-0-mb'
          , _0x514589 = _0x5642e3('27ae')['Base64'];
        function _0x2c5adb(_0x349906) {
            var _0x2880ec = _0x1ade76 + _0x349906['toString']();
            return _0x514589['encode'](_0x2880ec);
        }
'''
# Hook 技术中文又叫作钩子技术，它就是在程序运行的过程中，对其中的某个方法进行重写，
# 在原有的方法前后加入我们自定义的代码。相当于在系统没有调用该函数之前，钩子程序就先捕获该消息，
# 可以先得到控制权，这时钩子函数便可以加工处理（改变）该函数的执行行为。

import hashlib
import time
import base64
from typing import List, Any
import requests
import jsonpath
INDEX_URL = 'https://dynamic6.scrape.cuiqingcai.com/api/movie?limit={limit}&offset={offset}&token={token}'
DETAIL_URL = 'https://dynamic6.scrape.cuiqingcai.com/api/movie/{id}?token={token}'
LIMIT = 10
OFFSET = 0
SECRET = 'ef34#teuq0btua#(-57w1q5o5--j@98xygimlyfxs*-!i-0-mb'

def get_token(args: List[Any]):
    timestamp = str(int(time.time()))
    args.append(timestamp)
    sign = hashlib.sha1(','.join(args).encode('utf-8')).hexdigest()
    return base64.b64encode(
        ','.join([sign, timestamp]).encode('utf-8')).decode('utf-8')

args = ['/api/movie']
token = get_token(args=args)
index_url = INDEX_URL.format(limit=LIMIT, offset=OFFSET, token=token)
response = requests.get(index_url)
# print('response', response.json())

result = response.json()
# id = jsonpath.jsonpath(result,'$..id')
# print(id)
for item in result['results']:
    id = item['id']
    encrypt_id = base64.b64encode(
        (SECRET + str(id)).encode('utf-8')).decode('utf-8')
    args = [f'/api/movie/{encrypt_id}']
    token = get_token(args=args)
    detail_url = DETAIL_URL.format(id=encrypt_id, token=token)
    response = requests.get(detail_url)
    print('response', response.json())
