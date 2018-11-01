# -*- coding: utf-8 -*-
import scrapy
import re


class TotalitemSpider(scrapy.Spider):
    name = "totalitem"
    allowed_domains = ["gov.cn"]
    start_urls = ['http://gov.cn/']

    annNum = 1
    i = 0

    def start_requests(self):
        return [scrapy.FormRequest('http://sbgg.saic.gov.cn:9080/tmann/annInfoView/annSearchDG.html',
                                   formdata={'page': '1', 'rows': '20', 'annNum': str(self.annNum)},meta={'i':self.i})]

    def parse(self, response):

        # 商标信息：
        i = response.meta['i']
        total_item = re.findall('{"total":(.*?),', response.text)[0]
        i += int(total_item)
        print('已统计至第%s期----共%s条数据'%(self.annNum,i))
        # print(i)
        # 翻公告期号
        self.annNum += 1
        yield scrapy.FormRequest('http://sbgg.saic.gov.cn:9080/tmann/annInfoView/annSearchDG.html',
                                   formdata={'page': '1', 'rows': '20', 'annNum': str(self.annNum)},meta={'i':i})

