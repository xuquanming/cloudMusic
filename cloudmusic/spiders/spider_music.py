import scrapy
import time
import requests
import json
from scrapy import Selector,signals
from pydispatch import dispatcher
from ..items import SingerItem, CommentItem
from selenium import webdriver

class MusicSpider(scrapy.Spider):
    name = 'musicspider'
    allowed_domain = ['http://music.163.com']
    start_urls = 'http://music.163.com/discover/artist'
    referer = 'http://music.163.com'
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'
    headers = {'User-Agent': user_agent, 'Referer': referer}

    def __init__(self):
        self.driver = webdriver.Chrome()
        super(MusicSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        self.driver.close()

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls, headers=self.headers, method='GET', callback=self.parse)

    def parse(self, response):
        lists = response.selector.xpath('//ul[@id="m-artist-box"]/li')
        singer_list = []
        for info in lists:
            try:
                name = info.xpath('p/a[1]/text()').extract()[0]
                url = info.xpath('p/a[1]/@href').extract()[0]
                url = response.urljoin(url.strip())
                print(url)
                print(type(url))
                headimg = info.xpath('div/img/@src').extract()[0]
                singer_list.append({'name': name, 'url': url, 'headimg':headimg})
            except Exception:
                name = info.xpath('a[1]/text()').extract()[0]
                url = info.xpath('a[1]/@href').extract()[0]
                url = response.urljoin(url.strip())
                singer_list.append({'name': name, 'url': url})

        time_str = time.strftime('%H-%M-%S',time.localtime())
        with open(time_str+"Top_100.json", "w", encoding='utf-8') as f:
            # json.dump(dict_var, f)  # 写为一行
            json.dump(singer_list, f, indent=2, sort_keys=False, ensure_ascii=False)  # 写为多行
        for i in singer_list:
            url = i['url']
            yield scrapy.Request(url=url, headers=self.headers, method='GET', callback=self.singer_parse)

    def singer_parse(self, response):
        item = SingerItem()
        music_url = response.xpath('//script[@type="application/ld+json"]/text()').extract()[0]
        short_desc = json.loads(music_url)
        l, r = short_desc['@id'].split('?')
        item['name'] = short_desc['title']
        item['headimg'] = short_desc['images']
        item['brief'] = short_desc['description']
        item['url'] = short_desc['@id']
        item['context'] = short_desc['@context']
        item['desc_url'] = l + '/desc' + '?' + r
        item['pubdate'] = short_desc['pubDate']
        song_info = response.xpath('//div[@id="artist-top50"]//tbody/tr')
        song_list = []
        for i in song_info:
            url = i.xpath('td//span/a/@href').extract()[0]
            url = response.urljoin(url.strip())
            song = i.xpath('td//span/a/b/@title').extract()[0]
            time = i.xpath('td[@class="w2-1 s-fc3"]/span/text()').extract()[0]
            album = i.xpath('td[@class="w4"]/div/a/@title').extract()[0]
            album_url = i.xpath('td[@class="w4"]/div/a/@href').extract()[0]
            song_list.append({'name':song,'url':url,'time':time,'album':album,'album_url':album_url})

        item['song'] = song_list
        yield item
        for i in item['song']:
            url = i['url']
            yield scrapy.Request(url=url, headers=self.headers, method='GET', callback=self.music_parse)


    def music_parse(self, response):
        item = CommentItem()
        song_info = response.xpath('//div[@class="cnt"]')
        item['song'] = song_info.xpath('div/div/em/text()').extract()[0]
        item['singer'] = song_info.xpath('p/span/@title').extract()[0]
        item['album'] = song_info.xpath('p/a/text()').extract()[0]
        item['total'] = '共'+response.xpath('//div[@id="comment-box"]/div/div/span/span/text()').extract()[0]+'评论'
        comment = response.xpath('//div[@class="cmmts j-flag"]/div')
        cmmts = []
        for i in comment:
            image = i.xpath('div/a/img/@src').extract()[0]
            name = i.xpath('div/div/div/a/text()').extract()[0]
            content = i.xpath('div/div/div[@class="cnt f-brk"]/text()').extract()[0]
            time = i.xpath('div/div/div[@class="time s-fc4"]/text()').extract()[0]
            cmmts.append({'headimg':image,'name':name,'content':content,'time':time})
        item['comment'] = cmmts
        yield item