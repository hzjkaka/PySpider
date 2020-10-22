'''
豆瓣获取最新的电影排行榜
'''
import random
import time
import requests
from pyquery import PyQuery as pq
from fake_useragent import UserAgent
# 实例化 User-Agent 对象
ua = UserAgent()
# 随机浏览器 User-Agent
HEADERS = {'User-Agent': ua.random}
# print(HEADERS)
#随机时间间隔
TIME = random.randint(1, 3)
BASIC_URl = 'https://movie.douban.com/chart'
PROXY_POOL_URL = 'http://localhost:5555/random'

class  DoubanSpider():
    def __init__(self):
        self.url = f'{BASIC_URl}'
        self.headers = HEADERS
        ip = self.get_proxy()
        print(ip)
        self.proxies = {
            'http': 'http://' + ip,
            'https': 'https://' + ip}

    #  随机IP获取
    def get_proxy(self):
        try:
            response = requests.get(PROXY_POOL_URL)
            if response.status_code == 200:
                return response.text
        except ConnectionError:
            return None

    # 发送请求和获取响应
    def get_page(self):
        response = requests.get(
            url=self.url,
            headers=self.headers,
            proxies=self.proxies
        )
        time.sleep(TIME)
        try:
            if response.status_code == 200:
                # print(response.text)
                return response.text
            return None
        except requests.exceptions.ConnectionError as e:
            print(e.args)

    def parse_data(self,content):
        # 找到分组
        doc = pq(content)
        data = doc(' td:nth-child(2) > div ')
        data_list = []
        for data in data.items():
            item={}
            item["title"] = data('a').text()
            item["drama"] = data('p').text()
            item["score"] = data('div .rating_nums').text()
            data_list.append(item)
        return data_list

    def save_data(self,datalist):
        for i in datalist:
            print(i)

    def main(self):
        content = self.get_page()
        data = self.parse_data(content)
        self.save_data(data)

if __name__ == '__main__':
    response = DoubanSpider()
    response.main()



