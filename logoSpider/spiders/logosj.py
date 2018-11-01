# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import time
import hashlib
import random
from ..items import LogodownloadItem, LogospiderItem



class LogosjSpider(CrawlSpider):
    name = 'logosj'
    allowed_domains = ['logosj.com']
    start_urls = ['http://www.logosj.com/list_5_1.html#']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//dl/dt/a',)), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="pages_sub"]',)), follow=True),
    )

    def parse_item(self, response):
        t = str(int(time.time()))
        rand = str(random.randint(0, 100000))

        i = LogodownloadItem()
        item = LogospiderItem()

        i['image_kid'] = '其他'
        i['image_names'] = response.xpath('//div[@class="keywords_title"]/span/text()').extract()

        i['current_time'] = t
        i['randint'] = rand

        item['image_kid'] = '其他'
        item['image_name'] = response.xpath('//div[@class="keywords_title"]/span/text()').extract_first()
        item['image_link'] = response.xpath('//div[@class="my_Sharer_left"]/dl/dt/img/@src').extract_first()
        item['image_link'] = 'http://www.logosj.com/' + str(item['image_link'])
        i['image_urls'] = [item['image_link']]
        item['image_tags'] = response.xpath('//div[@class="my_Sharer_left"]/dl/dd/div[4]/a/text()').extract()
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

