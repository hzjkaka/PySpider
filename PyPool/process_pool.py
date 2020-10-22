import concurrent.futures

import time
from multiprocessing import Pool
import urllib.request
import urllib.error


def get_url(url):
    try:
        urllib.request.urlopen(url)
        print(f'URL {url} Scraped')
    except (urllib.error.HTTPError, urllib.error.URLError):
        print(f'URL {url} not Scraped')


if __name__ == '__main__':
    # pool = Pool(processes=3)

    urls = [
        'https://www.baidu.com',
        'http://www.meituan.com/',
        'http://blog.csdn.net/',
        'http://xxxyxxx.net'
    ]
    # start_time = time.time()
    # for url in urls:
    #     get_url(url)
    # end_time = time.time()
    # print(end_time - start_time)
    # pool.map(get_url, urls)
    # pool.close()

    # 线程池执行--采用map的方式来分配任务
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = executor.map(get_url, urls)
    end_time = time.time()
    print(end_time-start_time)

    #第二种写法
    # start_time = time.time()
    # with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    #     for url in urls:
    #         executor.submit(get_url, url)
    # end_time = time.time()
    # print(end_time-start_time)
    #
    '''
    进程池
    
    '''
    #--采用map的方式来分配任务
    # start_time = time.time()
    # with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
    #     futures = executor.map(get_url, urls)
    # end_time = time.time()
    # print(end_time - start_time)

    # 第二种写法
    # start_time = time.time()
    # with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
    #     for url in urls:
    #         executor.submit(get_url, url)
    # end_time = time.time()
    # print(end_time-start_time

