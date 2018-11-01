# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import SvgItem
from scrapy_redis.spiders import RedisSpider


class FlaticonSpider(scrapy.Spider):
    name = 'flaticon'
    allowed_domains = ['flaticon.com']
    start_urls = ['https://www.flaticon.com/packs/200']

    def parse(self, response):
        a_list = response.xpath('//section[@class="search-result"]//section[@class="box-container"]/article/a')
        for a in a_list:
            box_href = a.xpath('./@href').extract_first()
            yield scrapy.Request(box_href,callback=self.parse_box)

        next_url = response.xpath('//div[@class="pagination"]/a[@id="pagination-more"]/@href').extract_first()
        page_no = re.findall('https://www.flaticon.com/packs/(\d+)$',next_url)[0]
        if next_url is not None and int(page_no) <500:
            print('正在爬取{}............'.format(next_url))
            yield scrapy.Request(next_url,callback=self.parse,dont_filter=True)

    def parse_box(self,response):
        a_list = response.xpath('//section[@class="search-result"]/ul[@class="icons"]/li/div[@class="icon--holder"]/div[@class="overlay"]/a')
        for a in a_list:
            image_href = a.xpath('./@href').extract_first()
            yield scrapy.Request(image_href, callback=self.parse_image)

    def parse_image(self,response):
        item = SvgItem()
        item['kid_name'] = response.xpath('//div[@class="group group-pack"]/a/@title').extract_first()
        item['svg_name'] = re.findall('https://www.flaticon.com/.*/(.*?)$',response.url)[0]
        # print(item)
        image_url = response.xpath('//div[@class="gallery"]/div[@class="img-version"]/div[@class="main-icon"]/img/@src').extract_first()
        yield scrapy.Request(image_url,callback=self.parse_svg,meta={'item':item})

    def parse_svg(self,response):
        try:
            item = response.meta['item']

            item['svg'] = response.text
            # print(item)
            yield item
        except:
            pass