# -*- coding: utf-8 -*-
import scrapy
import re
import time
import hashlib
import random
from ..items import LogodownloadItem, LogospiderItem
from copy import deepcopy


class CnlogoSpider(scrapy.Spider):
    name = "cnlogo"
    allowed_domains = ["cnlogo8.com"]
    start_urls = ['http://www.cnlogo8.com/logoshouji/']

    def parse(self, response):
        i = LogodownloadItem()
        item = LogospiderItem()

        kid_list = response.xpath('//div[@class="logonav"]/a[text()="全部"]/following-sibling::*')
        for kid in kid_list:
            kid_url = kid.xpath('./@href').extract_first()
            kid_url = 'http://www.cnlogo8.com' + kid_url
            i['image_kid'] = kid.xpath('./text()').extract_first()
            item['image_kid'] = kid.xpath('./text()').extract_first()
            yield scrapy.Request(kid_url, callback=self.parse_list, meta={'i': deepcopy(i), 'item': deepcopy(item)},
                                 dont_filter=True)

    def parse_list(self, response):
        i = response.meta['i']
        item = response.meta['item']
        a_list = response.xpath('//ul[@class="plist sjpiclist"]/li/a')
        for a in a_list:
            detail_url = a.xpath('./@href').extract_first()
            detail_url = 'http://www.cnlogo8.com' + detail_url
            yield scrapy.Request(detail_url, callback=self.parse_item, meta={'i': deepcopy(i), 'item': deepcopy(item)})
        # 列表页翻页
        next_url = response.xpath('//div[@id="pages"]//a[text()="下一页"]/@href').extract_first()
        next_url = 'http://www.cnlogo8.com' + str(next_url)
        if next_url is not None:
            yield scrapy.Request(next_url, callback=self.parse_list, meta={'i': deepcopy(i), 'item': deepcopy(item)},
                                 dont_filter=True)

    def parse_item(self, response):
        t = str(int(time.time()))
        rand = str(random.randint(0, 100000))

        i = response.meta['i']
        item = response.meta['item']

        i['image_names'] = response.xpath('//div[@class="info"]/h1/text()').extract()
        i['image_urls'] = response.xpath('//div[@class="content"]/div[@class="img"]/img/@src').extract()
        i['image_urls'] = ['http://www.cnlogo8.com' + i for i in i['image_urls']]
        i['current_time'] = t
        i['randint'] = rand

        item['image_name'] = response.xpath('//div[@class="info"]/h1/text()').extract_first()
        item['image_link'] = response.xpath('//div[@class="content"]/div[@class="img"]/img/@src').extract_first()
        if not re.match('http', str(item['image_link'])):
            item['image_link'] = 'http://www.cnlogo8.com' + str(item['image_link'])
        item['image_tags'] = response.xpath('//div[@class="info"]/ul/li[3]/a/text()').extract()
        curtime = time.strftime("%Y-%m-%d", time.localtime())
        # 通过对图片名称，时间戳，随机数三个数据进行加密生成指纹用于定义新图片名称，避免名称重复
        fp = hashlib.sha1()
        name = str(item['image_name'])
        fp.update(name.encode())
        fp.update(t.encode())
        fp.update(rand.encode())
        fp = fp.hexdigest()

        item['image_from'] = re.findall('http://www.(.*?).com/', item['image_link'])[0] if re.findall(
            'http://www.(.*?).com/', item['image_link']) else 'cnlogo8'
        i['image_from'] = re.findall('http://www.(.*?).com/', item['image_link'])[0] if re.findall(
            'http://www.(.*?).com/', item['image_link']) else 'cnlogo8'
        item['image_path'] = '/data/logo_images/' + i['image_from'] + '/' + curtime + '/' + item[
            'image_kid'] + '/' + fp + '.' + \
                             item['image_link'].split('.')[-1]
        print('%s类商标信息：正在下载中............' % str(item['image_kid']))

        # print(item)
        # yield i
        # yield item
