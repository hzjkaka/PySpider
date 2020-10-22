# -*- coding: utf-8 -*-
"""
@File    : css1.py
@Time    : 2020/8/30 
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
import requests
import re
from parsel import Selector

url = 'http://www.porters.vip/confusion/flight.html'
resp = requests.get(url)
sel = Selector(resp.text)
em = sel.css('em.rel').extract()
base_price = []
alternate_price = []

for element in em:
    element = Selector(element)
    # 定位所有的b标签
    element_b = element.css('b').extract()
    b1 = Selector(element_b.pop(0))
    # 获取第1对b标签中的值(列表)
    base_price = b1.css('i::text').extract()
    # print(base_price)

    for eb in element_b:
        # ss = len(element_b)
        eb = Selector(eb)
        # 提取b标签的style属性值
        style = eb.css('b::attr("style")').get()
        # 获得具体的位置
        position = ''.join(re.findall('left:(.*)px', style))
        # 获得该标签下的数字
        value = eb.css('b::text').get()
        # 将b标签的位置信息和数字以字典的格式添加到替补票价列表中
        alternate_price.append({'position': position, 'value': value})
    # print(alternate_price)

    for al in alternate_price:
        position = int(al.get('position'))
        # print(position)
        value = al.get('value')
        # 计算下标，以16px为基准
        index = int(position / 16)
        # print(index)
        # 替换第一对b标签值列表中的元素，也就是完成值覆盖操作
        base_price[index] = value
    real_price =base_price

        # print(alternate_price)
    print(real_price)