# -*- coding: utf-8 -*-
import scrapy
import re
import time
import random
import hashlib

from ..items import LogospiderItem, LogodownloadItem


class SilhousetteAcSpider(scrapy.Spider):
    name = "silhousette-ac"
    allowed_domains = ["silhouette-ac.com"]
    start_urls = ['https://zh-cn.silhouette-ac.com/category/%E4%BA%BA%E7%89%A9']
    current_page = 1
    kids = ['人物', '运输', '动物', '在水生物', '昆虫', '木/叶子', '花', '季节/假期花', '音乐', '食品及饮料', '风景/建筑物',
            '运动', '贺年片','图标','否则']
    current = 0
    kid = kids[current]

    def start_requests(self):
        return [scrapy.Request('https://data.api.photo-ac.com/category/data?page=%s&slug=%s&lang=zh-cn&max_results=100&service_type=silhouette_ac'%(self.current_page,self.kid))]

    def parse(self, response):
        t = str(int(time.time()))
        rand = str(random.randint(0, 100000))

        i = LogodownloadItem()  # logo素材图片下载
        i['image_urls'] = re.findall('"thumbnail":"(.*?)",', response.text)
        image_names = re.findall('"title_zh-cn":"(.*?)",', response.text)
        c_num = 0
        i['image_names'] = []
        for image_name in image_names:
            if image_name in i['image_names']:
                image_name = image_name+str(c_num)
                c_num+=1
                i['image_names'].append(image_name)
            else:
                i['image_names'].append(image_name)
        i['image_kid'] = self.kid
        i['current_time'] = t
        i['randint'] = rand
        print(str(i))
        print('%s类logo素材：正在下载中.........第%d页' % (self.kid, self.current_page))

        item = LogospiderItem()  # logo素材信息

        result_list_tuple = re.findall("'image_names': (.*?),'image_urls': (.*?),", str(i))
        print(result_list_tuple)
        print('%s类logo信息：正在下载中.........第%d页' % (self.kid, self.current_page))


            # item['image_link'] = result_tuple[1]
            # item['image_tags'] = result_tuple[0]
            # item['image_kid'] = self.kid
            # curtime = time.strftime("%Y-%m-%d", time.localtime())
            # # 通过对图片名称，时间戳，随机数三个数据进行加密生成指纹用于定义新图片名称，避免名称重复
            # fp = hashlib.sha1()
            # name = item['image_name']
            # fp.update(name.encode())
            # fp.update(t.encode())
            # fp.update(rand.encode())
            # fp = fp.hexdigest()
            # item['image_from'] = self.allowed_domains[0]
            # i['image_from'] = self.name
            # item['image_path'] = '/data/logo_images/' + i['image_from'] + '/' + curtime + '/' + \
            #                      item['image_kid'] + '/' + fp + '.' + \
            #                      item['image_link'].split('.')[-1]
            #
            # print(item)
            # yield i
            # yield item

        # try:
        #     if len(result_list_tuple) > 0:
        #         self.current_page += 1
        #         yield scrapy.FormRequest('http://www.logosc.cn/api/searchIconsByKeywords',
        #                                  formdata={'keywords': self.kid, 'page': str(self.current_page)})
        #     else:
        #         print('*****************%s类Logo素材:  下载完毕***********************' % self.kid)
        #
        #         self.current_page = 1
        #         self.current += 1
        #         self.kid = self.kids[self.current]
        #         yield scrapy.FormRequest('http://www.logosc.cn/api/searchIconsByKeywords',
        #                                  formdata={'keywords': self.kid, 'page': str(self.current_page)})
        # except:
        #     pass
