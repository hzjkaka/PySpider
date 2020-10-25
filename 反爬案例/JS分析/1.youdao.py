# -*- coding: utf-8 -*-
"""
@File    : 1.youdao.py
@Time    : 2020/8/25 
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""

import requests
import hashlib
import time
import random
from fake_useragent import UserAgent
import jsonpath
class YdaoSpider(object):
    def __init__(self,word):
        self.url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
  
        self.headers={'User-Agent':UserAgent().random,
                     'Referer':'http://fanyi.youdao.com/',
                     'Origin': 'http://fanyi.youdao.com',
                     'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
                     'X-Requested-With':'XMLHttpRequest',
                     'Accept':'application/json, text/javascript, */*; q=0.01',
                     'Accept-Encoding':'gzip, deflate',
                     'Accept-Language':'zh-CN,zh;q=0.9',
                     'Connection': 'keep-alive',
                     'Host': 'fanyi.youdao.com',
                     'cookie':'_ntes_nnid=937f1c788f1e087cf91d616319dc536a,1564395185984; OUTFOX_SEARCH_USER_ID_NCOO=; OUTFOX_SEARCH_USER_ID=-10218418@11.136.67.24; JSESSIONID=; ___rl__test__cookies=1'
 }
        self.word = word
        self.formdata = None

    def get_form(self):
        '''
               表单数据对应的js代码：
               ts: r= "" + (new Date).getTime(),
               salt: ts + parseInt(10 * Math.random(), 10),
               sign: n.md5("fanyideskweb" + e + salt + "]BjuETDhU)zqSxf-=B#7m")
               '''
        # 改写成python代码
        ts = str(int(time.time() * 1000))  # 字符串类型的时间戳
        salt = ts + str(random.randint(0,9))
        tempstr = "fanyideskweb" + self.word + salt + "]BjuETDhU)zqSxf-=B#7m"
        md5 = hashlib.md5()
        md5.update(tempstr.encode())
        sign = md5.hexdigest()
        self.formdata ={
            'i': self.word,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict', #紧记是个''号 不然和python内置关键字冲突报 'type' object is not iterable 错误
            'client': 'fanyideskweb',
            'salt': salt,
            'sign': sign,
            'ts': ts,
            'bv': '7e14dfdb6b3686cc5af5e5294aaded19',
            'doctype': 'json',
            'version': '2.1',
           'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CLICKBUTTION',
        }

    def get_data(self):
        # print(self.formdata)
        s = requests.session()
        response = s.post(self.url,data=self.formdata,headers=self.headers)
        return response.json()

    def main(self):
        self.get_form()
        data =self.get_data()
        # JsonPath是一种信息抽取类库，是从JSON文档中抽取指定信息的工具，提供多种原因实现保本：JavaScript / Python / PHP和Java。
        # 使用方法如：
        # res = jsonpath.jsonpath(dic_name, '$..key_name')
        # 嵌套n层也能取到所有key_name信息,其中：“$”表示最外层的{}，“..”表示模糊匹配,当传入不存在的key_name时,程序会返回false
        result= jsonpath.jsonpath(data, '$..tgt')[0]
        # print(data['translateResult'][0][0]['tgt'])
        print(result)

if __name__ == '__main__':
    input = input("请输入翻译内容:")
    ydao = YdaoSpider(input)
    ydao.main()


