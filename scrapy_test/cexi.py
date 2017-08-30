# -*- coding:utf-8 -*-

import scrapy
from scrapy import Request
from scrapy.selector import Selector

# url = "https://www.guazi.com/wh/buy"
# req = Request(url=url,
# cookies={'antipas':'f90c49564a52dJxK6867t91E46b'},
# headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'})


class cexiSpider(scrapy.Spider):
    name = 'cexispider'
    cookies = {'antipas': 'f90c49564a52dJxK6867t91E46b'}
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'}

    custom_settings = {
        "DOWNLOAD_DELAY": 5.0,
    }

    def start_requests(self):
        url = 'https://www.guazi.com/wh/buy'
        yield Request(url=url, cookies=self.cookies, headers=self.headers, callback=self.parse)

    def parse(self, response):
        selector_href = response.xpath("//div[@class='dd-all clearfix js-brand js-option-hid-info']//li//a/@href")
        # for item in selector_href:
        #     next_page = response.urljoin(item.extract())
        #     yield scrapy.Request(next_page, cookies=self.cookies,
        #                      headers=self.headers, callback=self.parse_cexi)
        next_page = response.urljoin(selector_href[10].extract())
        yield scrapy.Request(next_page, cookies=self.cookies,
                             headers=self.headers, callback=self.parse_cexi)


    def parse_cexi(self, response):
        code = response.url.split("/")[-2]
        filename = "../data/pinpai_%s.txt" % code
        selector = response.xpath("//div[@class='dd-car js-tag js-option-hid-info']//li//a/text()")

        cexi_list = []

        for item in selector.extract():
            cexi_list.append(item)

        with open(filename, 'w') as f:
            for item in cexi_list:
                print item
                f.write(item.encode('utf-8'))
                f.write("\n")

