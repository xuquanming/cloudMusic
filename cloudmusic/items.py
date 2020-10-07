# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CloudmusicItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass



class SingerItem(scrapy.Item):
    headimg = scrapy.Field()
    name = scrapy.Field()
    url = scrapy.Field()
    context = scrapy.Field()
    song = scrapy.Field()
    brief = scrapy.Field()
    desc_url = scrapy.Field()
    pubdate = scrapy.Field()

class CommentItem(scrapy.Item):
    song = scrapy.Field()
    singer = scrapy.Field()
    album = scrapy.Field()
    total = scrapy.Field()
    comment = scrapy.Field()