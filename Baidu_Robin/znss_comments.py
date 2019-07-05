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
            'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&r'
                       '=https%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt='
        }
        self.session = None
        client = MongoClient('127.0.0.1', 27017)
        db = client.Baidu_Robin
        self.col = db.sina_comments

        self.max_id = None
        self.max_id_type = None

    def login(self, user, password):
        self.session = requests.Session()
        login_data = {
            'username': user,
            'password': password,
            'savestate': '1',
            'r': 'https://weibo.cn/',
            'ec': '0',
            'pagerefer': 'https://passport.weibo.cn/signin/welcome?entry='
                         'mweibo&r=https%3A%2F%2Fm.weibo.cn%2Fdetail%2F4333036507864049',
            'entry': 'mweibo',
            'mainpageflag': '1'
        }  # 表单数据
        login_url = 'https://passport.weibo.cn/sso/login'
        self.session.post(login_url, headers=self.login_headers, data=login_data)
        print('模拟登录手机网页端微博成功！')

    def get_comments(self, mid, max_page):

        self.mid = mid
        is_first_page = True

        for page in range(max_page):
            if is_first_page:
                url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0'.format(self.mid, self.mid)
            else:
                url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}' \
                      '&max_id_type={}'.format(self.mid, self.mid, self.max_id, self.max_id_type)
            self.get_data(url, page)
            is_first_page = False

    def get_data(self, url, page):
        response = self.session.get(url, headers=self.login_headers)
        try:
            self.col.insert_many(response.json()['data']['data'])
            self.max_id = response.json()['data']['max_id']  # 找出下一页需要用的max_id
            self.max_id_type = response.json()['data']['max_id_type']  # 找出下一页需要用的max_id_type，每爬16页会变更

            print('Successfully crawled data from page : {}'.format(page+1))
            time.sleep(random.random()*5)
        except:  # 处理采集频率过高被反爬的情况
            print('Can not crawl page : {}, crawler stopped! Crawler will retry later.'.format(page+1))
            time.sleep(60)
            self.get_data(url, page)


if __name__ == '__main__':
    com = CommentPhotoCrawler()
    com.login('', '')  # 传入你的微博用户名和密码
    com.get_comments(mid=, max_page=)
