# -*- coding: utf-8 -*-
import scrapy


class ConsumerSpider(scrapy.Spider):
    name = 'consumer'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://zhihu.com/']

    def parse(self, response):
        pass
