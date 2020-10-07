import requests
from scrapy.selector import Selector
import random
import time
import json
class ProxyMiddleWare(object):
    proxy_list=["http://58.87.89.234:31",
    #此处省略一堆代理IP
    ]

def process_request(self,request,spider):
    ip = random.choice(self.proxy_list)
    request.meta['proxy'] = ip

DOWNLOADER_MIDDLEWARES = {
   'wechat_spider.middlewares.RandomUserAgent': 10,
   'wechat_spider.middlewares.ProxyMiddleWare': 100,
}

def get_proxy():
    url = 0
    url = 'https://www.zdaye.com/dayProxy/ip/323777.html'
    response = requests.get(url)
    response.encoding = 'utf-8'
    html = response.text
    time_str = time.strftime('%H-%M-%S',time.localtime())
    proxy = Selector(text=html).xpath('//div[@class="cont"]/text()').extract()
    Proxy = []
    for i in proxy:
        p ='http://'+i.split('@')[0]
        Proxy.append(p)
    with open(time_str+'Proxy.json', 'w', encoding='utf-8') as f:
        json.dump(Proxy, f, indent=2, sort_keys=False, ensure_ascii=False)  # 写为多行