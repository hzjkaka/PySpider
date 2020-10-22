# -*- coding: utf-8 -*-
"""
@File    : weather.py
@Time    : 2020/8/15 
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
"""
爬取中国天气网并分析中国最高气温的排行榜与最低气温排行榜
难点：（1）因爬取港澳台数据的错误，所以替换浏览器的解析器html5lib
     (2) from pyecharts.charts import Bar 不能直接导入Bar
     (3) 使用stripped_strings
"""
import requests
from bs4 import BeautifulSoup as bs
import chardet
from fake_useragent import UserAgent
from pyecharts.charts import Bar
import pyecharts.options as opts
from requests.exceptions import RequestException
ua = UserAgent()
HEADERS = {"User-Agent": ua.random}  # 指定浏览器 User-Agent
ALL_DATA =[]
def get_page(url):
    response = requests.get(url, headers=HEADERS)
    try:
        if response.status_code == 200:
            response.encoding = chardet.detect(response.content)['encoding']
            return response.text
        return None
    except RequestException as e:
        print(e.args)

def parse_data(html):
    # soup = bs(html,'lxml')
    #因爬取港澳台数据的错误，所以替换浏览器的解析器html5lib
    #容错最好的解析方式
    soup = bs(html, 'html5lib')
    conMidtab = soup.find('div',class_='conMidtab')
    tables = conMidtab.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[2:]
        for index,tr in enumerate(trs):
            tds =tr.find_all('td')
            city_td = tds[0]
            if index==0:
                city_td = tds[1]
            # 获取子孙节点的文本并将空白字符删掉，返回一个生成器
            city = list(city_td.stripped_strings)[0]
            temp_td = tds[-2]
            min_temp = list(temp_td.stripped_strings)[0]
            ALL_DATA.append({'城市':city,'温度':int(min_temp)})

def analyze_data(content):
    # 根据最低气温来排序
    ALL_DATA = content
    ALL_DATA.sort(key=lambda data:data['温度'],reverse=True)
    data = ALL_DATA[0:10]

    cities = list(map(lambda i:i['城市'],data))
    temps = list(map(lambda i:i['温度'],data))
    #pyecharts
    chart = Bar()
    chart.add_xaxis(cities)
    # add_yaxis需要传入两个参数，第一个参数为str类型
    chart.add_yaxis('温度', temps)
    chart.set_series_opts(label_opts=opts.LabelOpts(is_show=False),
                            markpoint_opts=opts.MarkPointOpts(
                            data=[
                                opts.MarkPointItem(type_="max", name="最大值"),
                                opts.MarkPointItem(type_="min", name="最小值"),
                                opts.MarkPointItem(type_="average", name="平均值")
                            ]))
    chart.set_global_opts(title_opts=opts.TitleOpts(title='中国气温比较图比较图', pos_left='left'))
    chart.render('中国最高气温排行榜.html')


def main():
    urls = ['http://www.weather.com.cn/textFC/hb.shtml',
           'http://www.weather.com.cn/textFC/db.shtml',
           'http://www.weather.com.cn/textFC/hd.shtml',
           'http://www.weather.com.cn/textFC/hz.shtml',
           'http://www.weather.com.cn/textFC/hn.shtml',
           'http://www.weather.com.cn/textFC/xb.shtml',
           'http://www.weather.com.cn/textFC/xn.shtml',
           'http://www.weather.com.cn/textFC/gat.shtml'
    ]
    for url in urls:
        html = get_page(url)
        data =parse_data(html)
        analyze_data(data)

if __name__ == '__main__':
    main()