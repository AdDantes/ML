# -*- coding: utf-8 -*-
import scrapy
import re
import time
import hashlib
import random
# from scrapy_redis.spiders import RedisSpider

from logoSpider.items import LogodownloadItem, LogospiderItem


class LogoidsSpider(scrapy.Spider):
    name = "logoids"
    allowed_domains = ["logoids.com"]
    # redis_key = 'brand:start_url'    #在redis中添加key：'brand:start_url'，value：http://www.logoids.com/，启动爬虫
    start_urls = ['http://www.logoids.com/']

    def parse(self, response):
        a_list = response.xpath('//div[@class="cell"]/h3/a')
        for a in a_list:
            detali_url = a.xpath('./@href').extract_first()
            yield scrapy.Request(detali_url, callback=self.parse_item)
        next_url = response.xpath('//div[@class="pager"]/a[text()="›"]/@href').extract_first()
        if next_url is not None:
            yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)

    def parse_item(self, response):
        t = str(int(time.time()))
        rand = str(random.randint(0, 100000))

        i = LogodownloadItem()  # 商标素材图片下载
        i['image_kid'] = response.xpath('//div[@class="position"]/a[3]/@title').extract_first()
        if i['image_kid'] is not None:
            if re.findall('家电', str(i['image_kid'])):
                i['image_kid'] = i['image_kid'].replace('/', '-')
        else:
            i['image_kid'] = response.xpath('//div[@class="position"]/a[2]/@title').extract_first()
        i['image_names'] = response.xpath('//div[@class="info"]/div[1]/h1/text()').extract()
        i['image_urls'] = response.xpath('//div[@class="thumb"]/img/@src').extract()
        i['current_time'] = t
        i['randint'] = rand
        image_url = response.xpath('//div[@class="thumb"]/img/@src').extract_first()
        if not re.match('http://www.logoids.com', image_url):
            i['image_urls'] = []
            image_url = 'http://www.logoids.com' + image_url
            i['image_urls'].append(image_url)
        print('%s类商标图片：正在下载中............' % str(i['image_kid']))

        item = LogospiderItem()  # 商标素材信息
        item['image_kid'] = response.xpath('//div[@class="position"]/a[3]/@title').extract_first()
        if item['image_kid'] is not None:
            if re.findall('家电', str(item['image_kid'])):
                item['image_kid'] = item['image_kid'].replace('/', '-')
        else:
            item['image_kid'] = response.xpath('//div[@class="position"]/a[2]/@title').extract_first()
        item['image_name'] = response.xpath('//div[@class="info"]/div[1]/h1/text()').extract_first()
        item['image_tags'] = response.xpath('//div[@class="item tags"]/a/@title').extract()
        item['image_link'] = response.xpath('//div[@class="thumb"]/img/@src').extract_first()
        if not re.match('http://www.logoids.com', item['image_link']):
            item['image_link'] = 'http://www.logoids.com' + item['image_link']
        curtime = time.strftime("%Y-%m-%d", time.localtime())
        # 通过对图片名称，时间戳，随机数三个数据进行加密生成指纹用于定义新图片名称，避免名称重复
        fp = hashlib.sha1()
        name = item['image_name']
        fp.update(name.encode())
        fp.update(t.encode())
        fp.update(rand.encode())
        fp = fp.hexdigest()
        # print(fp)
        item['image_from'] = re.findall('http://www.(.*?)/', item['image_link'])[0]
        i['image_from'] = re.findall('http://www.(.*?).com/', item['image_link'])[0]
        item['image_path'] = '/data/logo_images/' + i['image_from'] + '/' + curtime + '/' + item[
            'image_kid'] + '/' + fp + '.' + \
                             item['image_link'].split('.')[-1]

        print('%s类商标图片：正在下载中............' % str(item['image_kid']))

        print(item)
        yield i
        yield item
