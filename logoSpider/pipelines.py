# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from pymongo import MongoClient
from .items import LogospiderItem, LogodownloadItem,SvgItem
from scrapy.pipelines.images import ImagesPipeline, DropItem
from scrapy.conf import settings
import time
import hashlib
from .log import logger
import re
import os


class LogoDownloadPipeline(ImagesPipeline):  # logo素材图片下载
    image_store = settings['IMAGES_STORE']
    localtime = time.localtime(time.time())
    curtime = time.strftime("%Y-%m-%d", time.localtime())

    def get_media_requests(self, item, info):
        if isinstance(item, LogodownloadItem):
            for image_url in item['image_urls']:
                yield scrapy.Request(image_url, meta={'item': item, 'index': item['image_urls'].index(
                    image_url)})  # 添加meta是为了下面重命名文件名使用

    def item_completed(self, results, item, info):
        if isinstance(item, LogodownloadItem):
            image_path = [data['path'] for ok, data in results if ok]
            if not image_path:
                raise DropItem("Item contains no images")
            return item

    def file_path(self, request, response=None, info=None):
        # logo素材图片：
        item = request.meta['item']  # 通过上面的meta传递过来item
        index = request.meta['index']  # 通过上面的index传递过来列表中当前下载图片的下标

        # 图片文件名：item['image_names'][index]得到名称 + 时间戳 + 随机数 +request.url.split('.')[-1]得到图片后缀jpg,png
        name = item['image_names'][index]
        ctime = item['current_time']
        rand = item['randint']

        # 通过对图片名称，时间戳，随机数三个数据进行加密生成指纹用于定义新图片名称，避免名称重复
        fp = hashlib.sha1()
        fp.update(name.encode())
        fp.update(ctime.encode())
        fp.update(rand.encode())
        fp = fp.hexdigest()

        image_guid = fp + '.' + request.url.split('.')[-1]
        path = '%s/%s/%s/%s' % (item['image_from'], self.curtime, str(item['image_kid']), image_guid)
        return path


class MongoPipeline(object):  # logo素材信息
    def __init__(self):
        # 连接本地数据库，测试专用！
        self.client = MongoClient('localhost', 27017)
        # 连接公司数据库，开发专用！
        # self.client = MongoClient(host="10.0.100.76", port=27017)
        self.db = self.client.logo
        # self.db.authenticate('', '')

        self.logo = self.db['logo_info']

    def process_item(self, item, spider):
        if spider.name == 'logo':
            if isinstance(item, LogospiderItem):
                self.logo.insert_one(dict(item))
        elif spider.name == 'cnlogo':
            if isinstance(item, LogospiderItem):
                self.logo.insert_one(dict(item))
        elif spider.name == 'logoids':
            if isinstance(item, LogospiderItem):
                self.logo.insert_one(dict(item))
        elif spider.name == 'ibiaozhi':
            if isinstance(item, LogospiderItem):
                self.logo.insert_one(dict(item))
        elif spider.name == 'logoshe':
            if isinstance(item, LogospiderItem):
                self.logo.insert_one(dict(item))
        elif spider.name == 'logoquan':
            if isinstance(item, LogospiderItem):
                self.logo.insert_one(dict(item))
        elif spider.name == 'easyicon':
            if isinstance(item, LogospiderItem):
                self.logo.insert_one(dict(item))
        elif spider.name == 'logonc':
            if isinstance(item, LogospiderItem):
                self.logo.insert_one(dict(item))
        elif spider.name == 'doooor':
            if isinstance(item, LogospiderItem):
                self.logo.insert_one(dict(item))
        elif spider.name == 'designevo':
            if isinstance(item, LogospiderItem):
                self.logo.insert_one(dict(item))
        elif spider.name == 'logosj':
            if isinstance(item, LogospiderItem):
                self.logo.insert_one(dict(item))
        elif spider.name == 'logoopnd':
            if isinstance(item, LogospiderItem):
                self.logo.insert_one(dict(item))

        return item

class SvgPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, SvgItem):
            # if not os.path.exists('/svg_data/{}'.format(item['kid_name'],item['img_name'])):  ###判断文件是否存在，返回布尔值
            #     os.makedirs('/svg_data/{}'.format(item['kid_name']))
            # ##os.makedirs() 这个连同中间的目录都会创建，类似于参数mkdir -p
            #     with open('/svg_data/{}/{}'.format(item['kid_name'],item['img_name'])) as f:
            #         f.write(item['svg'])
            # else:
            #     with open('/svg_data/{}/{}'.format(item['kid_name'], item['img_name'])) as f:
            #         f.write(item['svg'])

            if os.path.exists('E:\\flaticon\{}'.format(item['kid_name'])):

                with open('E:\\flaticon\{}\{}.svg'.format(item['kid_name'], item['svg_name']), 'w',
                          encoding='utf-8') as f:
                    f.write(item['svg'])
            else:
                os.makedirs('E:\\flaticon\{}'.format(item['kid_name']))
                with open('E:\\flaticon\{}\{}.svg'.format(item['kid_name'], item['svg_name']), 'w',
                          encoding='utf-8') as f:
                    f.write(item['svg'])
