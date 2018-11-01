# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LogospiderItem(scrapy.Item):  # logo素材信息
    image_name = scrapy.Field()
    image_link = scrapy.Field()
    image_kid = scrapy.Field()
    image_tags = scrapy.Field()
    image_path = scrapy.Field()
    image_from = scrapy.Field()


class LogodownloadItem(scrapy.Item):  # logo图片下载
    image_names = scrapy.Field()
    image_urls = scrapy.Field()
    image_kid = scrapy.Field()
    image_from = scrapy.Field()
    current_time = scrapy.Field()
    randint = scrapy.Field()

class SvgItem(scrapy.Item):
    kid_name = scrapy.Field()
    svg_name = scrapy.Field()
    svg = scrapy.Field()
    # add_path = scrapy.Field()