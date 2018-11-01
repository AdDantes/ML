# -*- coding: utf-8 -*-
import scrapy
import re
import time
import hashlib
import random
from ..items import LogodownloadItem, LogospiderItem
from copy import deepcopy



class DoooorSpider(scrapy.Spider):
    name = "doooor"
    allowed_domains = ["doooor.com","nihaologo.com"]
    start_urls = ['http://logo.doooor.com/tags']

    def parse(self, response):
        i = LogodownloadItem()
        item = LogospiderItem()
        a_list = response.xpath('//div[@class="tagslist"]/ul/li/a')
        for a in a_list:
            kid_url = a.xpath('./@href').extract_first()
            i['image_kid'] = a.xpath('./text()').extract_first()
            item['image_kid'] = a.xpath('./text()').extract_first()
            yield scrapy.Request(kid_url, callback=self.parse_list, meta={'i': deepcopy(i), 'item': deepcopy(item)},
                                 dont_filter=True)

    def parse_list(self, response):
        i = response.meta['i']
        item = response.meta['item']
        dt_list = response.xpath('//div[@class="excerpts"]/article/a')
        for dt in dt_list:
            detail_url = dt.xpath('./@href').extract_first()
            yield scrapy.Request(detail_url, callback=self.parse_item, meta={'i': deepcopy(i), 'item': deepcopy(item)})
        # 列表页翻页
        next_url = response.xpath('//div[@class="pagination pagination-multi"]/ul/li//a[text()="下一页"]/@href').extract_first()
        if next_url is not None:
            yield scrapy.Request(next_url, callback=self.parse_list, meta={'i': deepcopy(i), 'item': deepcopy(item)},
                                 dont_filter=True)

    def parse_item(self, response):
        t = str(int(time.time()))
        rand = str(random.randint(0, 100000))

        i = response.meta['i']
        item = response.meta['item']

        i['image_names'] = response.xpath('//h1[@class="article-title"]/text()').extract()
        i['image_urls'] = response.xpath('//article[@class="article-content"]/p/img/@src').extract()
        i['current_time'] = t
        i['randint'] = rand

        item['image_name'] = response.xpath('//h1[@class="article-title"]/text()').extract_first()
        item['image_link'] = response.xpath('//article[@class="article-content"]/p/img/@src').extract_first()
        item['image_tags'] = response.xpath('//div[@class="article-tags"]/a/text()').extract()
        curtime = time.strftime("%Y-%m-%d", time.localtime())
        # 通过对图片名称，时间戳，随机数三个数据进行加密生成指纹用于定义新图片名称，避免名称重复
        fp = hashlib.sha1()
        name = item['image_name']
        fp.update(name.encode())
        fp.update(t.encode())
        fp.update(rand.encode())
        fp = fp.hexdigest()

        item['image_from'] = re.findall('http://pic.(.*?)/', item['image_link'])[0]
        i['image_from'] = re.findall('http://pic.(.*?).com/', item['image_link'])[0]
        item['image_path'] = '/data/logo_images/' + i['image_from'] + '/' + curtime + '/' + item[
            'image_kid'] + '/' + fp + '.' + \
                             item['image_link'].split('.')[-1]
        print('%s类商标信息：正在下载中............' % str(item['image_kid']))
        print(item)
        yield i
        yield item

