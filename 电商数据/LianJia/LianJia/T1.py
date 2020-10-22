# -*- coding: utf-8 -*-
"""
@File    : T1.py
@Time    : 2020/9/2 
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""

# url = [f'https://sh.lianjia.com/zufang/pg{i}/' for i in range(1,10)]
# print(url)
# from fake_useragent import UserAgent
# import requests
# import time
# from lxml import etree
# headers = UserAgent().random
# res = requests.get(url ='https://sh.lianjia.com/zufang/')
# html = res.text
# # print(res.text)
# data = etree.HTML(html)
# location = data.xpath('//p[@class="content__list--item--des"]/a//text()')[:3]
# print(location)

location2 = ['徐汇', '上海南站', '汇成二村', '黄浦', '新天地', '梅兰坊', '徐汇', '长桥', '长桥一村', '徐汇', '康健', '杜鹃园', '长宁', '仙霞', '威宁大楼', '徐汇', '田林', '田林十三村', '长宁', '北新泾', '虹园八村', '徐汇', '康健', '康乐小区(徐汇)', '黄浦', '董家渡', '陆家浜路413弄', '黄浦', '蓬莱公园', '西凌新邨', '闵行', '吴泾', '永德小区', '浦东', '杨思前滩', '杨新路80弄', '浦东', '世博', '济阳三村', '浦东', '世博', '上南四村', '长宁', '北新泾', '新泾一村', '静安', '江宁路', '昌平路427-439号(单)', '浦东', '世博', '上钢六村', '浦东', '世博', '济阳一村', '徐汇', '田林', '钦州花苑']
results = []
i=0
# result = '-'.join(location2[i:i+3:])
for i in range(0,len(location2),3):
    b = '-'.join(location2[i:i+3])
    results.append(b)

# for i in range(0,10,2):
#
#     print(i)
# step = 3
# b = [location2[i:i+step] for i in range(0,len(location2),step)]
# print(b)
# for j in b:
#     print(j)

print(results)
# html ="
# 房山
# 长阳
# 绿地启航社
# 顺义
# 顺义城
# 仓上小区
# 东城
# 朝阳门内
# 禄米仓东巷
# 顺义
# 顺义城
# 滨河小区
# 丰台
# 五里店
# 五里店南里
# 顺义
# 马坡
# 佳和宜园
# 顺义
# 顺义城
# 石园北区
# 顺义
# 顺义城
# 滨河小区
# 房山
# 长阳
# 合景领峰10号院
# 顺义
# 顺义城
# 石园东区
# 通州
# 玉桥
# 玉桥南里
# 顺义
# 顺义城
# 石园东区
# 通州
# 万达
# 东营前街
# 大兴
# 大兴新机场
# 众美MIMO公馆
# 通州
# 北关
# 西潞苑小区
# 房山
# 良乡
# 黄辛庄东里
# 顺义
# 顺义城
# 建新南区
# 顺义
# 顺义城
# 滨河小区
# 通州
# 武夷花园
# 玉桥中路2号院
# 顺义
# 马坡
# 佳和宜园
# 通州
# 梨园
# 梨园东里
# 顺义
# 顺义城
# 滨河小区
# 顺义
# 顺义城
# 滨河小区
# 顺义
# 顺义城
# 滨河小区
# 顺义
# 顺义城
# 石园南区
# 顺义
# 顺义城
# 滨河小区
# 顺义
# 顺义城
# 滨河小区
# 房山
# 长阳
# 合景领峰10号院
# 昌平
# 昌平其它
# 沙河地质研究院家属楼
# 大兴
# 西红门
# 红华住宅区 "

