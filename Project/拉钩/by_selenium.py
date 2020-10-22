# -*- coding: utf-8 -*-
"""
@File    : by_selenium.py
@Time    : 2020/8/16
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
import re
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium .webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from lxml import etree
# options = 浏览器特征.ChromeOptions()
# options.add_argument('--headless')
# self.driver = 浏览器特征.Chrome(options=options)
class LagouSpider():
    def __init__(self):
        self.option = ChromeOptions()
        self.option.add_experimental_option(
            "excludeSwitches", ["enable-automation"])  # 开发者模式
        self.option.add_experimental_option(
            'useAutomationExtension', False)  # 取消chrome受自动控制提示
        self.driver = webdriver.Chrome(options=self.option)
        self.url = 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='
        self.positions = []
        self.wait = WebDriverWait(self.driver, 10)

    def parse_index(self, source):
        html = etree.HTML(source)
        links = html.xpath("//a[@class='position_link']/@href")
        for link in links:
            self.get_detail_page(link)
            time.sleep(2)

    def get_detail_page(self, detail_url):
        self.driver.execute_script("window.open('%s')" % detail_url)
        # self.driver.get(detail_url)
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.wait.until(EC.presence_of_element_located(
            (By.XPATH, '//div[@class="job-name"]/h1[@class="name"]')))
        detail_source = self.driver.page_source
        self.parse_detail_page(detail_source)
        # 关闭详情页
        self.driver.close()
        # 继续切回职位列表页
        self.driver.switch_to.window(self.driver.window_handles[0])

    def parse_detail_page(self, detail_source):
        html = etree.HTML(detail_source)
        name = html.xpath('//h1[@class="name"]/text()')[0]
        job_spans = html.xpath("//dd[@class='job_request']//span")
        salary = job_spans[0].xpath(".//text()")[0].strip()
        company = html.xpath('//div/h3/em/text()')[0].strip()
        city = job_spans[1].xpath(".//text()")[0].strip()
        city = re.sub(r'[\s/]', '', city)
        years = job_spans[2].xpath('.//text()')[0].strip()
        years = re.sub(r'[\s/]', '', years)
        education = job_spans[3].xpath('.//text()')[0].strip()
        education = re.sub(r'[\s/]', '', education)
        des = ''.join(html.xpath(
            '//dd[@class="job_bt"]//text()')).replace('\n', '').replace('\xa0', '').strip()
        position = {
            '职位名称': name,
            '公司名字':company,
            '薪水': salary,
            '城市': city,
            '工作时间': years,
            '学历': education,
            '简介': des
        }
        self.positions.append(position)
        print(position)

    def run(self):
        self.driver.get(self.url)
        while True:
            source = self.driver.page_source
            self.wait.until(EC.presence_of_element_located(
                (By.XPATH, '//span[contains(text(),"下一页")]')))
            self.parse_index(source)
            try:
                next = self.driver.find_element_by_xpath(
                    '//span[contains(text(),"下一页")]')
                if "pager_next pager_next_disabled" in next.get_attribute('class'):
                    break

                else:
                    #页面上的元素找到了，可是在点击的时候由于页面大小或许其它的原因，
                    # 导致定位的元素上面其实还有其它的元素，也就是说找的的元素被一个不知名的元素遮挡住了，
                    # 导致点击在遮挡元素上。因为selenium的点击是根据找的元素的坐标，然后去点击那个坐标的原因
                    #因此不能直接使用click()
                    #下拉页面:browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
                    self.driver.execute_script("arguments[0].click();", next)
                    #或者：element = driver.find_element_by_css('//span[contains(text(),"下一页")]')
                    # 浏览器特征.ActionChains(driver).move_to_element(element ).click(element ).perform()
            except :
                print('Error')
            time.sleep(1)


if __name__ == '__main__':
    s = LagouSpider()
    s.run()
