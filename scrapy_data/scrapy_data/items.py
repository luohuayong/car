# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyDataItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    shangpai_date = scrapy.Field()
    address = scrapy.Field()
    xingshi = scrapy.Field()
    price = scrapy.Field()
    price_new = scrapy.Field()

