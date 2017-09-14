# -*- coding: utf-8 -*-
import scrapy


class GuaziAreaSpider(scrapy.Spider):
    name = 'guazi_area'
    allowed_domains = ['www.guazi.com']
    start_urls = ['http://www.guazi.com/']

    def parse(self, response):
        pass
