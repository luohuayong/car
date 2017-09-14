# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapy.selector import Selector
import logging

class GuaziSpider(scrapy.Spider):
    name = 'guazi'
    allowed_domains = ['www.guazi.com']
    start_urls = ['https://www.guazi.com/wh/buy/']

    cookies = {'antipas': '57Z575218968bL6r20iIe1E1B2'}
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, cookies=self.cookies, headers=self.headers, callback=self.parse_brand)

    def parse_brand(self, response):
        logging.info("解析品牌")
        brand_block = response.xpath("//div[@class='dd-all clearfix js-brand js-option-hid-info']//li").extract()
        for i in range(len(brand_block)):
            brand_first = Selector(text=brand_block[i]).xpath("//label/text()").extract_first()
            for item in Selector(text=brand_block[i]).xpath("//a").extract():
                brand_name = Selector(text=item).xpath("//a/text()").extract_first()
                brand_herf = Selector(text=item).xpath("//a/@href").extract_first()
                url = response.urljoin(brand_herf)
                yield Request(url=url, cookies=self.cookies, headers=self.headers, callback=self.parse_car,
                              meta={'brand_first': brand_first, 'brand_name': brand_name})

    def parse_car(self, response):
        logging.info("解析车系")
        brand_first = response.meta['brand_first']
        brand_name = response.meta['brand_name']
        car_type_block = response.xpath("//div[@class='dd-car js-tag js-option-hid-info']//li").extract()
        for i in range(len(car_type_block)):
            car_type = Selector(text=car_type_block[i]).xpath("//label/text()").extract_first()
            for item in Selector(text=car_type_block[i]).xpath("//a").extract():
                car_name = Selector(text=item).xpath("//a/text()").extract_first()
                car_herf = Selector(text=item).xpath("//a/@href").extract_first()
                url = response.urljoin(car_herf)
                yield Request(url=url, cookies=self.cookies, headers=self.headers, callback=self.parse_sale_list,
                              meta={'brand_first': brand_first, 'brand_name': brand_name,
                                    'car_type': car_type, 'car_name': car_name})

    def parse_sale_list(self, response):
        logging.info("解析销售列表")
        brand_first = response.meta['brand_first']
        brand_name = response.meta['brand_name']
        car_type = response.meta['car_type']
        car_name = response.meta['car_name']
        next_page = response.xpath("//div[@class='pageBox']//a[@class='next']/@href").extract()
        if len(next_page) == 1:
            logging.info("销售列表下一页")
            url = response.urljoin(next_page[0])
            yield Request(url=url, cookies=self.cookies, headers=self.headers, callback=self.parse_sale_list,
                          meta={'brand_first': brand_first, 'brand_name': brand_name,
                                'car_type': car_type, 'car_name': car_name})

        for item in response.xpath("//ul[@class='carlist clearfix js-top']//a/@href").extract():
            url = response.urljoin(item)
            yield Request(url=url, cookies=self.cookies, headers=self.headers, callback=self.parse_sale,
                          meta={'brand_first': brand_first, 'brand_name': brand_name,
                                'car_type': car_type, 'car_name': car_name})

    def parse_sale(self, response):
        yield {
            'brand_first' : response.meta['brand_first'],
            'brand_name' : response.meta['brand_name'],
            'car_type' : response.meta['car_type'],
            'car_name' : response.meta['car_name'],
            'model_name': response.xpath("//div[@class='titlebox']/p/text()").extract_first(),
            'url': response.url,
            'shangpai_date': response.xpath("//li[@class='one']/span/text()").extract_first(),
            'xingshi': response.xpath("//li[@class='two']/span/text()").extract_first(),
            'address': response.xpath("//li[@class='three']/span/text()").extract_first(),
            'price': response.xpath("//span[@class='pricestype']/text()").extract_first(),
            'price_new': response.xpath("//span[@class='newcarprice']/text()").extract_first(),
        }



