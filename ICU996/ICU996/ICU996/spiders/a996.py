# -*- coding: utf-8 -*-
import json
import scrapy
import pandas as pd


class A996Spider(scrapy.Spider):
    name = '996'
    allowed_domains = ['github.com']

    def start_requests(self):
        data = pd.read_csv('stargazers.csv')
        for url in data.iloc[35000:39991]['url']:
            r_url = url + '?access_token=xxxxxxxxxxxxxxx'
            yield scrapy.Request(url=r_url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        item = json.loads(response.text)
        if response.status == 200:
            yield item
        else:
            print('链接:{}请求不成功!'.format(response.url))
