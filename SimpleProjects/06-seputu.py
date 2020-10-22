'''
盗墓笔记小说的爬取
'''
import csv
import re
import chardet
import requests
from lxml import etree as et
headers = {
    "User-Agent": "Mozilla/5.0(WindowsNT6.3;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/68.0.3440.106Safari/537.36"
}
url = 'http://seputu.com/'
r = requests.get(url, headers=headers)
r.encoding = chardet.detect(r.content)['encoding']
print(r.encoding)
print(r.text)
html = et.HTML(r.text)
div_mulus = html.xpath('.//*[@class="mulu"]')
rows = []
for div_mulu in div_mulus:
    div_h2 = div_mulu.xpath('./div[@class="mulu-title"]/center/h2/text()')
    # print(div_h2)
    if len(div_h2) > 0:
        h2_title = div_h2[0]
        a_s = div_mulu.xpath('./div[@class="box"]/ul/li/a')
        print(a_s)
        for a in a_s:
            href = a.xpath('./@href')[0]
            box_title = a.xpath('./@title')[0]
            pattern = re.compile(r'\s*\[(.*)\]\s+(.*)')  # []前后的\转义的意思
            match = re.search(pattern, box_title)
            if match is not None:
                date = match.group(1)
                real_title = match.group(2)
                content = (h2_title, real_title, date)
                print(content)
                rows.append(content)

# header = ["title", 'real_title', 'href', 'date']
# with open("spputu.csv", 'w') as file:
#     f = csv.writer(file)
#     f.writerow(header)
#     f.writerows(rows)
