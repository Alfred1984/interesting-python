import random
import time
import requests
from pymongo import MongoClient


class CommentPhotoCrawler(object):

    def __init__(self, sleep_time=2):
        self.sleep_time = sleep_time
        self.mid = None
        self.login_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 '
                          '(KHTML, like Gecko)Chrome/48.0.2564.116 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Origin': 'https://passport.weibo.cn',
            'Referer': 'https://passport.weibo.cn/signin/login?'
        }
        self.session = None
        client = MongoClient('127.0.0.1', 27017)
        db = client.Jayzhou
        self.col = db.jay
        self.col.ensure_index('scheme', unique=True)

    def login(self, user, password):
        self.session = requests.Session()
        login_data = {
            'username': user,
            'password': password,
            'savestate': '1',
            'r': 'https://weibo.cn/',
            'ec': '0',
            'pagerefer': 'https://passport.weibo.cn/signin/welcome',
            'entry': 'mweibo',
            'mainpageflag': '1'
        }  # 表单数据
        login_url = 'https://passport.weibo.cn/sso/login'
        self.session.post(login_url, headers=self.login_headers, data=login_data)
        print('模拟登录手机网页端微博成功！')

    def get_fans(self):

        while 1:
            urls = self.gen_url()
            for url in urls:
                res = self.session.get(url)
                print(res.json())
                if res.status_code == 418 or res.status_code == 403:
                    print('Can not get data from url: {}'.format(url))
                    time.sleep(60)
                else:
                    data = res.json().get('data').get('cards')
                    if len(data) > 0:
                        for item in data[0]['card_group']:
                            self.col.update({'scheme': item['scheme']}, {'$set': item}, upsert=True)
                        print('Successfully get data from url: {}'.format(url))
                    else:
                        print('Can not get data from url: {}'.format(url))
                    time.sleep(random.random()*5)

    @staticmethod
    def gen_url():
        base_url = 'https://m.weibo.cn/api/container/getIndex?containerid=' \
                   '2311407a8941058aaf4df5147042ce104568da_-_super_newfans&luicode' \
                   '=10000011&lfid=1008087a8941058aaf4df5147042ce104568da_-_hotuser&page={}'

        url_list = [base_url.format(i) for i in range(1, 51)]
        random.shuffle(url_list)
        return url_list


if __name__ == '__main__':
    com = CommentPhotoCrawler()
    com.login('', '')  # 传入你的微博用户名和密码
    com.get_fans()
