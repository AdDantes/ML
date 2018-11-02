# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import math


class TongchengSpider(CrawlSpider):
    name = 'tongcheng'
    allowed_domains = ['58.com']
    start_urls = ['https://bj.58.com/chuzu/?PGTID=0d3090a7-0047-6ebd-fc60-2c7da572b7b7&ClickID=2']

    rules = (
        Rule(LinkExtractor(restrict_xpaths=('//dl[@class="secitem secitem_fist"]/dd/a',)), follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="listBox"]/ul[@class="listUl"]/li/div[@class="des"]/h2/a',)), callback='parse_item',
             follow=True),
        Rule(LinkExtractor(restrict_xpaths=('//div[@class="pager"]/a',)), follow=True),
    )

    def parse_item(self, response):
        i = {}
        i['Title'] = response.xpath('//div[@class="house-title"]/h1/text()').extract_first()
        rent = response.xpath('//div[@class="house-pay-way f16"]/span[1]/b/text()').extract_first()
        i['rent'] = int(rent)
        i['Payment_method'] = response.xpath('//div[@class="house-pay-way f16"]/span[2]/text()').extract_first()
        i['ret_method'] = response.xpath('//ul[@class="f14"]/li[1]/span[2]/text()').extract_first()
        house_type = response.xpath('//ul[@class="f14"]/li[2]/span[2]/text()').extract_first()
        i['house_type'] = re.findall('(.*?)   ', house_type)[0] if len(re.findall('(.*?)   ', house_type)) > 0 else None
        area = re.findall('    (.*?)       ', house_type)[0] if len(
            re.findall('    (.*?)       ', house_type)) > 0 else None
        i['area'] = float(area)
        i['Decoration'] = re.findall('平  (.*?)$', house_type)[0] if len(
            re.findall('平  (.*?)$', house_type)) > 0 else None
        Orientation = response.xpath('//ul[@class="f14"]/li[3]/span[2]/text()').extract_first()
        i['Orientation'] = re.findall('(.*?)  ', Orientation)[0] if len(
            re.findall('(.*?)  ', Orientation)) > 0 else None
        i['floor'] = re.findall('  (.*?)\/', Orientation)[0] if len(re.findall('  (.*?)\/', Orientation)) > 0 else None
        i['xiao_qu'] = response.xpath('//ul[@class="f14"]/li[4]/span[2]/a/text()').extract_first()
        i['Big_quYu'] = response.xpath('//ul[@class="f14"]/li[5]/span[2]/a[1]/text()').extract_first()
        i['detail_quYu'] = response.xpath('//ul[@class="f14"]/li[5]/span[2]/a[2]/text()').extract_first()
        metro_distance = response.xpath('//ul[@class="f14"]/li[5]/em/text()').extract_first()
        metro_distance = re.findall('\d+', metro_distance)[0] if len(
            re.findall('\d+', metro_distance)) > 0 else None
        i['metro_distance'] = int(metro_distance)
        i['house_disposal'] = response.xpath('//ul[@class="house-disposal"]//text()').extract()
        house_disposal = [i.replace('\n', '').replace(' ', '') for i in i['house_disposal'] if i != '']
        i['house_disposal'] = [i for i in house_disposal if i != '']
        print(i)
        yield i
