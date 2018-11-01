# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import time
import hashlib
import random
from ..items import LogodownloadItem, LogospiderItem



class A16sucaiSpider(CrawlSpider):
    name = '16sucai'
    allowed_domains = ['16sucai.com']
    start_urls = ['http://www.16sucai.com/sjxs/bz/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="zhuanti_box"]//ul/li/a[1]',)),
             callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//div[@id="pages"]/a',)), follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//div[@id="pages"]/a',)), follow=True),
    )

    def parse_item(self, response):
        t = str(int(time.time()))
        rand = str(random.randint(0, 100000))

        i = LogodownloadItem()  # 商标素材图片下载
        i['image_kid'] = '其他'
        i['image_names'] = response.xpath('//div[@class="neirong_bt"]/h1/text()').extract()
        i['image_urls'] = response.xpath('//div[@class="endtext"]/p/img/@src').extract()
        i['current_time'] = t
        i['randint'] = rand

        item = LogospiderItem()  # 商标素材信息
        item['image_kid'] = '其他'
        item['image_name'] = response.xpath('//div[@class="neirong_bt"]/h1/text()').extract_first()
        item['image_tags'] = response.xpath('//div[@class="keyword2"]/span/text()').extract()
        p_list = response.xpath('//div[@class="endtext"]/p')
        c_img = 0
        for p in p_list:
            item['image_link'] = p.xpath('./img/@src').extract_first()

            curtime = time.strftime("%Y-%m-%d", time.localtime())
            # 通过对图片名称，时间戳，随机数三个数据进行加密生成指纹用于定义新图片名称，避免名称重复
            fp = hashlib.sha1()
            name = item['image_name'] + str(c_img)
            fp.update(name.encode())
            fp.update(t.encode())
            fp.update(rand.encode())
            fp = fp.hexdigest()

            item['image_from'] = re.findall('http://file\d+.(.*?)/', str(item['image_link']))[0] if re.findall('http://file\d+.(.*?)/', str(item['image_link'])) else None
            i['image_from'] = re.findall('http://file\d+.(.*?).com/', str(item['image_link']))[0] if re.findall('http://file\d+.(.*?).com/', str(item['image_link'])) else None
            item['image_path'] = '/data/logo_images/' + i['image_from'] + '/' + curtime + '/' + item[
                'image_kid'] + '/' + fp + '.' + \
                                 item['image_link'].split('.')[-1]
            c_img += 1
            print('%s类商标信息：正在下载中............' % str(item['image_kid']))

            print(item)
            yield i
            # yield item