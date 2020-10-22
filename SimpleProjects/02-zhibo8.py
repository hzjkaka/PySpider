import csv
# from lxml import etree
import requests
from fake_useragent import UserAgent
# import  json
import random
ua = UserAgent()
HEADERS = {"User-Agent": ua.chrome}  # 指定浏览器 User-Agent
TIME_OUT = random.randint(1, 3)


class Spider(object):
    def __init__(self):
        self.url = 'https://dc.qiumibao.com/shuju/public/index.php?_url=/data/index&league=%E6%84%8F%E7%94%B2&tab=%E7%A7%AF%E5%88%86%E6%A6%9C'
        self.time_out = TIME_OUT
        self.header = HEADERS

    def get_url(self):
        try:
            r = requests.get(self.url,headers=self.header,timeout=self.time_out)
            if r.status_code == 200:
                return r.json()
            return None
        except requests.exceptions.ConnectionError as e:
            print(e.args)
    def get_data(self,content):
        # data = json.loads(content)
        # print(data)
        data_list = []
        for index in content['data']:
            indexs = []
            indexs.append(index['排名'])
            indexs.append(index['球队'])
            indexs.append(index['场次'])
            indexs.append(index['胜'])
            indexs.append(index['平'])
            indexs.append(index['负'])
            indexs.append(index['进/失球'])
            indexs.append(index['净胜球'])
            indexs.append(index['积分'])
            data_list.append(indexs)
        return data_list
    def save_data(self,data):
        with open('zhibo8.csv','a+',encoding='utf-8') as f:
            header = (['排名', '球队', '场次', '胜', '平', '负', '进/失球', '净胜球', '积分'])
            f_csv = csv.writer(f)
            f_csv.writerow(header)
            f_csv.writerows(data)

if __name__ == '__main__':
    response = Spider()
    content = response.get_url()
    data = response.get_data(content)
    response.save_data(data)

    
