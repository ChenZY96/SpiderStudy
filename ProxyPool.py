# coding=utf-8
import requests
from pyquery import PyQuery as pq
from requests.exceptions import ConnectionError
import random
from pymongo import MongoClient
from gevent.threadpool import ThreadPool
import gevent

TEST_URL = 'https://www.baidu.com'


client = MongoClient("localhost",27017)
db = client.proxies
collection = db['Proxy_Port']

def parse_url(url):
    headers = [
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:34.0) Gecko/20100101 Firefox/34.0'},
        {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'},
        {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11'},
        {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'},
        {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:40.0) Gecko/20100101 Firefox/40.0'},
        {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/44.0.2403.89 Chrome/44.0.2403.89 Safari/537.36'}
    ]

    try:
        response = requests.get(url,headers=random.choice(headers))
        if response.status_code == 200:
            return response.text
    except ConnectionError:
        print('Error')

def proxy_xici():
    url = 'http://www.xicidaili.com/nn'
    response = parse_url(url)
    doc = pq(response)

    total_page = doc.find('.pagination a').eq(-2).text()
    total_page=5
    proxies = []
    for page in range(1,int(total_page)+1):
        url = 'http://www.xicidaili.com/nn/{}'.format(page)
        doc = pq(parse_url(url))
        trs = doc.find('table#ip_list tr').items()
        for tr in trs:
            if tr == doc.find('table#ip_list tr').eq(0):
                continue
            ip = tr.find('td').eq(1).text()
            port = tr.find('td').eq(2).text()
            #proxy = ip+':'+port
            proxy = {
                'ip':ip,
                'port':port
            }
            proxies.append(proxy)
    return proxies

def proxy_test(proxy):
    try:
        resp = requests.get(TEST_URL, proxies={'http': 'http://{0}:{1}'.format(proxy['ip'], proxy['port']),
                                               'https': 'https://{0}:{1}'.format(proxy['ip'], proxy['port'])}, timeout=10)
        if resp and resp.status_code == 200:
            print('Valid proxy', proxy)
            collection.insert(proxy)
            #print('Valid proxy', proxy)
    except Exception as e:
        pass


proxies = proxy_xici()
pool = ThreadPool(20)
threads = [pool.spawn(proxy_test, each) for each in proxies]
gevent.joinall(threads)

