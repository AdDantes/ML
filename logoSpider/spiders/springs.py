# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import re

class SpringsSpider(scrapy.Spider):
    name = 'springs'
    allowed_domains = ['graphicsprings.com']
    start_urls = ['https://www.graphicsprings.com/categories']

    def parse(self, response):
        item = {}
        li_list = response.xpath('//div[@class="row"]/ul[@class="category-list"]/li')
        for li in li_list:
            kid_link = li.xpath('./a/@href').extract_first()
            kid_link = 'https://www.graphicsprings.com' +str(kid_link)
            item['kid'] = li.xpath('./a/text()').extract_first().strip()
            yield scrapy.Request(kid_link,callback=self.parse_item,meta={'item':deepcopy(item)})

    def parse_item(self,response):
        item = response.meta['item']
        li_list = response.xpath('//div[@class="row"]/ul[@class="logos-gallery"]/li')
        for li in li_list:
            svg = li.xpath('./a/img/@src').extract_first()
            item['svg'] = 'https://www.graphicsprings.com' + svg
            item['name'] = li.xpath('./a/img/@alt').extract_first()
            # print(item)
            yield scrapy.Request(item['svg'],callback=self.parse_svg,meta={'item':deepcopy(item)})

        next_url = response.xpath('//div[@class="row"]/div/span/a[text()="Next page"]/@href').extract_first()
        if next_url is not None:
            next_url = 'https://www.graphicsprings.com' +str(next_url)
            # print(next_url)
            yield scrapy.Request(next_url,callback=self.parse_item,meta={'item':deepcopy(item)})

    def parse_svg(self, response):
        item = response.meta['item']
        item['svg'] = response.body.decode()
        print(item)
        yield item