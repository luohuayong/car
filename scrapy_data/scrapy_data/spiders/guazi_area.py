# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.selector import Selector
import logging
import json

class GuaziAreaSpider(scrapy.Spider):
    name = 'guazi_area'
    allowed_domains = ['www.guazi.com']
    start_urls = ['https://www.guazi.com/wh/sell']

    cookies = {'antipas': '57Z575218968bL6r20iIe1E1B2'}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, cookies=self.cookies, headers=self.headers, callback=self.parse_province)

    def parse_province(self, response):
       for item in response.xpath("//li[@class='com-li gj_dispro']").extract():
           province_id = Selector(text=item).xpath("//li/@pronum").extract_first()
           province_name = Selector(text=item).xpath("//li/text()").extract_first()
           url = "https://www.guazi.com/bj/sell?act=ajaxGetEvaluCity&province_id={0}".format(province_id)
           yield Request(url=url, cookies=self.cookies, headers=self.headers, callback=self.parse_city,
                         meta={'province_id': province_id, 'province_name': province_name})

    def parse_city(self, response):
        jsonresponse = json.loads(response.body)
        for item in jsonresponse:
            yield {
                'province_id': response.meta['province_id'],
                'province_name': response.meta['province_name'],
                'city_id': item['id'],
                'city_name': item['name']
            }


