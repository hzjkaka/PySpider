'''
爬取博客园的代码：此网站已加入了反爬，该代码已无法在爬取
后续会使用新的方法来爬取

'''
import multiprocessing
import random
import time
import requests
from lxml import etree
from fake_useragent import UserAgent
# 实例化 user-agent 对象
ua = UserAgent()
# 随机浏览器 user-agent
HEADERS = {
    'cookie': '_ga=GA1.2.789692814.1575245968; _gid=GA1.2.90574348.1575245968; __gads=ID=d0b3d037d343ea7f:T=1575246122:S=ALNI_MYb3-Nqsf59wLf_5kAyYqYllV7EFA; _gat=1; .Cnblogs.AspNetCore.Cookies=CfDJ8DeHXSeUWr9KtnvAGu7_dX-Wfut1-dgX_yW1t_fPBSG6ejwby5on7dPqagwvw_WdjyzxkSv4BwoUWPbClu4VNcySbHU5xW1f4vpuOB4NET3TigRH9T3mlgNwIWy7oqLFygXjQxNj2gkFzpDx7Yq8T7HJOmxg30lx50dN4ssnGTWVCTppMnHJT1NyfQs58HorucZThRwEjTxDMdcAI_VoGbd-EmMOUT9h-fLvnQ_hn4b8lQ9evYMG4n9nmmArBnhf3wNo-RKb7TgMCx6QUWWIbYXp2M2TjzG3uzbO3rnEljkTL1cVEB6My97ZQfjLRe27RbArxp4wltsXi4WkBcNTQAXyI2SpiFZYCcBZTxT_uC-Z5Phphjs-sl1_iu7sIR-8m0qysad-BuKdS6Qwvj5qlJt1JCJbi_WFH6Dzs_rgJvn0DfPQE50sAlHOs6Dhgqc7N-YDVqpSphJDRlRkIM6JBH8Pq6EZ8S0IRbZsdkIqiJ54CD-H5G5Hx9oATlEakAqDnWyZ4LlBVyu1wkne48R5usxkmITyZ1PDWwHC5pKRKxfelXDoR05REO4GDOXhXxG5XEZeYA1rWdJI7AKnIM5RM9Y; .CNBlogsCookie=E4793F450C4325E3C9EF21B78B1DE43F6258C9FD5951338859D96A5EC8795064AB518501755136F3A4CB1CE647EBD2CC352C1E9EBDC6E460B6320E9F62F083A52A635A4651A3D1082631D55FCE58E283B97D016E61DC411E094F6EA9A9CF9A59A292C16F',
    'user-agent': ua.random,
    'Host': 'www.cnblogs.com',
    'Connection': 'keep-alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9'}
# 随机时间间隔
TIME = random.randint(1, 3)
BASIC_URL = 'https://zzk.cnblogs.com'
KEYWORD = 'python'
TOTAL_PAGE = 4


class CnblogSpider():
    def __init__(self):
        self.headers = HEADERS
    # 发送请求和获取响应

    def get_page(self, url):
        response = requests.get(url, headers=self.headers)
        time.sleep(TIME)
        try:
            if response.status_code == 200:
                # print(response.text)
                return response.text
            return None
        except requests.exceptions.ConnectionError as e:
            print(e.args)

    def get_index(self, page):
        index_url = self.url = f'{BASIC_URL}/s/blogpost?Keywords={KEYWORD}&pageindex={page}'
        return self.get_page(index_url)

    # 定义列表页的爬取方法
    def parse_index(self, html):
        data = etree.HTML(html)
        # 使用xpath找的详情页的跳转url
        nodes = data.xpath('//*[@id="searchResult"]/div/div')
        for node in nodes:
            title = node.xpath('./h3/a/text()')
            drama = node.xpath('./span/text()')
            username = node.xpath('./div[1]/span[1]/text()')
            publish_date = node.xpath('./div[1]/span[2]/text()')
            good = node.xpath('./div[1]/span[3]/text()')
            comments = node.xpath('./div[1]/span[4]/text()')
            views = node.xpath('./div[1]/span[5]/text()')
            relate_blog = node.xpath('./span[6]/a/@href')
            detail_url = node.xpath('./div[2]/span[1]/text()')

            return {
                'title': title,
                'drama': drama,
                'username': username,
                'publish_date': publish_date,
                'good': good,
                'comments': comments,
                'views': views,
                'relate_blog': relate_blog,
                'detail_url': detail_url
            }

    # 请求详情页
    # def get_detail(self,url):
    #     return self.get_page(url)

    # # 解析详情页
    # def parse_detail(self,html):
    #     data = etree.HTML(html)
    #     cover = data('img.cover').attr('src')
    #     name = data('.m-b-sm').text()
    #     categories = [item.text() for item in data('.categories button span').items()]
    #     date = data('.info:contains(上映)').text().strip('上映')
    #     # date = re.search(r'(\d{4}-\d{2}-\d{2})', date).group(1) \
    #     #     if date and re.search(r'\d{4}-\d{2}-\d{2}', date) else None
    #     score = data('p.score').text()
    #     score = float(score) if score else None
    #     drama = data('.drama p').text()
    #     return {
    #         'cover': cover,
    #         'name': name,
    #         'categories': categories,
    #         'published_at': date,
    #         'score': score,
    #         'drama': drama
    #     }
    # def save_data(self,data):
    #     clinet = pymongo.MongoClient(MONGO_CONNECTION)
    #     db = clinet[MONGO_DB_NAME]
    #     col = db[MONGO_COLLECTION_NAME]
    #     #做到即插及更新
    #     col.update_one({'name':data.get('name')},{
    #         "$set": data }, upsert=True)

    def main(self):
        for page in range(1, TOTAL_PAGE + 1):
            index_html = self.get_index(page)
            data = self.parse_index(index_html)
            print(data)
            time.sleep(TIME)
            # detail_urls = self.detail_url(index_html)
            # for detail_url in detail_urls:
            #     html = self.get_detail(detail_url)
            #     data = self.parse_detail(html)
            # self.save_data(data)


if __name__ == '__main__':
    response = CnblogSpider()
    pool = multiprocessing.Pool()
    pages = range(1, TOTAL_PAGE + 1)
    pool.map(response.main(), pages)
    pool.close()
    pool.join()
