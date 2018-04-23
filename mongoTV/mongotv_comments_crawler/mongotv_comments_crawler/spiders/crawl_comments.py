# -*- coding: utf-8 -*-
import json
import scrapy
from scrapy.http import Request


class CrawlCommentsSpider(scrapy.Spider):
    name = 'crawl_comments'  # 爬虫名
    allowed_domains = ['mgtv.com']  # 允许爬取的域名
    subject_id = 4327535  # 视频的id
    pages = list(range(1, 638))  # 需要爬取的评论页数

    def start_requests(self):  # 重写start_requests函数
        start_urls = ['https://comment.mgtv.com/video_comment/list/?callback=' \
                      'jQuery182040635960604983135_1524066975165&_support=10000000' \
                      '&type=hunantv2014&subject_id={}&page={}'.format(self.subject_id, page) for page in self.pages]
        # 生成所有需要爬取的url保存进start_urls
        for url in start_urls:  # 遍历start_urls发出请求
            yield Request(url)

    def parse(self, response):
        text = response.text[response.text.find('{'):-1]  # 通过字符串选取的方式把"jQuery...()去掉"
        json_data = json.loads(text)  # 转换成json格式
        for i in json_data['comments']:  # 遍历每页的评论列表
            item = {'comment_id': i['comment_id'],  # 取出'comment_id'用来唯一标识每条评论
                    'comments': i}  # 每条评论的相关信息全部塞进'comments'
            yield item
