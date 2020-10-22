import requests,chardet
headers = {
            "User-Agent": "Mozilla/5.0(WindowsNT6.3;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/68.0.3440.106Safari/537.36"
        }
url = 'http://seputu.com/'
r = requests.get(url,headers=headers)
#检测字符串编码
r.encoding = chardet.detect(r.content)['encoding']
print(r.text)