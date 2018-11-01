# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import time
import hashlib
import random
from ..items import LogodownloadItem, LogospiderItem


class IbiaozhiSpider(CrawlSpider):
    name = 'ibiaozhi'
    allowed_domains = ['ibiaozhi.com']
    start_urls = ['http://www.ibiaozhi.com/ilogo/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="Left"]/ul/li/p',)),
             callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="Page"]',)), follow=True),
    )

    def parse_item(self, response):
        t = str(int(time.time()))
        rand = str(random.randint(0, 100000))

        i = LogodownloadItem()
        i['image_kid'] = response.xpath('//div[@class="Index_tit"]/strong/text()').extract_first()
        if i['image_kid'] == '标志大全':
            i['image_kid'] = '其他'
        i['image_names'] = response.xpath('//div[@class="fl-left hidden Color10"]/strong/text()').extract()
        i['image_urls'] = response.xpath('//div[@class="fl-right hidden center"]/img/@src').extract()

        i['current_time'] = t
        i['randint'] = rand

        item = LogospiderItem()
        item['image_kid'] = response.xpath('//div[@class="Index_tit"]/strong/text()').extract_first()
        if item['image_kid'] == '标志大全':
            item['image_kid'] = '其他'
        item['image_name'] = response.xpath('//div[@class="fl-left hidden Color10"]/strong/text()').extract_first()
        item['image_link'] = response.xpath('//div[@class="fl-right hidden center"]/img/@src').extract_first()
        item['image_tags'] = response.xpath('//div[@class="hidden"]/a/text()').extract()
        curtime = time.strftime("%Y-%m-%d", time.localtime())
        # 通过对图片名称，时间戳，随机数三个数据进行加密生成指纹用于定义新图片名称，避免名称重复
        fp = hashlib.sha1()
        name = item['image_name']
        fp.update(name.encode())
        fp.update(t.encode())
        fp.update(rand.encode())
        fp = fp.hexdigest()
        if re.findall('(http://img.ibiaozhi.com/)', item['image_link']):
            item['image_from'] = re.findall('(http://img.(.*?)/)', item['image_link'])[0]
            item['image_from'] = list(item['image_from'])[1]
        elif re.findall('http://www.ibiaozhi.com/', item['image_link']):
            item['image_from'] = re.findall('http://www.(.*?)/', item['image_link'])[0]
        i['image_from'] = item['image_from'].replace('.com', '')

        item['image_path'] = '/data/logo_images/' + i['image_from'] + '/' + curtime + '/' + item[
            'image_kid'] + '/' + fp + '.' + \
                             item['image_link'].split('.')[-1]
        print('%s类商标信息：正在下载中............' % str(item['image_kid']))
        print(item)

        yield i
        yield item
