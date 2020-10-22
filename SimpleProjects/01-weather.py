import random
import requests
from lxml import etree
from fake_useragent import UserAgent
# 实例化 user-agent 对象
ua = UserAgent()
HEADERS = {"user-agent": ua.chrome}  # 指定浏览器 user-agent
TIME_OUT = random.randint(1, 3)


class Spider(object):
    def __init__(self):
        self.url = 'http://tianqi.sogou.com/pc/weather/56923'
        self.time_out = TIME_OUT
        self.header = HEADERS

    def get_url(self):
        try:
            r = requests.get(
                self.url,
                headers=self.header,
                timeout=self.time_out)
            if r.status_code == 200:
                return r.text
            return None
        except requests.exceptions.ConnectionError as e:
            print(e.args)

    def get_weather(self,r):
        html = etree.HTML(r)
        location = html.xpath('//div/a/em/text()')[0]
        today = html.xpath("//a[@class ='date']/text()")[0].strip()

        weather = html.xpath('//span[@class="num"]/text()')[0]
        weather2 = html.xpath(
            "//div[@class='r1-img']/p[@class='text']/text()")[0]
        wind = html.xpath("//span[@class='wind']/text()")[1].strip()
        shidu = html.xpath("//p/span[@class='hundity']/text()")[1].strip()
        quality = html.xpath('//p[2]/span/a/em/text()')[0]
        rank = html.xpath(
            "//p[2]/span/a/span[@class='liv-img liv-img-cor1']/text()")[0]
        content = f'早上好！\n这是今日份的{location}天气！\n今天是：' + today + '\n当前温度：' + weather + \
            '度  ' + weather2 + '\n风级：' + wind + '\n湿度:' + shidu + '\n空气质量指数:' + quality + ' 等级：' + rank
        return content

if __name__ == '__main__':
    response = Spider()
    r =response.get_url()
    content = response.get_weather(r)
    print(content)
