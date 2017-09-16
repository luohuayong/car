# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy import Selector
import json

class GuaziPinpaiSpider(scrapy.Spider):
    name = 'guazi_pinpai'
    allowed_domains = ['www.guazi.com']
    start_urls = ['https://www.guazi.com/wh/sell']

    cookies = {'antipas': '57Z575218968bL6r20iIe1E1B2'}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, cookies=self.cookies, headers=self.headers, callback=self.parse_brand)

    def parse_brand(self, response):
        # for item_p in response.xpath("//p[@class='s-tt']").extract():
        #     brand_first =
        for item_ul in response.xpath("//ul[@class='all-brand']").extract():
            for item in Selector(text=item_ul).xpath("//li").extract():
                brand_id = Selector(text=item).xpath("//li/@tagnum").extract_first()
                brand_name = Selector(text=item).xpath("//li/text()").extract_first()

                url = "https://www.guazi.com/bj/sell?act=ajaxgettaginfo&brandId={0}&needChild=1".format(brand_id)
                yield Request(url=url, cookies=self.cookies, headers=self.headers, callback=self.parse_car,
                          meta={'brand_id': brand_id, 'brand_name': brand_name})

    def parse_car(self, response):
        jsonresponse = json.loads(response.body)
        for key,item in jsonresponse['msg']:
            car_id = item['id']
            car_name = item['name']
            url = "https://www.guazi.com/bj/sell/?act=ajaxGetEvaluCheXing&tag_id={0}".format(car_id)
            yield Request(url=url, cookies=self.cookies, headers=self.headers, callback=self.parse_model,
                          meta={'brand_id': response.meta['brand_id'], 'brand_name': response.meta['brand_name'],
                                'car_id': car_id, 'car_name': car_name})

    def parse_model(self, response):
        jsonresponse = json.loads(response.body)
        for key,item in jsonresponse:
            yield{
                'brand_id': response.meta['brand_id'],
                'brand_name': response.meta['brand_name'],
                'brand_first': '',
                'car_id': response.meta['car_id'],
                'car_name': response.meta['car_name'],
                'car_tyoe': '',
                'model_id': item['id'],
                'model_name': item['name']
            }




