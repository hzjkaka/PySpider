'''
爬取每天的百度热点排行榜
'''
import time
import requests
import random
from  pyquery import PyQuery as pq
from fake_useragent import UserAgent
#随机化请求头和请求IP
# 最常用的方式
# 写爬虫最实用的是可以随意变换headers，一定要有随机性。支持随机生成请求头
ua = UserAgent()
HEADERS = {"User-Agent": ua.random}  # 指定浏览器 User-Agent
TIME = random.randint(1,3)
BASIC_URl = 'http://top.baidu.com'
TIME_OUT = 30
#设计爬虫类
class BdaiduHot(object):
    # 初始化数据
    def __init__(self):
        self.headers = HEADERS
        self.timeout = TIME_OUT

    # 发送请求和获取响应
    def get_page(self,url):
        response = requests.get(
            url,
            headers=self.headers,
            timeout=self.timeout)
        try:
            if response.status_code == 200:
                return response.content
            return None
        except requests.exceptions.ConnectionError as e:
            print(e.args)

    # 定义列表页的爬取方法
    def get_index(self):
        index_url = f'{BASIC_URl}/buzz?b=341&c=513&fr=topbuzz_b1_c513'
        return self.get_page(index_url)
    #定义列表页的爬取方法
    def parse_data(self,data):
        doc = pq(data)
        topics = doc('tr')
        # data_list = []
        # for topic in topics.items():
        #     item={}
        #     item['排名'] = topic('td.first').text()
        #     item['标题'] = topic('td.keyword > a:nth-child(1)').text()
        #     item['搜索指数'] = topic('td.last').text()
        #     if item['排名'] != None and item['标题'] != None and item['搜索指数'] != None:
        #         data_list.append(item)

        for topic in topics.items():
            rank = topic('td.first').text()
            title = topic('td.keyword > a:nth-child(1)').text()
            num = topic('td.last').text()
            data = "排名：{0:^4}\t标题：{1:^15}\t搜索指数：{2:^8}"
            print(data.format(rank, title, num))
        return data
    
    # def save_data(self,data):


    def run(self):
        data = self.get_index()
        self.parse_data(data)
        # self.save_data(data_list)

if __name__ == '__main__':
    response = BdaiduHot()
    response.run()
    time.sleep(TIME)
        



