# -*- coding: utf-8 -*-
import scrapy


class GuaziPinpaiSpider(scrapy.Spider):
    name = 'guazi_pinpai'
    allowed_domains = ['www.guazi.com']
    start_urls = ['http://www.guazi.com/']

    def parse(self, response):
        pass