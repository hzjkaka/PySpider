# -*- coding: utf-8 -*-
"""
@File    : run2.py
@Time    : 2020/10/20 
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
from scrapy import cmdline
cmdline.execute('scrapy crawl product_spider'.split())