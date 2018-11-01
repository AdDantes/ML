# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import time
import hashlib
import random
from ..items import LogodownloadItem, LogospiderItem


class LogosheSpider(CrawlSpider):
    name = 'logoshe'
    allowed_domains = ['logoshe.com']
    start_urls = ['http://logoshe.com/logo/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="fenlei-list"]/ul/li/a',)),
             callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="fenye-1"]/ul/li')), follow=True),
    )

    def parse_item(self, response):
        t = str(int(time.time()))
        rand = str(random.randint(0, 100000))

        i = LogodownloadItem()  # 商标素材图片下载
        i['image_kid'] = response.xpath('//div[@class="zuosmp"]/a[3]/text()').extract_first()
        i['image_names'] = response.xpath('//div[@class="xinzhongjian-zuotitle"]/h2/text()').extract()
        i['image_urls'] = response.xpath('//div[@class="zuocontentnei"]/img/@src').extract()
        i['current_time'] = t
        i['randint'] = rand

        item = LogospiderItem()  # 商标素材信息
        item['image_kid'] = response.xpath('//div[@class="zuosmp"]/a[3]/text()').extract_first()
        item['image_name'] = response.xpath('//div[@class="xinzhongjian-zuotitle"]/h2/text()').extract_first()
        item['image_link'] = response.xpath('//div[@class="zuocontentnei"]/img/@src').extract_first()
        item['image_tags'] = response.xpath('//div[@class="zuobiaoqian"]/a/text()').extract()
        curtime = time.strftime("%Y-%m-%d", time.localtime())
        # 通过对图片名称，时间戳，随机数三个数据进行加密生成指纹用于定义新图片名称，避免名称重复
        fp = hashlib.sha1()
        name = item['image_name']
        fp.update(name.encode())
        fp.update(t.encode())
        fp.update(rand.encode())
        fp = fp.hexdigest()

        item['image_from'] = re.findall('http://www.(.*?)/', item['image_link'])[0]
        i['image_from'] = re.findall('http://www.(.*?).com/', item['image_link'])[0]
        item['image_path'] = '/data/logo_images/' + i['image_from'] + '/' + curtime + '/' + item[
            'image_kid'] + '/' + fp + '.' + \
                             item['image_link'].split('.')[-1]
        print('%s类商标信息：正在下载中............' % str(item['image_kid']))

        print(item)
        yield i
        yield item
