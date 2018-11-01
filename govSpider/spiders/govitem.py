# -*- coding: utf-8 -*-
import scrapy
import re
import json


class GovitemSpider(scrapy.Spider):
    name = "govitem"
    allowed_domains = ["gov.cn"]
    start_urls = ['http://gov.cn/']
    annNum = 1586
    item_page = 7592


    def start_requests(self):
        return [scrapy.FormRequest('http://sbgg.saic.gov.cn:9080/tmann/annInfoView/annSearchDG.html',
                                   callback=self.parse,
                                   formdata={'page': str(self.item_page), 'rows': '20', 'annNum': str(self.annNum)})]

    def parse(self, response):
        # 商标信息：
        print(response.status)
        image_items = re.findall(',"rows":\[(.*)\]}', response.text)[0]
        if len(image_items) > 0:
            items = image_items.split('},')
            image_items = [i.strip('{') for i in items]
            for item in image_items:
                if item.endswith('}'):
                    item = '{' + str(item)
                else:
                    item = '{' + str(item) + '}'
                item = json.loads(item)
                item['image_path'] = '/data/Brand_images' + '/' + '商标总局' + '/' + str(self.annNum) + '/' + str(
                    item['page_no']) + '.jpg'

                print(item)
                yield item


            self.item_page += 1
            print('正在下载 第%s期商标信息：第%s页' % (self.annNum, self.item_page))
            yield scrapy.FormRequest('http://sbgg.saic.gov.cn:9080/tmann/annInfoView/annSearchDG.html',
                                     callback=self.parse,
                                     formdata={'page': str(self.item_page), 'rows': '20', 'annNum': str(self.annNum)})

        else:

            print('*****************%s期商标:  下载完毕***********************' % self.annNum)
            self.item_page = 1
            if self.annNum < 1600:
                self.annNum += 1
                yield scrapy.FormRequest('http://sbgg.saic.gov.cn:9080/tmann/annInfoView/annSearchDG.html',
                                         callback=self.parse, formdata={'page': str(self.item_page), 'rows': '20',
                                                                        'annNum': str(self.annNum)})
