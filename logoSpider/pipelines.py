# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from pymongo import MongoClient
from .items import  BranddownloadItem
from scrapy.pipelines.images import ImagesPipeline, DropItem
from scrapy.conf import settings
import time
import hashlib
from .log import logger
import re




class BrandDownloadPipeline(ImagesPipeline):  # 商标网图片：
    image_store = settings['IMAGES_STORE']
    localtime = time.localtime(time.time())
    curtime = time.strftime("%Y-%m-%d", time.localtime())

    def get_media_requests(self, item, info):
        if isinstance(item, BranddownloadItem):
            for image_url in item['image_link']:
                yield scrapy.Request(image_url, meta={'item': item, 'index': item['image_link'].index(
                    image_url)})

    def item_completed(self, results, item, info):
        if isinstance(item, BranddownloadItem):
            image_path = [data['path'] for ok, data in results if ok]
            if not image_path:
                raise DropItem("Item contains no images")
            return item

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']  # 通过上面的meta传递过来item
        index = request.meta['index']  # 通过上面的index传递过来列表中当前下载图片的下标
        name = item['image_name'][index]
        image_guid = name + '.' + request.url.split('.')[-1]
        path = '%s/%s/%s.jpg' % (item['image_from'], str(item['image_kid']), image_guid)
        return path


class BrandMongoPipeline(object):  # 商标信息
    def __init__(self):
        # 连接本地数据库，测试专用！
        self.client = MongoClient(host='10.0.93.43',port=27017)
        self.mydb = self.client['brand']
        self.gov = self.mydb['brand_gov']


        # 连接公司数据库，开发专用！
        # self.client = MongoClient(host="10.0.100.76", port=27017)
        # self.db = self.client.trademark
        # self.db.authenticate('trademark', 'trademark')
        # self.Brand = self.db['brand_info']
        # self.test = self.db['brand_t22']

    def process_item(self, item, spider):
        if spider.name == 'govitem':
            self.gov.insert(dict(item))
        return item

