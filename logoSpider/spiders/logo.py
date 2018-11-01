# -*- coding: utf-8 -*-
import scrapy
import re
import time
import random
import hashlib

from ..items import LogospiderItem, LogodownloadItem


class LogoSpider(scrapy.Spider):
    name = 'logo'
    allowed_domains = ['logosc.cn']
    start_urls = ['http://logosc.cn/']
    current_page = 1
    kids = ['餐饮', '教育', '网络科技', '商务贸易', '金融', '购物休闲', '房地产', '艺术传媒', '建材家居', '运动健身', '医疗美容', '创意设计',
            '摄影摄像', '交通运输', '店铺网店', '工业制造', '影视音乐', '旅游酒店', '绿色环保', '社团机关', '宠物生活', '家政保洁', '婚庆礼仪',
            '农林牧渔', '母婴亲子']
    # kids = ['动物','儿童','线条','游戏','食品','建筑','综合','餐厅','网站','服饰','家居','卡通','极简']
    current = 0
    kid = kids[current]

    def start_requests(self):
        return [scrapy.FormRequest('http://www.logosc.cn/api/searchIconsByKeywords',
                                   formdata={'keywords': self.kid, 'page': str(self.current_page)})]

    def parse(self, response):
        t = str(int(time.time()))
        rand = str(random.randint(0, 100000))

        i = LogodownloadItem()  # logo素材图片下载
        image_links = re.findall('"imgpath":"(.*?)",', response.body.decode('unicode_escape'))
        i['image_names'] = re.findall('"icon_name":"(.*?)",', response.body.decode('unicode_escape'))
        i['image_urls'] = ['http://www.logosc.cn/' + str(i.replace('\\', '')) for i in image_links]
        i['image_kid'] = self.kid
        i['current_time'] = t
        i['randint'] = rand
        print('%s类logo素材：正在下载中.........第%d页' % (self.kid, self.current_page))

        item = LogospiderItem()  # logo素材信息
        img_name_img_path_tags = re.compile('"icon_name":"(.*?)","imgpath":"(.*?)","tags":"(.*?)"')
        result_list_tuple = re.findall(img_name_img_path_tags, response.body.decode('unicode_escape'))
        print('%s类logo信息：正在下载中.........第%d页' % (self.kid, self.current_page))
        for result_tuple in result_list_tuple:
            item['image_name'] = result_tuple[0]
            item['image_link'] = 'http://www.logosc.cn/' + str(result_tuple[1].replace('\\', ''))
            item['image_tags'] = result_tuple[2].split(',')
            item['image_kid'] = self.kid
            curtime = time.strftime("%Y-%m-%d", time.localtime())
            # 通过对图片名称，时间戳，随机数三个数据进行加密生成指纹用于定义新图片名称，避免名称重复
            fp = hashlib.sha1()
            name = item['image_name']
            fp.update(name.encode())
            fp.update(t.encode())
            fp.update(rand.encode())
            fp = fp.hexdigest()
            item['image_from'] = re.findall('http://www.(.*?)/', item['image_link'])[0]
            i['image_from'] = re.findall('http://www.(.*?).cn/', item['image_link'])[0]
            item['image_path'] = '/data/logo_images/' + i['image_from'] + '/' + curtime + '/' + \
                                 item['image_kid'] + '/' + fp + '.' + \
                                 item['image_link'].split('.')[-1]

            print(item)
            yield i
            yield item

        try:
            if len(result_list_tuple) > 0:
                self.current_page += 1
                yield scrapy.FormRequest('http://www.logosc.cn/api/searchIconsByKeywords',
                                         formdata={'keywords': self.kid, 'page': str(self.current_page)})
            else:
                print('*****************%s类Logo素材:  下载完毕***********************' % self.kid)

                self.current_page = 1
                self.current += 1
                self.kid = self.kids[self.current]
                yield scrapy.FormRequest('http://www.logosc.cn/api/searchIconsByKeywords',
                                         formdata={'keywords': self.kid, 'page': str(self.current_page)})
        except:
            pass
