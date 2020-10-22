import time
from urllib.parse import urljoin
import pymongo
import requests
import random
from  pyquery import PyQuery as pq
from fake_useragent import UserAgent
import multiprocessing
#随机化请求头和请求IP
# 最常用的方式
# 写爬虫最实用的是可以随意变换headers，一定要有随机性。支持随机生成请求头
ua = UserAgent()
HEADERS = {"User-Agent": ua.random}  # 指定浏览器 User-Agent
TIME = random.randint(1,3)
BASIC_URl = 'https://static1.scrape.cuiqingcai.com'
# PROXY_POOL_URL = 'http://localhost:5555/random'
TOTAL_PAGE = 10

# 数据库存储
MONGO_CONNECTION = 'mongodb://localhost:27017/'
MONGO_DB_NAME = 'Scrape'
MONGO_COLLECTION_NAME = 'movies1'

#设计爬虫类
class StaticScrpae(object):
    # 初始化数据
    def __init__(self):
        self.headers = HEADERS
        # self.timeout = TIME_OUT
    # 发送请求和获取响应
    def get_page(self,url):
        response = requests.get(
            url,
            headers=self.headers)
        try:
            if response.status_code == 200:
                return response.content
            return None
        except requests.exceptions.ConnectionError as e:
            print(e.args)

    #定义列表页的爬取方法
    def get_index(self,page):
        index_url = f'{BASIC_URl}/page/{page}'
        return self.get_page(index_url)

    #定义详情页的url爬取方法
    def detail_url(self,html):
        data = pq(html)
        # 使用css找的详情页的跳转url
        links = data('.el-card .name')
        for link in links.items():
            href =link.attr.href
            detail_url = urljoin(BASIC_URl,href)
            yield detail_url

    # 请求详情页
    def get_detail(self,url):
        return self.get_page(url)

    # 解析详情页
    def parse_detail(self,html):
        data = pq(html)
        cover = data('img.cover').attr('src')
        name = data('.m-b-sm').text()
        categories = [item.text() for item in data('.categories button span').items()]
        date = data('.info:contains(上映)').text().strip('上映')
        # date = re.search(r'(\d{4}-\d{2}-\d{2})', date).group(1) \
        #     if date and re.search(r'\d{4}-\d{2}-\d{2}', date) else None
        score = data('p.score').text()
        score = float(score) if score else None
        drama = data('.drama p').text()
        return {
            'cover': cover,
            'name': name,
            'categories': categories,
            'published_at': date,
            'score': score,
            'drama': drama
        }
    def save_data(self,data):
        client = pymongo.MongoClient(MONGO_CONNECTION)
        db = client[MONGO_DB_NAME]
        col = db[MONGO_COLLECTION_NAME]
        #做到即插及更新
        col.update_one({'name':data.get('name')},{
            "$set": data }, upsert=True)

    def main(self):
        for  page in range(1,TOTAL_PAGE+1):
            index_html = self.get_index(page)
            detail_urls = self.detail_url(index_html)
            for detail_url in detail_urls:
                html = self.get_detail(detail_url)
                data = self.parse_detail(html)
                self.save_data(data)


if __name__ == '__main__':
    response = StaticScrpae()
    pool = multiprocessing.Pool()
    pages = range(1,TOTAL_PAGE+1)
    pool.map(response.main(),pages)
    pool.close()
    pool.join()
    time.sleep(TIME)
