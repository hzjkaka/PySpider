# -*- coding: utf-8 -*-

"""
@File    : run1.py
@Time    : 2020/8/17
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
from scrapy import  cmdline
cmdline.execute('scrapy crawl wxapp_spider'.split())