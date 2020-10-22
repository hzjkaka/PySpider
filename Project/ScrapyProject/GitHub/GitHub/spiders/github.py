# -*- coding: utf-8 -*-
import re

import scrapy


class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    start_urls = ['http://github.com/login']

    def parse(self, response):
        authenticity_token = response.xpath("//input[@name='authenticity_token']/@value").extract_first()
        commit = response.xpath('//input[@name="commit"]/@value').extract_first()

        post_data = dict(
            login="hzjkaka",
            password="123456",
            authenticity_token=authenticity_token,
            commit=commit
        )
        yield scrapy.FormRequest(
            url='https://github.com/session',
            formdata=post_data,
            callback=self.after_login
        )

    def after_login(self, response):
        print(re.findall("hzjkaka", response.body.decode()))
