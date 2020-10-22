# -*- coding: utf-8 -*-
"""
@File    : gushiwen.py
@Time    : 2020/8/15 
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
import requests
import re
import chardet
from fake_useragent import UserAgent
ua = UserAgent()
HEADERS = {"User-Agent": ua.random}  # 指定浏览器 User-Agent
def get_page(url):
    response = requests.get(url, headers=HEADERS)
    try:
        if response.status_code == 200:
            response.encoding = chardet.detect(response.content)['encoding']
            return response.text
        return None
    except requests.exceptions.ConnectionError as e:
        print(e.args)

def parse_page(content):
    titles = re.findall(r'<div class="cont".*?<b>(.*?)</b>',content,re.DOTALL)
    dynasties = re.findall(r'<p class="source".*?<a.*?>(.*?)</a>',content)
    authors = re.findall(r'<p class="source".*?<a.*?>.*?<a.*?>(.*?)</a>',content,re.S)
    contents = re.findall(r'<div class="contson".*?>(.*?)</div>',content,re.S)
    poetry_texts =[]
    for data in contents:
        poetry_texts.append(re.sub(r'[<br />\ue310</p><p>]','',data).strip())
        # replace('<br />','').replace('\ue310','').replace('</p>','').replace('<p>','').strip())

    poetries = []
    for value in zip(titles,dynasties,authors,poetry_texts):
        title,dynastie,author,poetry_text = value
        poetry ={
            '标题':title,
            '朝代':dynastie,
            '作者':author,
            '诗文':poetry_text
        }
        poetries.append(poetry)
    # 多个返回值时：一定记住写返回值不然报错：'NoneType' object is not iterable
    return poetries
    # for poetry in poetries:
    #     print(poetry)
    #     print("="*40)

def save_data(poetries):
    for poetry in poetries:
        with open('gushiwen.txt', 'a+', encoding='utf-8') as f:
            f.write('\n'+str(poetry)+'\n'+'*'*40)
            # f.writelines('\n')

def main():
    for page in range(1,6):
        url = f'https://www.gushiwen.cn/default_{page}.aspx'
        content = get_page(url)
        datas =parse_page(content)
        save_data(datas)


if __name__ == '__main__':
    main()