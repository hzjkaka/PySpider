# -*- coding: utf-8 -*-
import scrapy


class RenrenLoginSpider(scrapy.Spider):
    name = 'renren_login'
    allowed_domains = ['renren.com']
    start_urls = ['http://renren.com/']

    def start_requests(self):
        url = 'http://www.renren.com/PLogin.do'
        data = {'email':'9710138074@qq.com','password':
                'pythonspider'}
        request = scrapy.FormRequest(url,formdata=data,callback=
                                     self.login)
        yield request
        
    def login(self,response):
        request = scrapy.Request(url='http://www.renren.com/880151247/profile',
        callback=self.index)
        yield request
    
    def index(self,response):
        with open('dp.html','w',encoding='utf-8') as f:
            f.write(response.text)
    def parse(self, response):
        pass
