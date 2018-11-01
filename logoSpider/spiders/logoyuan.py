# -*- coding: utf-8 -*-
import scrapy
import re
import time
import hashlib
import random
from ..items import LogodownloadItem, LogospiderItem
from copy import deepcopy


class LogoyuanSpider(scrapy.Spider):
    name = "logoyuan"
    allowed_domains = ["logoyuan.com"]
    start_urls = ['http://logoyuan.com/xiaoguotu/']
    curren_page = 1

    def parse(self, response):
        i = LogodownloadItem()
        item = LogospiderItem()
        li_list = response.xpath('//h3[text()="其他分类"]/../ul[@class="list-inline list-paddingleft-2"]/li')
        for li in li_list:
            kid_url = li.xpath('./a/@href').extract_first()
            i['image_kid'] = li.xpath('./a/text()').extract_first()
            item['image_kid'] = li.xpath('./a/text()').extract_first()
            yield scrapy.Request(kid_url, callback=self.parse_list, meta={'i': deepcopy(i), 'item': deepcopy(item)},
                                 dont_filter=True)

    def parse_list(self, response):
        i = response.meta['i']
        item = response.meta['item']
        a_list = response.xpath('//div[@class="row news"]//div[@class="news-box tags"]/a')
        for a in a_list:
            detail_url = a.xpath('./@href').extract_first()
            yield scrapy.Request(detail_url, callback=self.parse_item, meta={'i': deepcopy(i), 'item': deepcopy(item)})
        next_url = response.xpath('//ul/li[2]/a[text()=" 下页 "]/@href').extract_first()

        if next_url is not None:
            yield scrapy.Request(next_url, callback=self.parse_list, meta={'i': deepcopy(i), 'item': deepcopy(item)},
                                 dont_filter=True)

    def parse_item(self, response):
        t = str(int(time.time()))
        rand = str(random.randint(0, 100000))

        i = response.meta['i']
        item = response.meta['item']

        i['image_names'] = response.xpath('//h2[@class="title"]/text()').extract()
        i['image_urls'] = response.xpath('//figure[@class="col-xs-12 col-sm-4 col-md-4 col-lg-4 "]/img/@src').extract()
        i['current_time'] = t
        i['randint'] = rand

        item['image_name'] = response.xpath('//h2[@class="title"]/text()').extract_first()
        item['image_link'] = response.xpath(
            '//figure[@class="col-xs-12 col-sm-4 col-md-4 col-lg-4 "]/img/@src').extract_first()
        item['image_tags'] = response.xpath(
            '//html/body/main/div/section[1]/div/article[1]/div/figure[2]/h5[4]/a[text()!="更多"]/text()').extract()
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
