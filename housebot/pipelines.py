# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
import pymongo


class HousebotLocalFilePipeline(object):
    # save data to json file
    def __init__(self):
        self.file = codecs.open('test.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)
        return item


class HousebotMongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db, mongo_post):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_post = mongo_post

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB', 'items'),
            mongo_post=crawler.settings.get('MONGO_POST')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.post = self.db[self.mongo_post]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.post.insert(dict(item))
        return item
