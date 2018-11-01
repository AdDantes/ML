# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re

class MonoSpider(CrawlSpider):
    name = 'mono'
    allowed_domains = ['icooon-mono.com']
    start_urls = ['http://icooon-mono.com/?lang=en']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//ul[@id="categoryNav"]/li',)),follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//div[@id="topMaincolumn"]/ul/li/a',)),callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//div[@id="wp_page_numbers"]',)),follow=True),
    )

    def parse_item(self, response):
        item = {}
        item['name'] = response.xpath('//div[@id="imgDetail"]/h1/text()').extract_first()
        item['kid'] = response.xpath('//div[@id="imgDetail"]/p[@class="pankuzu"]/a[2]/text()').extract_first()
        # print(response.url)
        svg_id = re.findall('http://icooon-mono.com/(\d+)-',response.url)[0]
        # print(svg_id)
        yield scrapy.Request('http://icooon-mono.com/i/icon_%s/icon_%s0.svg'%(svg_id,svg_id),callback=self.parse_svg,meta={'item':item})

    def parse_svg(self, response):
        item = response.meta['item']
        item['svg'] = response.body.decode()
        print(item)
        # yield item