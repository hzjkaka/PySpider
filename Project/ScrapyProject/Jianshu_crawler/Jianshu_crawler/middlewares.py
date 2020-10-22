# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import time

from scrapy import signals


class JianshuCrawlerSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the SpiderLearning, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('SpiderLearning opened: %s' % spider.name)


from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse
from selenium.webdriver import ChromeOptions
# from logging import getLogger



class SeleniumMiddleware():
    def __init__(self):
        self.option = ChromeOptions()
        self.option.add_experimental_option(
            "excludeSwitches", ["enable-automation"])  # 避免被检测
        self.option.add_experimental_option(
            'useAutomationExtension', False)  # 取消chrome受自动控制提示
        self.driver = webdriver.Chrome(options=self.option)
        self.wait = WebDriverWait(self.driver, 3)

    def process_request(self, request, spider):
        """
        用 selenium 抓取页面
        :param request: Request 对象
        :param spider: SpiderLearning 对象
        :return: HtmlResponse
        """

        self.driver.get(request.url)
        time.sleep(1)
        try:
            while True:
                submit = self.wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'H7E3vT')))
                submit.click()
                time.sleep(0.5)
                if not submit:
                    break
        except:
            pass
        response = HtmlResponse(url=request.url, body=self.driver.page_source, request=request, encoding='utf-8',
                            status=200)
        return response

