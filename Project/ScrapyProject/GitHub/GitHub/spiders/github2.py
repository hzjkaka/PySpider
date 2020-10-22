# -*- coding: utf-8 -*-
import re

import scrapy


class Github2Spider(scrapy.Spider):
    name = 'github2'
    allowed_domains = ['github.com']
    start_urls = ['http://github.com/login']

    def parse(self, response):
        #自动从response找寻form表单
        yield scrapy.FormRequest.from_response(
            response,
            formdata={'login':'hzjkaka','password':'123456'},
            callback= self.after_login
        )
    def after_login(self, response):
        print(re.findall("hzjkaka", response.body.decode()))
