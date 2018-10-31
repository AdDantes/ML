# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BranddownloadItem(scrapy.Item):
    image_link = scrapy.Field()
    image_name = scrapy.Field()
    image_from = scrapy.Field()
    image_kid = scrapy.Field()




