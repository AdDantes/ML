# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class ZufangPipeline(object):
    def __init__(self):
        # 连接本地数据库，测试专用！
        self.client = MongoClient('localhost', 27017)
        # 连接公司数据库，开发专用！
        # self.client = MongoClient(host="10.0.100.76", port=27017)
        self.db = self.client.zufang
        # self.db.authenticate('', '')

        self.tongcheng = self.db['tongcheng']

    def process_item(self, item, spider):
        if spider.name == 'tongcheng':
            self.tongcheng.insert_one(dict(item))


        return item
