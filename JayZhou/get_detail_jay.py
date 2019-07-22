import random
import time
import requests
from pymongo import MongoClient


class CommentPhotoCrawler(object):
    """注：这次爬虫由于时间原因，写得比较粗糙，仅供参考"""

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
        self.db = client.Jayzhou
        self.col = self.db.jay_detail
        self.col.ensure_index('uid', unique=True)

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
        base_url = 'https://m.weibo.cn/api/container/getIndex?containerid=230283{}_-_INFO' \
                   '&title=%E5%9F%BA%E6%9C%AC%E8%B5%84%E6%96%99&luicode=10000011&lfid=230283{}'
        uid_list = self.gen_url()
        for uid in uid_list:
            res = self.session.get(base_url.format(uid, uid))
            if res.status_code == 200:
                print(res.json())
                self.parse_res(res, uid)
                print('Successfully got data from uid: {}'.format(uid))
            else:
                print('Can not get uid : {}'.format(uid))
            time.sleep(random.random()*4)

    def gen_url(self):
        col = self.db.get_collection('jay')
        scheme_list = list(col.distinct('scheme'))
        uid_list = [scheme[21:31] for scheme in scheme_list]
        with open('uid.txt', 'w') as f:
            for u in uid_list:
                f.write(u+'\n')
        return uid_list

    def parse_res(self, response, uid):
        item = {'uid': uid}
        data = response.json()['data']['cards'][0:2]
        try:
            for info in data[0]['card_group'][1:]:
                try:
                    item[info['item_name']] = info['item_content']
                except:
                    pass
            for info in data[1]['card_group'][1:]:
                try:
                    item[info['item_name']] = info['item_content']
                except:
                    pass
        except:
            print('Passing uid: {}'.format(uid))

        self.col.update({'uid': item['uid']}, {'$set': item}, upsert=True)


if __name__ == '__main__':
    com = CommentPhotoCrawler()
    com.login('', '')  # 传入你的微博用户名和密码
    com.get_fans()