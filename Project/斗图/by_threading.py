# -*- coding: utf-8 -*-
"""
@File    : doutu.py
@Time    : 2020/8/16
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
import os
import re
import time
from queue import Queue
import requests
import threading
from lxml import etree
import chardet
from fake_useragent import UserAgent
from urllib.request import urlretrieve

ua = UserAgent()
HEADERS = {"user-agent": ua.random}  # 指定浏览器 user-agent


class Producer(threading.Thread):
    def __init__(self, page_queue, img_queue):
        super().__init__()
        self.page_queue = page_queue
        self.img_queue = img_queue
        self.headers = HEADERS

    def run(self):
        while True:
            if self.page_queue.empty():
                break
            url = self.page_queue.get()
            data = self.get_page(url)
            self.parse_page(data)

    def get_page(self, url):
        response = requests.get(url, headers=self.headers)
        try:
            if response.status_code == 200:
                response.encoding = chardet.detect(
                    response.content)['encoding']
                return response.text
            return None
        except requests.exceptions.ConnectionError as e:
            print(e.args)

    def parse_page(self, content):
        data = etree.HTML(content)
        imgs = data.xpath('//div[@class="page-content text-center"]//img')
        for img in imgs:
            img_url = img.get('data-original')
            name = img.get('alt')
            # 去除图片名的特殊字符
            name = re.sub(r'[\?？\.,。，\*！!\\]', '', name)
            # 获取后缀名
            suffix = os.path.splitext(img_url)[1]
            filename = name + suffix
            # 注意以元组形式来加入队列
            self.img_queue.put((img_url, filename))


class Consumer(threading.Thread):
    def __init__(self, page_queue, img_queue):
        super().__init__()
        self.page_queue = page_queue
        self.img_queue = img_queue

    def run(self):
        # 元组解包
        while True:
            if self.img_queue.empty() and self.page_queue.empty():
                break
            img_url, filename = self.img_queue.get()
            img_path = 'images2'
            if not os.path.exists(img_path):
                os.makedirs(img_path)
            urlretrieve(img_url, img_path + os.path.sep + filename)
            print(filename + '下载完成！')

def main():
    page_queue = Queue(10)
    img_queue = Queue()
    start = time.time()
    for page in range(1, 11):
        url = 'https://www.doutula.com/photo/list/?page={}'.format(page)
        page_queue.put(url)

    p_threads = []
    for i in range(5):
        t = Producer(page_queue, img_queue)
        t.start()
        p_threads.append(t)

    for thread in p_threads:
        thread.join()

    c_threads = []
    for j in range(5):
        t = Consumer(page_queue, img_queue)
        t.start()
        c_threads.append(t)

    for thread in p_threads:
        thread.join()

    end = time.time()
    print(end - start)


if __name__ == '__main__':
    main()
