# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import BranddownloadItem


class GovSpider(scrapy.Spider):
    name = "gov"
    allowed_domains = ["gov.cn"]
    start_urls = ['http://gov.cn/']
    annNum = 428
    img_page = 4
    item_page = 1

    def start_requests(self):
        return [scrapy.FormRequest('http://sbgg.saic.gov.cn:9080/tmann/annInfoView/selectInfoidBycode.html',
                                   formdata={'annNum': str(self.annNum), 'annTypecode': 'TMZCSQ'})]

    def parse(self, response):
        id = response.text
        image_name = 1
        yield scrapy.FormRequest('http://sbgg.saic.gov.cn:9080/tmann/annInfoView/imageView.html',
                                 formdata={'id': id, 'pageNum': str(self.img_page), 'flag': '1'},
                                 callback=self.parse_link, meta={'id': id, 'image_name': image_name})

    def parse_link(self, response):
        id = response.meta['id']
        image_name = response.meta['image_name']
        try:
            image_list = re.findall('"imaglist":\[(.*)\],', response.text)[0]
            list1 = image_list.split(',')
            image_urls = [i.strip('""') for i in list1]
        except:
            error = '未获取到第{}期商标图片'.format(self.annNum) + '\n'
            print(error)
            with open('D:\logo_crawler\logoSpider\image_log.txt', 'a', encoding='utf8') as f:
                f.write(error)
        else:
            yield scrapy.FormRequest('http://sbgg.saic.gov.cn:9080/tmann/annInfoView/annSearchDG.html',
                                     callback=self.parse_item,
                                     meta={'image_name': image_name, 'image_urls': image_urls, 'id': id},
                                     formdata={'page': str(self.item_page), 'rows': '20', 'annNum': str(self.annNum)})

    def parse_item(self, response):
        # 商标图片下载：
        item = BranddownloadItem()
        id = response.meta['id']
        image_link = response.meta['image_urls']
        item['image_link'] = image_link
        image_name = response.meta['image_name']
        item['image_kid'] = str(self.annNum)
        item['image_from'] = '商标总局'
        item['image_name'] = []
        for image_link in item['image_link']:
            item['image_name'].append(str(image_name))
            image_name += 1
        print(item)
        yield item

        # 同期翻页
        if len(image_link) > 2:
            self.img_page += 20
            self.item_page += 1
            print('正在下载 第%s期商标图片：第%s页' % (self.annNum, self.item_page))
            yield scrapy.FormRequest('http://sbgg.saic.gov.cn:9080/tmann/annInfoView/imageView.html',
                                     formdata={'id': id, 'pageNum': str(self.img_page), 'flag': '1'},
                                     callback=self.parse_link,
                                     meta={'id': id, 'image_name': image_name})

        # 翻公告期号
        else:
            print('*****************%s期商标:  下载完毕***********************' % self.annNum)
            self.img_page = 4
            self.item_page = 1
            if self.annNum < 700:
                self.annNum += 1
                yield scrapy.FormRequest('http://sbgg.saic.gov.cn:9080/tmann/annInfoView/selectInfoidBycode.html',
                                         formdata={'annNum': str(self.annNum), 'annTypecode': 'TMZCSQ'})
