"""
'@File    ':'comment.py',
'@Time    ':'2020/9/25 ',
'@Author  ':'Hzj',
'@Email   ':'hzjkaka@163.com',
'@IDE':'PyCharm',
"""
import csv

import requests
from lxml import etree
import time
from fake_useragent import UserAgent
import re
import chardet
import random


# 实例化 User-Agent 对象
ua = UserAgent()
# 随机浏览器 User-Agent
HEADERS = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
# 'Accept-Encoding':'gzip, deflate, br',
# 'Accept-Language':'zh-CN,zh;q=0.9',
'Cache-Control':'max-age=0',
'Connection':'keep-alive',
'Cookie':'douban-fav-remind=1; ll="118200"; trc_cookie_storage=taboola%2520global%253Auser-id%3D59ae9979-e3fa-4204-95fe-6b0caf35a8e8-tuct47bcd99; __yadk_uid=4mggz6tiKdckEXmx4d6V2dKZrOlaEIC6; _vwo_uuid_v2=DB9EE4818364265FE94A87F1BDA64E692|3d65e19e2ec2dd2a63d40eb619286f7b; __gads=ID=fc82a40358d820e0:T=1583244518:S=ALNI_MZsLRMrhnJcd0OEW8jUalvtK4U4aQ; gr_user_id=b7c07aee-68bd-431e-b357-f9ce3988ab1e; viewed="27061630_34938311"; bid=4vB2w_-iIu4; dbcl2="184472382:lEjaOvsLkRs"; push_doumail_num=0; push_noty_num=0; __utmv=30149280.18447; ck=jVVU; ap_v=0,6.0; __utmc=30149280; __utmt=1; __utmc=223695111; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1601075588%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=30149280.15751317.1572437547.1601075580.1601075615.23; __utmb=30149280.0.10.1601075615; __utmz=30149280.1601075615.23.16.utmcsr=sogou|utmccn=(organic)|utmcmd=organic|utmctr=%E5%85%AB%E4%BD%B0; __utma=223695111.556213055.1572437547.1601075588.1601075615.22; __utmb=223695111.0.10.1601075615; __utmz=223695111.1601075615.22.17.utmcsr=sogou|utmccn=(organic)|utmcmd=organic|utmctr=%E5%85%AB%E4%BD%B0; _pk_id.100001.4cf6=b59833735216f326.1572437547.15.1601075621.1601019485.',
'Host':'movie.douban.com',
'Referer':'https://movie.douban.com/subject/26754233/',
'Sec-Fetch-Dest':'document',
'Sec-Fetch-Mode':'navigate',
'Sec-Fetch-Site':'same-origin',
'Sec-Fetch-User':'?1',
'Upgrade-Insecure-Requests':'1',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',

}

TIME = random.randint(1, 3)
url = 'https://movie.douban.com/subject/26754233/reviews?start=%d'
# PROXY_POOL_URL = 'http://localhost:5555/random'
# ID = '4551208402421931'
# MID = '4551208402421931'
# class  DoubanSpider():
#     def __init__(self):
#         self.url = f'{BASIC_URl}/comments/hotflow?id={ID}&mid={MID}'
#         self.headers = HEADERS

if __name__ == '__main__':
    # data = []
    fp  = open('babai2.csv','w',encoding='utf-8')
    fp.write('name\trating\tdate\ttitle\tup_vote\tdown_vote\n')
    for i in range(20):
        if i==100:
            _url = url%(200)
        else:
            _url = url%(i*20)
        response = requests.get(_url,headers=HEADERS)
        response.encoding = 'utf-8'
            # chardet.detect(response.content)['encoding']
        text = response.text
        # print(text)
        html = etree.HTML(text)
        comments =html.xpath('//div[@class ="review-list  "]//div[@class="main review-item"]')
        print(len(comments))
        for comment in comments:
            name = comment.xpath('./header/a[2]/text()')[0].strip()
            rating = comment.xpath('./header/span[1]/@title')
            date = comment.xpath('./header/span[2]/text()')
            title = comment.xpath('./div[@class="main-bd"]/h2/a/text()')[0].strip()
            # review = comment.xpath('./div[@class="main-bd"]//div[@class="short-content"]/text()')[0].strip()
            up_vote = comment.xpath('./div[@class="main-bd"]/div[@class="action"]/a[1]/span/text()')[0].strip()
            down_vote = comment.xpath('./div[@class="main-bd"]/div[@class="action"]/a[2]/span/text()')[0].strip()
            if rating or date:
                # print('%s %s %s %s %s %s'%(name,rating[0],date[0],title,up_vote,down_vote))

                # content = (name,rating[0],date[0],title,up_vote,down_vote)
                # data.append(content)
                fp.write(('%s\t%s\t%s\t%s\t%s\t%s\n'%(name,rating[0],date[0],title,up_vote,down_vote)))
        print('第%d页数据保存成功' % (i + 1))
        time.sleep(TIME)
    fp.close()
    # headers = ['name','rating','date','title','up_vote','down_vote']
    # with open('babai.csv','w',encoding='utf-8') as f:
    #     f_csv = csv.writer(f,)
    #     f_csv.writerow(headers)
    #     f_csv.writerows(data)







