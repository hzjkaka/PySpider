# -*- coding: utf-8 -*-
"""
@File    : by_pyppeteer.py
@Time    : 2020/8/13 
@Author  : Hzj
@Email   : hzjkaka@163.com
@IDE: PyCharm
"""
from pyppeteer import launch
import asyncio

width,height = 1366, 768

async def get_data(url,page_num):
    browser = await  launch(headless=False, args=['--disable-infobars', f'--window-size={width},{height}'])
    page = await browser.newPage()
    await page.setViewport({"width": width, "height": height})
    await page.goto(url)
    await page.waitFor(100)
    await page.evaluate('window.scrollBy(0, document.body.scrollHeight)')
    #  等待时间  用来渲染页面
    await asyncio.sleep(1)
    print(page_num)
    print("########################################")
    elem_list = await page.xpath("//div[@class='gl-i-wrap']")

    #  获取数据
    for num in elem_list:
        item = dict()
        name  = await num.xpath("./div[@class='p-name p-name-type-2']/a")
        item["name"] = await (await name[0].getProperty("title")).jsonValue()
        price = await num.xpath("./div[@class='p-price']/strong/i")
        item["price"] = await (await price[0].getProperty("textContent")).jsonValue()

        print(item)

async def main():
    for i in range(100):
        page_num = i+2
        url = "https://search.jd.com/Search?keyword=ipad&page={}".format(page_num)
        await  get_data(url,page_num)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
