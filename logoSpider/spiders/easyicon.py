# -*- coding: utf-8 -*-
import scrapy
import re
from copy import deepcopy
from ..items import SvgItem

class EasyiconSpider(scrapy.Spider):
    name = 'easyicon'
    allowed_domains = ['easyicon.net']
    start_urls = ['https://www.easyicon.net/update/1']

    def parse(self, response):
        item = SvgItem()
        h_list = response.xpath('//div[@id="container"]/h3')
        for h3 in h_list:
            list_url = h3.xpath('./a/@href').extract_first()
            list_url = 'https://www.easyicon.net'+list_url
            item['kid_name'] = h3.xpath('./a/text()').extract_first()
            date = h3.xpath('./span/text()').extract_first()
            addedTime = re.findall('Added time：(.*?) ',date)[0]
            item['add_path'] = addedTime.replace('-','\\')
            # print(item)
            yield scrapy.Request(list_url,callback=self.parse_list,meta={'item':deepcopy(item)})

        next_url = response.xpath('//div[@class="all_num"]/a[@class="cur"]/following-sibling::a[1]/@href').extract_first()
        if next_url is not None:
            next_url = 'https://www.easyicon.net' + next_url
            print(next_url)
            print('**********************')
            yield scrapy.Request(next_url, callback=self.parse, meta={'item':deepcopy(item)})



    def parse_list(self,response):
        item = response.meta['item']
        li_list = response.xpath('//div[@id="result_right_layout"]/div/ol/li')
        for li in li_list:
            svg = li.xpath('./div[@class="svg"]/a/@href').extract_first()
            title = li.xpath('./div[@class="pd_img"]/div/a/@title').extract_first()
            if svg is not None:
                tm_name = re.findall('svg/(.*?)$',svg)[0] if len(re.findall('svg/(.*?)$',svg))>0 else None
                tm_name = tm_name.replace('/','')
                item['svg_name'] = title+'_'+tm_name
                yield scrapy.Request(svg,callback=self.parse_svg,meta={'item':deepcopy(item)})

                # print(svg)
                print(item)
        next_url = response.xpath('//div[@class="pages_all"]//span//following-sibling::a[1]/@href').extract_first()
        if next_url is not None:
            # print(response.request.url)
            next_url = 'https://www.easyicon.net'+next_url
            # print(next_url)
            yield scrapy.Request(next_url,callback=self.parse_list,meta={'item':deepcopy(item)})

    def parse_svg(self,response):
        item = response.meta['item']
        item['svg'] = response.text
        # print(item)
        yield item