import os
import time
from datetime import datetime
import requests
from pymongo import MongoClient


class MaoYan(object):
    """
    猫眼评论爬虫，爬取电影《流浪地球》的评论和评分
    """

    def __init__(self):
        """
        初始化函数
        :param
        headers: 请求头
        time: 当前时间戳
        premiere_time: 首映时间的时间戳
        """
        self.headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.'
                                      '38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
                        'Connection': 'keep-alive',
                        'Cookie': '_lxsdk_cuid=168d5d128e7c8-033114908a580c-10376654-fa000-168d5d128e7c8;'
                                  ' _lx_utm=utm_source%3Dbing%26utm_medium%3Dorganic; uuid_n_v=v1;'
                                  ' iuuid=5D49FF702DB211E9AF1B8D0648275EC02D381B7848144BC1A299A63C05094BF5;'
                                  ' webp=true; selectci=true; ci=281%2C%E6%83%A0%E5%B7%9E;'
                                  ' __mta=247299643.1549775481575.1549783540088.1549862773375.3;'
                                  ' _lxsdk=5D49FF702DB211E9AF1B8D0648275EC02D381B7848144BC1A299A63C05094BF5;'
                                  ' _lxsdk_s=168db05185a-332-e0d-bc5%7C%7C157'}
        self.time = int(time.time()*1000)
        self.premiere_time = int(time.mktime(time.strptime('2019-02-05 00:00:00', '%Y-%m-%d %H:%M:%S'))*1000)

        # 配置mongodb数据库
        host = os.environ.get('MONGODB_HOST', '127.0.0.1')  # 本地数据库
        port = os.environ.get('MONGODB_PORT', '27017')  # 数据库端口
        mongo_url = 'mongodb://{}:{}'.format(host, port)
        mongo_db = os.environ.get('MONGODB_DATABASE', 'maoyan')
        client = MongoClient(mongo_url)
        self.db = client[mongo_db]
        self.db['maoyan'].create_index('id', unique=True)  # 以评论的id为主键进行去重

    def get_comment(self):
        """
        爬取首映到当前时间的电影评论
        :param
        url: 评论真实请求的url，参数ts为时间戳
        :return: None
        """
        url = 'http://m.maoyan.com/review/v2/comments.json?movieId=248906&userId=-1&' \
              'offset=0&limit=15&ts={}&type=3'
        while self.time > self.premiere_time:
            req_url = url.format(self.time)
            res = requests.get(req_url, headers=self.headers)
            count = 0
            for com in res.json()['data']['comments']:
                self.parse_comment(com=com)
                count += 1
                if count == 15:
                    self.time = com['time']

            print('成功爬取截止到{}的数据！'.format(datetime.fromtimestamp(int(self.time/1000))))

    def parse_comment(self, com):
        """
        解析函数，用来解析爬回来的json评论数据，并把数据保存进mongodb数据库
        :param com: 每一条评论的json数据
        :return:
        """
        comment = {'content': com['content'], 'gender': com['gender'], 'id': com['id'],
                   'nick': com['nick'], 'replyCount': com['replyCount'], 'score': com['score'],
                   'time': com['time'], 'upCount': com['upCount'],
                   'userId': com['userId'], 'userLevel': com['userLevel']}  # 构造评论字典
        # 通过评论id去重，如果已经有了就更新，没有就插入
        self.db['maoyan'].update_one({'id': comment['id']}, {'$set': comment}, upsert=True)


if __name__ == '__main__':
    my = MaoYan()
    my.get_comment()
