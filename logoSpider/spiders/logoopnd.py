# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import time
import hashlib
import random
from ..items import LogodownloadItem, LogospiderItem


class LogoopndSpider(CrawlSpider):
    name = 'logoopnd'
    allowed_domains = ['logopond.com']
    start_urls = ['https://logopond.com/gallery/list/?gallery=featured&month=&year=&filter=N']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="row pushtop"]/ul[@class="large-12 medium-12 tween-12 small-12 row  logo_list"]/li[@class="large-2 medium-3 tween-4 small-6 lcolumns mcolumns tcolumns scolumns logo_gallery_container"]/div[@class="block"]/div[@class="logo_image"]/a[@class="metastats shide"]',)),callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="pagination  large-12 medium-12 tween-12 small-12"]/div[@class="large-6 medium-6 tween-6 small-6 lcolumns mcolumns tcolumns scolumns lright mright tright sright"]/a[text()="next"]',)), follow=True),
    )

    def parse_item(self, response):
        t = str(int(time.time()))
        rand = str(random.randint(0, 100000))
        i = LogodownloadItem()
        image_names = response.xpath('//div[@id="logo_info_title"]/div[@class="detail_header large-12 medium-12 tween-12 small-12"]/h2/text()').extract_first()
        image_names = image_names.replace('\n','')
        i['image_names'] = [image_names]
        image_urls = response.xpath('//div[@id="logo_info_title"]//img/@src').extract_first()
        i['image_urls'] = ['https://logopond.com/'+str(image_urls)]
        i['image_kid'] = '其他'
        i['image_from'] = self.name
        i['current_time'] =t
        i['randint'] = rand
        # print(i)

        item = LogospiderItem()

        item['image_name'] =image_names.replace('\n','')
        # print(item['image_name'])
        item['image_link'] ='https://logopond.com/'+str(image_urls)

        curtime = time.strftime("%Y-%m-%d", time.localtime())
        fp = hashlib.sha1()
        name = item['image_name']
        fp.update(name.encode())
        fp.update(t.encode())
        fp.update(rand.encode())
        fp = fp.hexdigest()

        item['image_kid'] = '其他'
        item['image_tags'] = response.xpath('//div[@id="logo_info_title"]/div[4]/p[4]/a/text()').extract()
        if item['image_tags'] is not None:
            item['image_tags'] =[i.strip() for i in item['image_tags'] if i != '\n']
        else:
            item['image_tags'] = response.xpath('//div[@id="logo_info_title"]/div[3]/p[4]/a/text()').extract()
            item['image_tags'] = [i.strip() for i in item['image_tags']]
        item['image_from'] = self.name
        item['image_path'] =item['image_path'] = item['image_path'] = '/data/logo_images/' + i['image_from'] + '/' + curtime + '/' + item[
            'image_kid'] + '/' + fp + '.' + \
                                                  item['image_link'].split('.')[-1]
        print(item)
        yield i
        yield item