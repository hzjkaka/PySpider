# -*- coding: utf-8 -*-
"""
@File    : wycj_spider.py
@Time    : 2020/10/23
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
import time
import requests
import random
from lxml import etree
from fake_useragent import UserAgent
# 随机化请求头和请求IP
# 随意变换headers，实现支持随机生成请求头
ua = UserAgent()
# 指定浏览器 User-Agent
HEADERS = {"User-Agent": ua.random}
TIME = random.randint(1,2)
BASIC_URl = 'http://money.163.com'
TOTAL_PAGE = 20
# 设计网易财经新闻的爬虫类
'''
爬取起始UrL：http://money.163.com/special/00252G50/macro.html的数据
'''


class WYCJ(object):
    # 初始化数据
    def __init__(self):
        self.headers = HEADERS
        # self.timeout = TIME_OUT

    # 发送请求和获取响应
    def get_page(self, url):
        response = requests.get(
            url,
            headers=self.headers)
        try:
            if response.status_code == 200:
                return response.text
            return None
        except requests.exceptions.ConnectionError as e:
            print(e.args)

    # 定义列表页1的爬取方法
    def get_index1(self, page):
        index_url = f'{BASIC_URl}/special/00252G50/macro_0{page}.html'
        return self.get_page(index_url)

    # 定义列表页2的爬取方法
    def get_index2(self, page):
        index_url = f'{BASIC_URl}/special/00252G50/macro_{page}.html'
        return self.get_page(index_url)

    # 定义详情页的url爬取方法
    def detail_url(self, html):
        data = etree.HTML(html)
        # 使用xpath找的详情页的跳转url
        urls = data.xpath("//div[@class='list_item clearfix']//h2/a/@href")
        return urls

    # 请求详情页
    def get_detail(self, url):
        return self.get_page(url)

    # 页面形式1：解析详情页的数据
    def parse_detail1(self, html):
        data = etree.HTML(html)
        title = ''.join(data.xpath(
            "//div[@class='article_title']/h2/text()")[0]).strip().replace('\n', '')
        publish_time = ''.join(data.xpath(
            "//div[@class='article_title']/div[@class='share_box']/p/span[1]/text()"))
        agency = ''.join(data.xpath(
            "//div[@class='article_title']/div[@class='share_box']/p/span[3]/text()"))
        comment = ''.join(data.xpath(
            "//div[@class='article_title']/div[@class='share_box']/span/span/a/text()"))
        content = ''.join(data.xpath("//div[@class='article_box']/div[@class='content']//p/text()"))\
            .replace('\u3000', '').strip()
        return (
            "新闻标题:'{0}'   发布时间:'{1}'    发布机构:'{2}'   内容:'{3}'   跟帖:'{4}'".format(
                title,
                publish_time,
                agency,
                content,
                comment))

   # 页面形式2：解析详情页的数据
    def parse_detail2(self, html):
        data = etree.HTML(html)
        title = ''.join(data.xpath(
            "//div[@class='post_content_main']/h1/text()")[0]).strip().replace('\n', '')
        publish_time = ''.join(
            data.xpath("//div[@class='post_content_main']/div[@class='post_time_source']/text()")) .replace(
            '来源', '').replace(
            "\n", '').replace(
                '\u3000:', '').replace(
            "\t", '').strip()
        agency = ''.join(data.xpath(
            "//div[@class='post_content_main']/div[@class='post_time_source']/a[1]/text()"))
        content = ''.join(
            data.xpath("//div[@class='post_content_main']/div[@class='post_body']/div[@class='post_text']/p/text()")).replace(
            '\n',
            '') .replace(
            '\u3000',
            '').strip()
        author = ''.join(data.xpath(
            "//div[@class='post_content_main']/div[@class='post_body']/div[@class='post_text']/div[@class='ep-source cDGray']/span[2]/text()")) .replace('责任编辑：', '')
        return (
            "新闻标题:'{0}'   发布时间:'{1}'   发布机构:'{2}'   内容:'{3}'   作者:'{4}'".format(
                title,
                publish_time,
                agency,
                content,
                author))

    # 解析首页
    def parse_first_page(self):
        url = 'http://money.163.com/special/00252G50/macro.html'
        index_html = self.get_page(url)
        detail_urls = self.detail_url(index_html)
        for detail_url in detail_urls:
            if 'article' in detail_url:
                html = self.get_detail(detail_url)
                data = self.parse_detail1(html)
                self.save_data(data)
            else:
                html = self.get_detail(detail_url)
                data = self.parse_detail2(html)
                self.save_data(data)

    # 保存--打印数据
    def save_data(self, data):
        print('-' * 116)
        print(data)
        time.sleep(TIME)

    # 主程序
    def main(self):
        self.parse_first_page()
        # URL中页码大于2小于10的数据
        for page in range(2, 10):
            index_html = self.get_index1(page)
            detail_urls = self.detail_url(index_html)
            for detail_url in detail_urls:
                if 'article' in detail_url:
                    html = self.get_detail(detail_url)
                    data = self.parse_detail1(html)
                    self.save_data(data)
                else:
                    html = self.get_detail(detail_url)
                    data = self.parse_detail2(html)
                    self.save_data(data)
        # URL中页码大于10的数据
        for page in range(10, TOTAL_PAGE + 1):
            index_html = self.get_index2(page)
            detail_urls = self.detail_url(index_html)
            for detail_url in detail_urls:
                if 'article' in detail_url:
                    html = self.get_detail(detail_url)
                    data = self.parse_detail1(html)
                    self.save_data(data)
                else:
                    html = self.get_detail(detail_url)
                    data = self.parse_detail2(html)
                    self.save_data(data)


if __name__ == '__main__':
    response = WYCJ()
    response.main()

