# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
import json
from .items import SingerItem
from .items import CommentItem
from scrapy.utils.project import get_project_settings
settings = get_project_settings()


class CloudmusicPipeline:

    def __init__(self):
        host = settings['MONGODB_HOST']
        port = settings['MONGODB_PORT']
        db_name = settings['MONGODB_DBNAME']
        self.singer = settings['MONGODB_DOCNAME_SINGER']
        self.comment = settings['MONGODB_DOCNAME_COMMENT']
        self.client = pymongo.MongoClient(host=host, port=port)
        self.tdb = self.client[db_name]
        self.post = ''

    def process_item(self, item, spider):
        '''先判断itme类型，在放入相应数据库'''
        if isinstance(item, SingerItem):
            try:
                self.post = self.tdb[self.singer]
                singer_info = dict(item)  #
                if self.post.insert(singer_info):
                    print('Singer Successful!')
            except Exception as e:
                print(e)
        if isinstance(item, CommentItem):
            try:
                self.post = self.tdb[self.comment]
                Comment_info = dict(item)
                if self.post.insert(Comment_info):
                    print('Comment Successful!')
            except Exception as e:
                print(e)
        return item