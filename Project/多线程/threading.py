# -*- coding: utf-8 -*-
"""
@File    : threading.py
@Time    : 2020/8/28
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
import requests
from lxml import etree
from queue import Queue
import threading
import json


class ThreadCrawl(threading.Thread):
    def __init__(self, threadName, pageQueue, dataQueue):
        # 父类初始化方法
        super(ThreadCrawl, self).__init__()
        self.threadName = threadName
        self.pageQueue = pageQueue
        self.dataQueue = dataQueue
        self.headers = {}

    def run(self):
        print("启动" + self.threadName)
        while not CRAWL_EXIT:
            # 取出一个值
            # get()中有个参数block，默认值为True，
            # 为True就会进入阻塞状态直到有新的参数
            # 为False，就会弹出一个Queue.empty()异常
            try:
                page = self.pageQueue.get(False)
                url = 'http://www.qiushibaike.com/8hr/page/' + str(page) + "/"
                r = requests.get(url, headers=self.headers)
                self.dataQueue.put(r.content)
            except BaseException:
                pass
        print("结束" + self.threadName)


class ThreadParse(threading.Thread):
    def __init__(self, threadName, dataQueue, filename):
        # 父类初始化方法
        super(ThreadParse, self).__init__()
        self.threadName = threadName
        self.dataQueue = dataQueue
        self.filename = filename

    def run(self):
        while not PARSE_EXIT:
            try:
                html = self.dataQueue.get(False)
                self.parse(html)
            except BaseException:
                pass

    def parse(self, html):
        pass


CRAWL_EXIT = False
PARSE_EXIT = False


def main():
    # 页码的队列
    pageQueue = Queue(10)
    # 放入1-10，先进先出
    for i in range(1, 11):
        pageQueue.put(i)
    # 采集结果的数据队列，参数为空表示不限制
    dataQueue = Queue()
    # 本地文件
    filename = open('duanzi.txt', 'a+')

    # 三个采集线程
    crawlList = ['采集线程1', '采集线程2', '采集线程3']
    threadCrawl = []
    for threadName in crawlList:
        thread = ThreadCrawl(threadName, pageQueue, dataQueue)
        thread.start()
        threadCrawl.append(thread)

    # 三个解析线程
    parseList = ['解析线程1', '解析线程2', '解析线程3']
    # 存储三个解析现线程的列表
    threadParse = []
    for threadName in parseList:
        thread = ThreadParse(threadName, dataQueue, filename)
        thread.start()
        threadParse.append(thread)

    # 等待队列为空,之前的操作执行完毕
    while not pageQueue.empty():
        pass

    while not dataQueue.empty():
        pass

    global CRAWL_EXIT, PARSE_EXIT
    CRAWL_EXIT = True
    print('pageQueue为空')

    for thread in threadCrawl:
        thread.join()
        print('1')

    PARSE_EXIT = True
    print('dataQueue为空')

    for thread in threadParse:
        thread.join()
        print('1')


# 防止错误执行的
if __name__ == '__main__':
   main()
