
from urllib.request import urlretrieve
import chardet
import requests
from lxml import etree
'''
从天堂网(https://www.ivsky.com/tupian)爬取心仪的图片下载保存到本地
'''
KEYWORD = 'ziranfengguang'
def get_img(url):
    headers = {
        "User-Agent": "Mozilla/5.0(WindowsNT6.3;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/68.0.3440.106Safari/537.36"
    }
    r = requests.get(url, headers=headers)
    r.encoding = chardet.detect(r.content)
    html = etree.HTML(r.content)
    img_urls = html.xpath('//img/@src')
    names = html.xpath('//img/@alt')
    # print(r.text)
    return img_urls, names

#获取当前的图片下载进度
def schedule(a, b, c):
    per = 100 * a * b / c
    if per > 100:
        per = 100
        print('当前下载进度：%d' % per)

def main():
    for i in range(1, 21):
        url = "https://www.ivsky.com/tupian/{}/index_{}".format(KEYWORD, i) + ".html"
        # print(url)
        img_urls = get_img(url)[0]
        name = get_img(url)[1]
        # print(name)
        k = 0
        for j in range(0, len(img_urls)):
            img_url = 'http:' + img_urls[j]
            filepath = 'D:/WebSpider/Py3Spider/photos/' + str(i) + str(j) + str(name[k]) + '.png'
            urlretrieve(img_url, filepath, schedule)
            k += 1
            i += 1
if __name__ == '__main__':
    main()




