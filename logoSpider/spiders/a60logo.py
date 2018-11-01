# -*- coding: utf-8 -*-
import scrapy


class A60logoSpider(scrapy.Spider):
    name = "60logo"
    allowed_domains = ["60logo.com"]
    start_urls = ['http://www.60logo.com/index.php?m=model&a=index&cid=5&p=1']

    def parse(self, response):
        item = {}
        dl_list = response.xpath('//div[@id="container"]/dl')
        for dl in dl_list:
            item['name'] = dl.xpath('.//p/a/text()').extract_first()
            item['svg'] = '<!--?xml version="1.0" encoding="utf-8"?-->\n' + dl.xpath('./a/dt/div/svg').extract_first()
            print(item)
            yield item


        next_url = response.xpath('//div[@id="pages"]/a[text()="下一页"]/@href').extract_first()
        next_url = 'http://www.60logo.com'+next_url
        if next_url is not None:
            yield scrapy.Request(next_url,callback=self.parse,dont_filter=True)