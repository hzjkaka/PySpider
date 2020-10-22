import time

import requests
from lxml import etree
import random
from fake_useragent import UserAgent
ua = UserAgent()
# 最常用的方式
# 写爬虫最实用的是可以随意变换headers，一定要有随机性。支持随机生成请求头
HEADERS = {"User-Agent": ua.random}  # 指定浏览器 User-Agent
TIME = random.randint(2, 3)
# proxies = {
#     # 'http': 'http://' + ip,
#       'https': 'https://' + '106.14.3.97:8888'
# }
BASIC_URl = 'http://tieba.baidu.com'
# 随机IP获取
PROXY_POOL_URL = 'http://localhost:5555/random'
def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL)

        if response.status_code == 200:
            return response.text
    except ConnectionError:
        return None
ip = get_proxy()
print(ip)


class TieBa(object):
    # 初始化数据
    def __init__(self, keyword):
        self.url = 'https://tieba.baidu.com/f?kw={}&ie=utf-8'.format(keyword)
        self.headers = HEADERS
        self.proxies ={'https': 'https://' + ip}
        print(self.proxies)

    # 发送请求和获取响应
    def get_page(self, next_url):
        response = requests.get(
            url=self.url,
            headers=self.headers,
            proxies =self.proxies
            )
        try:
            if response.status_code == 200:
                time.sleep(TIME)
                return response.content
            return None
        except requests.exceptions.ConnectionError as e:
            print(e.args)

    def get_data(self, html):
        html = html.decode().replace("<!--", "").replace("-->", "")
        data = etree.HTML(html)
        # 找的主题的分组
        node_list = data.xpath(
            '//*[@id="thread_list"]/li[@class=" j_thread_list clearfix"]/div/div[2]/div[1]/div[1]/a')
        # print(node_list)
        data_list = []
        for node in node_list:
            item = {}
            item['Title'] = node.xpath('./text()')[0]
            item['Link'] = BASIC_URl + node.xpath('./@href')[0]
            data_list.append(item)
        # 翻页操作
        try:
            next_url = 'https:'+data.xpath('//*[@id="frs_list_pager"]/a[contains(text(),"下一页>")]/@href')[0]
            print(next_url)
        except BaseException:
            next_url = None
        return data_list, next_url

    def save_data(self, content):
        with open("03-baidutieba.txt", 'a+', encoding='utf-8') as f:
            f.write('\n' + str(content))
            f.write('\n' + '*' * 10 + '\n')

    def main(self):
        next_url = self.url
        while True:
            data = self.get_page(next_url)
            data_list, next_url = self.get_data(data)
            # print(data_list)
            self.save_data(data_list)
            if next_url == None:
                break


if __name__ == '__main__':
    keyword = 'C罗'
    response = TieBa(keyword)
    response.main()
    time.sleep(TIME)
