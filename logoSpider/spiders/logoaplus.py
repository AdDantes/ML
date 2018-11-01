# -*- coding: utf-8 -*-
import scrapy
import re
import time
import hashlib
import random
from ..items import LogodownloadItem, LogospiderItem



class LogoaplusSpider(scrapy.Spider):
    name = "logoaplus"
    allowed_domains = ["logoaplus.com"]
    start_urls = ['http://www.logoaplus.com/logo/list/']

    def parse(self, response):
        i =LogodownloadItem()
        t = str(int(time.time()))
        rand = str(random.randint(0, 100000))
        image_list = response.xpath('//ul[@class="logo-list"]/li/span')
        i['image_names'] = []
        i['image_urls'] = []
        for image in image_list:
            image_name= image.xpath('./a[@class="title"]/text()').extract_first().replace(' ', '').split()[0]
            i['image_names'].append(image_name)
            # print(i['image_names'])
            image_urls = image.xpath('./a[@class="thumb"]/svg/g/image[1]').extract_first()
            image_url = re.findall('xlink:href="(.*?)">', image_urls)[0]
            image_urls = 'http://www.logoaplus.com' + image_url
            i['image_urls'].append(image_urls)
            # print(i['image_urls'])
            i['image_kid'] = image.xpath('./span[@class="trade"]/text()').extract()[0].replace('/', ',').split(',')[0]
            i['current_time'] = t
            i['randint'] = rand
            i['image_from'] = self.name
            yield i

            item = LogospiderItem()
            item['image_name'] = image.xpath('./a[@class="title"]/text()').extract_first().replace(' ', '')
            image_urls = image.xpath('./a[@class="thumb"]/svg/g/image[1]').extract_first()
            image_urls = re.findall('xlink:href="(.*?)"', image_urls)[0]
            item['image_link'] = 'http://www.logoaplus.com' + image_urls
            item['image_tags'] = image.xpath('./a[@class="title"]/text()').extract_first().split(' ')
            curtime = time.strftime("%Y-%m-%d", time.localtime())
            # 通过对图片url，时间戳，随机数三个数据进行加密生成指纹用于定义新图片名称，避免名称重复
            fp = hashlib.sha1()
            name = item['image_link']
            fp.update(name.encode())
            fp.update(t.encode())
            fp.update(rand.encode())
            fp = fp.hexdigest()

            item['image_kid'] = image.xpath('./span[@class="trade"]/text()').extract()[0].replace('/', ',').split(',')
            print(item['image_kid'])
            item['image_from'] = self.name
            i['image_from'] = self.name
            item['image_path'] = '/data/logo_images/' + i['image_from'] + '/' + curtime + '/' + item['image_kid'][
                0] + '/' + fp + '.' + item['image_link'].split('.')[-1]
            print(item)
            yield item


        next_url = response.xpath(
            '//div[@class="text-center"]/ul[@class="pagination"]/li/a[@class="next-page"]/@href').extract_first()
        if next_url is not None:
            next = 'http://www.logoaplus.com/logo/list/' + str(next_url)
            yield scrapy.Request(next, callback=self.parse)
