# -*- coding: utf-8 -*-
import scrapy
import time
import logging

from scrapy.http.request import Request
from housebot.items import HousebotItem


class lianjiaSpider(scrapy.Spider):
    logger = logging.getLogger()
    name = 'lianjia-spider'
    base_url = 'https://sh.lianjia.com/ershoufang/'
    start_urls = [
        base_url,
    ]
    RESOURCE = 'lianjia'
    SLASH = '/'
    PAGE_INDEX = 2
    PAGE_MAX = 99
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

    HOUSE_INFO_PATH = '//ul[@class="sellListContent"]/li[@class="clear LOGVIEWDATA LOGCLICKDATA"]'
    TITLE_PATH = './div[@class="info clear"]/div[@class="title"]/a/text()'
    TAG_PATH = './div[@class="info clear"]/div[@class="tag"]/span'
    ADDRESS_1ST_PATH = './div[@class="info clear"]/div[@class="address"]/div/a/text()'
    ADDRESS_2ND_PATH = './div[@class="info clear"]/div[@class="address"]/div/text()'
    FLOOR_1ST_PATH = './div[@class="info clear"]/div[@class="flood"]/div/text()'
    FLOOR_2ND_PATH = './div[@class="info clear"]/div[@class="flood"]/div/a/text()'
    FOLLOW_INFO_PATH = './div[@class="info clear"]/div[@class="followInfo"]/text()'
    PRICE_INFO_1ST_PATH = './div[@class="info clear"]/div[@class="priceInfo"]/div/span/text()'
    PRICE_INFO_2ND_PATH = './div[@class="info clear"]/div[@class="priceInfo"]/div/text()'
    UNIT_PRICE_PATH = './div[@class="info clear"]/div[@class="priceInfo"]/div[@class="unitPrice"]/span/text()'
    DETAIL_URL_PATH = './a/@href'
    BASE_INFO_LIST_PATH = '//div[@class="m-content"]/div[@class="box-l"]/div[@class="newwrap baseinform"]/div/div[@class="introContent"]/div[@class="base"]/div[@class="content"]/ul/li'
    TRANSACTION_INFO_LIST_PATH = '//div[@class="m-content"]/div[@class="box-l"]/div[@class="newwrap baseinform"]/div/div[@class="introContent"]/div[@class="transaction"]/div[@class="content"]/ul/li'
    LAYOUT_INFO_PATH = '//div[@class="m-content"]/div[@class="box-l"]/div/div[@class="layout-wrapper"]/div[@class="layout"]/div[@class="content"]'

    # here do not return item otherwise it will create a new item which not contains detail info
    def parse(self, response):
        for houseInfo in response.xpath(self.HOUSE_INFO_PATH):
            house_item = HousebotItem()
            house_item['resource'] = self.RESOURCE
            house_item['fetchDate'] = time.strftime('%Y-%m-%d %H:%M:%S')
            house_item['title'] = self.title_handle(houseInfo)
            house_item['address'] = self.address_handle(houseInfo)
            house_item['floor'] = self.floor_handle(houseInfo)
            house_item['followInfo'] = self.follow_info_handle(houseInfo)
            house_item['tag'] = self.tag_handle(houseInfo)
            house_item['priceInfo'] = self.price_info_handle(houseInfo)
            house_item['unitPrice'] = self.unit_price_handle(houseInfo)
            detail_page_url = self.detail_url_handle(houseInfo)
            yield Request(detail_page_url, meta={'items': house_item}, callback=self.parse_detail)
        next_page_url = self.base_url + 'pg' + str(self.PAGE_INDEX)
        if self.PAGE_INDEX < self.PAGE_MAX:
            self.PAGE_INDEX += 1
            yield Request(next_page_url,
                          dont_filter=True)

    def parse_detail(self, response):
        house_item = response.meta['items']
        # todo need to complete whole info
        house_item['room'] = response.xpath('//div[@class="room"]/div[@class="mainInfo"]/text()').extract_first()
        house_item['type'] = response.xpath('//div[@class="type"]/div[@class="mainInfo"]/text()').extract_first()
        house_item['area'] = response.xpath('//div[@class="area"]/div[@class="mainInfo"]/text()').extract_first()
        house_item['baseInfo'] = self.base_info_handle(response.xpath(self.BASE_INFO_LIST_PATH))
        house_item['transactionInfo'] = self.transaction_info_handle(response.xpath(self.TRANSACTION_INFO_LIST_PATH))
        house_item['layoutInfo'] = self.layout_info_handle(response.xpath(self.LAYOUT_INFO_PATH))
        yield house_item

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url,
                          headers=self.HEADERS,
                          dont_filter=True)

    # 布局信息处理
    def layout_info_handle(self, layoutInfo):
        layout_info_dict = {'imgUrl': layoutInfo.xpath('./div[@class="imgdiv"]/img/@src').extract_first()}
        detail_info_list = layoutInfo.xpath('./div[@class="des"]/div[@class="info"]/div[@class="list"]/div[@id="infoList"]/div[@class="row"]')
        # self.logger.debug('detail_info_list is %s', detail_info_list)
        for idx, info in enumerate(detail_info_list):
            key = 'layoutInfo[{}]'.format(idx)
            detail_list = []
            for detail in info.xpath('./div[@class="col"]'):
                detail_list.append(detail.xpath('./text()').extract_first())
            layout_info_dict[key] = detail_list
        return layout_info_dict

    # 交易信息处理
    def transaction_info_handle(self, transactionInfoList):
        transaction_info_dict = {}
        for transactionInfo in transactionInfoList:
            key = transactionInfo.xpath('./span[@class="label"]/text()').extract_first()
            value = transactionInfo.xpath('./span/text()').extract()[1]
            transaction_info_dict[key] = str(value).strip().replace('/n', '')
        return transaction_info_dict

    # 基本信息处理
    def base_info_handle(self, baseInfoList):
        base_info_dict = {}
        for baseInfo in baseInfoList:
            key = baseInfo.xpath('./span/text()').extract_first()
            value = baseInfo.xpath('./text()').extract_first()
            base_info_dict[key] = value
        return base_info_dict

    # 标签信息处理
    def tag_handle(self, houseInfo):
        tag_list = []
        for tag in houseInfo.xpath(self.TAG_PATH):
            # self.logger.debug('tag is %s', tag)
            temp = tag.xpath('./text()').extract_first()
            if temp is not None:
                tag_list.append(temp)
        return tag_list

    # 标题信息处理
    def title_handle(self, houseInfo):
        return houseInfo.xpath(self.TITLE_PATH).extract_first()

    # 地址信息处理
    def address_handle(self, houseInfo):
        return houseInfo.xpath(self.ADDRESS_1ST_PATH).extract_first() \
               + houseInfo.xpath(self.ADDRESS_2ND_PATH).extract_first()

    # 楼层信息处理
    def floor_handle(self, houseInfo):
        return houseInfo.xpath(self.FLOOR_1ST_PATH).extract_first() \
               + houseInfo.xpath(self.FLOOR_2ND_PATH).extract_first()

    # 关注信息处理
    def follow_info_handle(self, houseInfo):
        return houseInfo.xpath(self.FOLLOW_INFO_PATH).extract_first()

    # 价格信息处理
    def price_info_handle(self, houseInfo):
        return houseInfo.xpath(self.PRICE_INFO_1ST_PATH).extract_first() \
               + houseInfo.xpath(self.PRICE_INFO_2ND_PATH).extract_first()

    # 单价信息处理
    def unit_price_handle(self, houseInfo):
        return houseInfo.xpath(self.UNIT_PRICE_PATH).extract_first()

    # 详细页面url处理
    def detail_url_handle(self, houseInfo):
        return houseInfo.xpath(self.DETAIL_URL_PATH).extract_first()
