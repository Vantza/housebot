# -*- coding: utf-8 -*-
import scrapy
import time

from scrapy.http.request import Request


class lianjiaSpider(scrapy.Spider):
    name = 'lianjia-spider'
    base_url = 'https://sh.lianjia.com/ershoufang/'
    start_urls = [
        base_url,
    ]
    RESOURCE = 'lianjia'
    SLASH = '/'
    PAGE_INDEX = 2
    PAGE_MAX = 10
    HEADERS = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'lianjia_uuid=07e69a53-d612-4caa-9145-b31c2e9410f4; _smt_uid=5c2b6394.297c1ea9; UM_distinctid=168097cfb8db98-058790b6b3796c-10306653-13c680-168097cfb8e3fa; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1546347413; _ga=GA1.2.1249021892.1546347415; _gid=GA1.2.1056168444.1546347415; all-lj=c60bf575348a3bc08fb27ee73be8c666; TY_SESSION_ID=d35d074b-f4ff-47fd-9e7e-8b9500e15a82; CNZZDATA1254525948=1386572736-1546352609-https%253A%252F%252Fbj.lianjia.com%252F%7C1546363071; CNZZDATA1255633284=2122128546-1546353480-https%253A%252F%252Fbj.lianjia.com%252F%7C1546364280; CNZZDATA1255604082=1577754458-1546353327-https%253A%252F%252Fbj.lianjia.com%252F%7C1546366122; lianjia_ssid=087352e7-de3c-4505-937e-8827e808c2ee; select_city=440700; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1546391853',
        'DNT': '1',
        'Host': 'sh.lianjia.com',
        'Referer': 'https://sh.lianjia.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    HOUSE_INFO_PATH = '//ul[@class="sellListContent"]/li/div[@class="info clear"]'
    TITLE_PATH = './div[@class="title"]/a/text()'
    ADDRESS_1ST_PATH = './div[@class="address"]/div/a/text()'
    ADDRESS_2ND_PATH = './div[@class="address"]/div/text()'
    FLOOR_1ST_PATH = './div[@class="flood"]/div/text()'
    FLOOR_2ND_PATH = './div[@class="flood"]/div/a/text()'
    FOLLOW_INFO_PATH = './div[@class="followInfo"]/text()'
    PRICE_INFO_1ST_PATH = './div[@class="priceInfo"]/div/span/text()'
    PRICE_INFO_2ND_PATH = './div[@class="priceInfo"]/div/text()'
    UNIT_PRICE_PATH = './div[@class="priceInfo"]/div[@class="unitPrice"]/span/text()'

    def parse(self, response):
        for houseInfo in response.xpath(self.HOUSE_INFO_PATH):
            yield {
                'resource': self.RESOURCE,
                'fetchDate': time.strftime('%Y-%m-%d %H:%M:%S'),
                'title': self.title_handle(houseInfo),
                'address': self.address_handle(houseInfo),
                'floor': self.floor_handle(houseInfo),
                'followInfo': self.follow_info_handle(houseInfo),
                'tag': self.tag_handle(houseInfo),
                'priceInfo': self.price_info_handle(houseInfo),
                'unitPrice': self.unit_price_handle(houseInfo)
            }
        next_page_url = self.base_url + 'pg' + str(self.PAGE_INDEX)
        if self.PAGE_INDEX < self.PAGE_MAX:
            self.PAGE_INDEX += 1
            yield Request(next_page_url,
                          dont_filter=True)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url,
                          headers=self.HEADERS,
                          dont_filter=True)

    def tag_handle(self, houseInfo):
        tag_list = ''
        for tag in houseInfo.xpath('./div[@class="tag"]/span'):
            temp = tag.xpath('./text()').extract_first()
            if temp is not None:
                tag_list = tag_list + temp + self.SLASH
        return tag_list

    def title_handle(self, houseInfo):
        return houseInfo.xpath(self.TITLE_PATH).extract_first()

    def address_handle(self, houseInfo):
        return houseInfo.xpath(self.ADDRESS_1ST_PATH).extract_first() \
               + houseInfo.xpath(self.ADDRESS_2ND_PATH).extract_first()

    def floor_handle(self, houseInfo):
        return houseInfo.xpath(self.FLOOR_1ST_PATH).extract_first() \
               + houseInfo.xpath(self.FLOOR_2ND_PATH).extract_first()

    def follow_info_handle(self, houseInfo):
        return houseInfo.xpath(self.FOLLOW_INFO_PATH).extract_first()

    def price_info_handle(self, houseInfo):
        return houseInfo.xpath(self.PRICE_INFO_1ST_PATH).extract_first() \
               + houseInfo.xpath(self.PRICE_INFO_2ND_PATH).extract_first()

    def unit_price_handle(self, houseInfo):
        return houseInfo.xpath(self.UNIT_PRICE_PATH).extract_first()
