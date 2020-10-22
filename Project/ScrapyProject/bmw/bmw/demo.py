# -*- coding: utf-8 -*-
"""
@File    : demo.py
@Time    : 2020/8/20 
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm

"""
import os
# from urllib.request import urlretrieve
path = 'images'
if not  os.path.exists(path):
    os.mkdir(path)
else:
    print('文件夹已存在！')
category = "类别"
ims_urls =[1,3,4,5,6,7]
category_path = os.path.join(path,category)
if not os.path.exists(category_path):
    os.mkdir(category_path)




