# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class BrandDataItem(scrapy.Item):
    name = scrapy.Field()
    name_e = scrapy.Field()
    code_guazi = scrapy.Field()
    first = scrapy.Field()

class CarDataItem(scrapy.Item):
    name = scrapy.Field()
    brand_id = scrapy.Field()
    code_guazi = scrapy.Field()
    type = scrapy.Field()

class ModelDataItem(scrapy.Item):
    name = scrapy.Field()
    car_id = scrapy.Field()
    price_new = scrapy.Field()

class SaleDataItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    shangpai_date = scrapy.Field()
    address = scrapy.Field()
    xingshi = scrapy.Field()
    price = scrapy.Field()
    price_new = scrapy.Field()

class ScrapyDataItem(scrapy.Item):
    brand_name = scrapy.Field()
    brand_first = scrapy.Field()
    car_name = scrapy.Field()
    car_type = scrapy.Field()
    model_name = scrapy.Field()
    price_new = scrapy.Field()
    url = scrapy.Field()
    shangpai_date = scrapy.Field()
    address = scrapy.Field()
    xingshi = scrapy.Field()
    price = scrapy.Field()

class GuaziItem(scrapy.Item):
    brand_name = scrapy.Field()
    brand_first = scrapy.Field()
    car_name = scrapy.Field()
    car_type = scrapy.Field()
    model_name = scrapy.Field()
    price_new = scrapy.Field()
    url = scrapy.Field()
    shangpai_date = scrapy.Field()
    address = scrapy.Field()
    xingshi = scrapy.Field()
    price = scrapy.Field()
