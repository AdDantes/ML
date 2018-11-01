# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy
import re
from ..items import SvgItem


class FreesvgiconSpider(scrapy.Spider):
    name = 'freesvgicon'
    allowed_domains = ['freesvgicon.com']
    start_urls = ['https://freesvgicon.com/683']

    def parse(self, response):
        try:
            kid_list = response.xpath('//div[@class="container"]//div[@class="column is-one-quarter"]/a')
            i = SvgItem()
            for kid in kid_list:
                kid_link = kid.xpath('./@href').extract_first()
                i['kid_name'] = kid.xpath('.//div[@class="icon-pack-card-meta"]/h3/text()').extract_first()
                kid_link = 'https://freesvgicon.com' + kid_link
                yield scrapy.Request(kid_link, callback=self.parse_item, meta={'i': deepcopy(i)})
        except:
            print('403')

        next_url = response.xpath(
            '//nav[@class="pagination is-centered list-paginator"]/a[@class="pagination-next"]/@href').extract_first()
        print('正在下载第%s页' % next_url)
        next_url = 'https://freesvgicon.com' + next_url

        if next_url is not None:
            yield scrapy.Request(next_url, callback=self.parse, dont_filter=True)

    def parse_item(self, response):
        i = response.meta['i']
        img_list = response.xpath('//div[@class="icons-grid"]/div[@class="icon-item"]')
        for img in img_list:
            img_link = img.xpath('./div[@class="icon-item-cover"]/a/@href').extract_first()
            i['img_name'] = re.findall("/.*?/(.*?).svg", img_link)[0] if len(
                re.findall("/.*?/(.*?).svg", img_link)) > 0 else None
            img_link = 'https://freesvgicon.com' + img_link
            yield scrapy.Request(img_link, self.parse_svg, meta={'i': deepcopy(i)})

    def parse_svg(self, response):
        i = response.meta['i']
        i['svg'] = response.body.decode()
        print(i)
        # yield i

