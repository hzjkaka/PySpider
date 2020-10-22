# -*- coding: utf-8 -*-
"""
@File    : by_selenium.py
@Time    : 2020/8/14
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
import time
import pymongo
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from lxml import etree

class JDSpider(object):
    def __init__(self):
        self.option = ChromeOptions()
        self.option.add_experimental_option(
            "excludeSwitches", ["enable-automation"])  # 开启selenium开发者模式
        self.option.add_experimental_option(
            'useAutomationExtension', False)  # 取消chrome受自动控制提示
        self.option.add_argument("--window-size=1900,1080")
        self.driver = webdriver.Chrome(options=self.option)
        self.wait = WebDriverWait(self.driver, 50)

    def search(self, url,keyword):
        # 返回总页数:先模拟打开jd，输入查询的内容，再模拟点击。
        self.driver.get(url)
        # 1. 获取输入框，
        input = self.wait.until(
            # 网页上获取CSS
            EC.presence_of_element_located((By.CSS_SELECTOR, '#key'))
        )
        input.clear()
        input.send_keys(keyword)
        # 2. 获取搜索按钮，实现点击
        button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.button'))
        )
        button.click()
        # 3. 执行js，拖动窗口
        # 为了防止操作过快,页面还未加载出来,先设置睡眠一秒
        time.sleep(1)
        for i in range(16):
            js = 'window.scrollTo(0, {} * document.body.scrollHeight / 16)'.format(i)
            self.driver.execute_script(js)
            time.sleep(0.5)

        # 4. 获取搜素到的关键词查询出的总页数
        total = self.wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#J_bottomPage>span>em>b')))
        # 测试源码中是否有60个商品信息
        html = self.driver.page_source
        data = self.parse_data(html)
        print(data)
        print(len(data))
        self.save_data(data)
        return total.text

    def next_page(self):
        # 获取下一页的内容
        next = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="J_bottomPage"]/span[1]/a[9]')))
        next.click()
        # 滚动
        for i in range(16):
            js = 'window.scrollTo(0, {} * document.body.scrollHeight / 16)'.format(i)
            self.driver.execute_script(js)
            time.sleep(0.5)

        time.sleep(2)
        data = self.driver.page_source
        # print(html)
        data = self.parse_data(data)
        print(data)
        print(len(data))
        self.save_data(data)

    def parse_data(self, html):
        content = etree.HTML(html)
        goods_list = content.xpath('//*[@id="J_goodsList"]/ul/li')
        datas = []
        for goods in goods_list:
            # 获取图片、价格、名称、评论、商店的名称
            data = {
                'name': ' '.join(goods.xpath('.//div[@class="p-name p-name-type-2"]/a/em/text()')),
                'price': ' '.join(goods.xpath('.//div[@class="p-price"]//i/text()')),
                # 如果存在懒加载的话,图片信息会存在于img的data-lazy-img属性中,此处进行判断
                'img': ' '.join(goods.xpath('./div/div[1]/a/img/@src') if goods.xpath('./div/div[1]/a/img/@src') else goods.xpath(
                    './div/div[1]/a/img/@data-lazy-img')),
                'comment': ''.join(goods.xpath(".//div[@class='p-commit']/strong//text()")),
                'shop': ' '.join(goods.xpath('./div/div[5]/span/a/text()'))
            }
            datas.append(data)
        return datas

    # 创建连接mongodb数据库并写入函数
    def save_data(self, data):
        client = pymongo.MongoClient(host='localhost', port=27017)
        db = client['JD']
        db['口罩'].insert_many(data)

    def main(self):
        url = 'http://www.jd.com'
        KEYWORD = '口罩'
        self.search(url,keyword=KEYWORD)
        # total = self.search(url)
        # 此处可设置需要爬取多少页面的数据
        # 例如爬取搜素到的关键词查询出的总页数得数据
        for page in range(2, 5):
            self.next_page()


if __name__ == '__main__':
    r = JDSpider()
    r.main()
