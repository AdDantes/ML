# -*- coding: utf-8 -*-
import scrapy
import re
import time
import hashlib
import random
from ..items import LogodownloadItem, LogospiderItem


class DesignevoSpider(scrapy.Spider):
    name = "designevo"
    allowed_domains = ["designevo.com"]
    start_urls = ['https://www.designevo.com/res/templates/thumb_small/']

    def parse(self, response):
        t = str(int(time.time()))
        rand = str(random.randint(0, 100000))

        i = LogodownloadItem()
        item = LogospiderItem()
        tr_list = response.xpath('//tr')
        for tr in tr_list:
            image_link = tr.xpath('./td/a/@href').extract_first()
            item['image_link'] = 'https://www.designevo.com/res/templates/thumb_small/'+str(image_link)
            i['image_urls'] = [item['image_link']]
            i['image_names'] = re.findall('thumb_small/(.*?).png',item['image_link']) if re.findall('thumb_small/(.*?).png',item['image_link']) else None
            if type(i['image_names']) == list:
                for image_name in i['image_names']:
                    item['image_name'] = image_name
                    image_tags = image_name.split('-')
                    item['image_tags'] = [i for i in image_tags if i != 'and']
                    item['image_kid'] = image_tags[0]
                    i['image_kid'] = image_tags[0]
                    i['current_time'] = t
                    i['randint'] = rand

                    curtime = time.strftime("%Y-%m-%d", time.localtime())
                    # 通过对图片名称，时间戳，随机数三个数据进行加密生成指纹用于定义新图片名称，避免名称重复
                    fp = hashlib.sha1()
                    name = item['image_name']
                    fp.update(name.encode())
                    fp.update(t.encode())
                    fp.update(rand.encode())
                    fp = fp.hexdigest()

                    item['image_from'] = self.allowed_domains[0]
                    i['image_from'] = self.name
                    item['image_path'] = '/data/logo_images/' + i['image_from'] + '/' + curtime + '/' + item[
                        'image_kid'] + '/' + fp + '.' + \
                                         item['image_link'].split('.')[-1]

                    print('%s类商标信息：正在下载中............' % str(item['image_kid']))
                    print(item)
                    yield i
                    yield item