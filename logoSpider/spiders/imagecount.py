# -*- coding: utf-8 -*-
import scrapy
import re

class ImagecountSpider(scrapy.Spider):
    name = "imagecount"
    allowed_domains = ["gov.cn"]
    start_urls = ['http://gov.cn/']
    annNum = 1496
    i = 0

    def start_requests(self):
        if self.annNum>72:
            return [scrapy.FormRequest('http://sbgg.saic.gov.cn:9080/tmann/annInfoView/selectInfoidBycode.html',
                                   formdata={'annNum': str(self.annNum), 'annTypecode': 'TMZCSQ'},meta={'i':self.i})]
        else:
            return [scrapy.FormRequest('http://sbgg.saic.gov.cn:9080/tmann/annInfoView/selectInfoidBycode.html',
                                       formdata={'annNum': str(self.annNum), 'annTypecode': 'TMZCZC'},
                                       meta={'i': self.i})]

    def parse(self, response):
        i = response.meta['i']
        id = response.text
        image_name = 1
        yield scrapy.FormRequest('http://sbgg.saic.gov.cn:9080/tmann/annInfoView/imageView.html',
                                 formdata={'id': id, 'pageNum': '1', 'flag': '1'},
                                 callback=self.parse_link, meta={'id': id, 'image_name': image_name,'i':i})

    def parse_link(self, response):
        i = response.meta['i']
        imagecount = re.findall(',"total":(.*?),', response.text)[0]
        i += int(imagecount)
        print('已统计至第%s期----共%s张图片' % (self.annNum, i))

        # 翻公告期号
        self.annNum += 1
        if self.annNum > 72:
            yield scrapy.FormRequest('http://sbgg.saic.gov.cn:9080/tmann/annInfoView/selectInfoidBycode.html',
                                    formdata={'annNum': str(self.annNum), 'annTypecode': 'TMZCSQ'},meta={'i':i})
        else:
            yield scrapy.FormRequest('http://sbgg.saic.gov.cn:9080/tmann/annInfoView/selectInfoidBycode.html',
                                     formdata={'annNum': str(self.annNum), 'annTypecode': 'TMZCZC'}, meta={'i': i})

