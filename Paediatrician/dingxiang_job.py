import os
import json
import time
import random
import requests
from pymongo import MongoClient


class CrawlJob(object):

    def __init__(self):
        self.list_header = {'Host': 'api.jobmd.cn',
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'Accept-Encoding': 'br, gzip, deflate',
                            'Connection': 'keep-alive',
                            'Accept': '*/*',
                            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X)'
                                          ' AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16D57 Mi'
                                          'croMessenger/7.0.3(0x17000321) NetType/4G Language/en',
                            'Referer': 'https://servicewechat.com/wx9a1e763032f69003/124/page-frame.html',
                            'Content-Length': '105',
                            'Accept-Language': 'en-us'}
        self.list_url = 'https://api.jobmd.cn/api/wechatMiniApp/search'
        self.detail_header = {'Host': 'api.jobmd.cn',
                              'DXY-WXAPP-AUTH-TOKEN': '[object Object]',
                              'Content-Type': 'application/json',
                              'Connection': 'keep-alive',
                              'Accept': '*/*',
                              'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_1_4 like Mac OS X)'
                                            ' AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/16D57'
                                            ' MicroMessenger/7.0.3(0x17000321) NetType/4G Language/en',
                              'Referer': 'https://servicewechat.com/wx2c8b5efe895460dc/14/page-frame.html',
                              'Accept-Language': 'en-us',
                              'Accept-Encoding': 'br, gzip, deflate'}
        self.company_type = {'公立医院': 1, '民营医院': 2, '医药企业': 3, '生物企业': 4,
                             '科研院校': 5, '网络出版': 6, '其他单位': 7, '诊所/药房': 8}
        self.area_code = None

        host = os.environ.get('MONGODB_HOST', '127.0.0.1')  # 本地数据库
        port = os.environ.get('MONGODB_PORT', '27017')  # 数据库端口
        mongo_url = 'mongodb://{}:{}'.format(host, port)
        mongo_db = os.environ.get('MONGODB_DATABASE', 'DingXiang')
        client = MongoClient(mongo_url)
        self.db = client[mongo_db]
        self.db['erke'].create_index('id', unique=True)  # 以m端链接为主键进行去重
        self.all_id = []

    def get_area_code(self):
        url = 'https://assets.dxycdn.com/core/widgets/cascading-list-v2/data/location.js?t=20180226&t=2019324'
        res = requests.get(url)
        data = json.loads(res.text.replace('\n    ', '').replace('\n', '')[19:-25])
        area = []
        code = []
        for dist in data:
            area.append(dist['label'])
            code.append(dist['key'])

        self.area_code = dict(zip(area, code))
        with open('area_code.txt', 'w') as f:
            f.write(str(self.area_code))

    def get_job_id(self, wd):
        with open('area_code.txt', 'r') as f:
            self.area_code = f.read()
            self.area_code = eval(self.area_code)

        for area, code in self.area_code.items():
            for c_type, num in self.company_type.items():
                page = 1
                has_more = 1
                while has_more:
                    post_data = {'wd': wd,
                                 'locations': str(code),
                                 'pageSize': '10',
                                 'pageNo': str(page),
                                 'salary': None,
                                 'companyType': str(num),
                                 'grade': None,
                                 'jobType': None,
                                 'jobYear': None}
                    try:
                        host, port = self.get_proxy_ip()
                        proxies = {"http": "http://{}:{}".format(host, port),
                                   "https": "http://{}:{}".format(host, port), }
                        res_list = requests.post(url=self.list_url,
                                                 headers=self.list_header,
                                                 data=post_data,
                                                 proxies=proxies,
                                                 timeout=3)
                        data = res_list.json()
                        if data['success'] and data['results']['pageBean']['totalCount'] > 0:
                            print('链接请求成功！[locations:{}, pageNo:{}, companyType:{}]'.format(code,
                                                                                            page,
                                                                                            num))
                            for li in data['results']['items']:
                                job_id = li['id']
                                self.get_job_detail(job_id, area)

                            total = data['results']['pageBean']['totalCount']
                            if total / 10 <= page:
                                has_more = 0
                            page += 1
                            time.sleep(random.random() * 2)
                        else:
                            print('该页无数据！[locations:{}, pageNo:{}, companyType:{}]'.format(code,
                                                                                           page,
                                                                                           num))
                            has_more = 0
                            time.sleep(random.random()*5)

                    except:
                        print('链接请求不成功![locations:{}, pageNo:{}, companyType:{}]'.format(code,
                                                                                         page,
                                                                                         num))

    def get_job_detail(self, job_id, area):
        if job_id in self.all_id:
            print('Job_id{}重复！'.format(job_id))
        else:
            detail_url = 'https://api.jobmd.cn/api/wechatMiniApp/entwork?id={}&recommendSize=0'.format(job_id)
            retry = 1
            while retry:

                try:
                    host, port = self.get_proxy_ip()
                    proxies = {"http": "http://{}:{}".format(host, port),
                               "https": "http://{}:{}".format(host, port), }

                    res_job = requests.get(url=detail_url,
                                           headers=self.detail_header,
                                           proxies=proxies,
                                           timeout=3)
                    de_data = res_job.json()
                    if de_data['success']:
                        item = de_data['results']['entwork']
                        item['area'] = area
                        self.db['fuchanke'].update_one({'id': item['id']}, {'$set': item}, upsert=True)
                        print('成功保存数据:{}!'.format(item))
                    retry = 0
                    time.sleep(random.random()*2)
                    self.all_id.append(job_id)
                except:
                    print('id{}请求不成功！'.format(job_id))

    @staticmethod
    def get_proxy_ip():
        proxy_url = 'https://proxy.horocn.com/api/proxies?order_id=V8SX1629045840556986' \
                    '&num=1&format=json&line_separator=win&can_repeat=yes'
        res = requests.get(proxy_url)
        host = res.json()[0]['host']
        port = res.json()[0]['port']
        return host, port


if __name__ == '__main__':
    crawler = CrawlJob()
    crawler.get_area_code()
    crawler.get_job_id('妇产科')
