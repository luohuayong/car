# -*- coding:utf-8 -*-

import scrapy
from scrapy import Request
from scrapy.selector import Selector

# url = "https://www.guazi.com/wh/buy"
# req = Request(url=url,
# cookies={'antipas':'f90c49564a52dJxK6867t91E46b'},
# headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'})


class guaziSpider(scrapy.Spider):
    name = 'guazispider'
    start_urls = ['https://www.guazi.com/wh/buy',]

    def start_requests(self):
        for url in self.start_urls:
            yield  Request(url=url,
                           cookies={'antipas':'f90c49564a52dJxK6867t91E46b'},
                           headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'})


    def parse(self, response):
        # 品牌
        selector1 = response.xpath("//span[@class='a-box']/a/text()")
        for item in selector1:
            print item.extract()
        # 全部品牌
        selector2 = response.xpath("//div[@class='dd-all clearfix js-brand js-option-hid-info']//li")
        for i in range(len(selector2)):
            selector_label = Selector(text=selector2[i].extract()).xpath("//label/text()")
            print selector_label.extract()
            for item_a in Selector(text=selector2[i].extract()).xpath("//a/text()"):
                print item_a.extract()
        # # 车系
        # selector3 = response.xpath("//div[@class='dd-all clearfix js-brand js-option-hid-info']//a/text()")
        # for item in selector3:
        #     print item.extract()
        # # 全部车系
        # selector4 = response.xpath("//div[@class='dd-all clearfix js-brand js-option-hid-info']//a/text()")
        # for item in selector4:
        #     print item.extract()

