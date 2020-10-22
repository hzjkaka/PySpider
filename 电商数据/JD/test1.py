# -*- coding: utf-8 -*-
"""
@File    : test1.py
@Time    : 2020/10/21 
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
# 一般有两种通用做法:
#
# 第一种方法：使用自带函数实现:
# 在python的字典的属性方法里面有一个has_key()方法:

# #生成一个字典
# d = {'name':'Tom', 'age':10, 'Tel':110}
# #打印返回值
# print (d.has_key('name'))
# #结果返回True

#第二种方法：使用in方法:

#生成一个字典
d = {'name':'Tom', 'age':10, 'Tel':110}
#打印返回值，其中d.keys()是列出字典所有的key
print ('name' in d.keys())
print ('name' in d)
#两个的结果都是返回True