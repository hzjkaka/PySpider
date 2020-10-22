# -*- coding: utf-8 -*-
"""
@File    : hash.py
@Time    : 2020/8/25 
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
import hashlib

data='python'
#创建hash对象
r = hashlib.md5()
#向hash对象添加需要做的hash运算的字符串
r.update(data.encode())#必须是bytes类型
#16进制
print(r.hexdigest())