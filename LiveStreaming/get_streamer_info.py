import re
import requests
import pandas as pd
from pymongo import MongoClient


class SteamerInfo(object):
    def __init__(self):
        self.base_url = 'http://m.toutiao.com/profile/{}/#mid=6512351477'
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit/537.36 '
                                      '(KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
        self.pat_username = r'''id="username" item="fontsize">(.*)</span>'''
        self.pat_follow = r'''data-num="(\d*)"'''
        self.pat_description = r'''<p class="text" id="description" item="fontsize">(.*)</p>'''
        self.pat_auth = r'''<span class="auth-type" item="fontsize">(.*)</span>'''
        client = MongoClient(host='localhost', port=27017)
        db = client.LiveData
        self.col = db.SteamerInfo

    def get_steamer_info(self):
        data = pd.read_csv('steamer_id.csv')
        data = data[data['user_name'].notnull()]
        steamer_id = list(data['user_id'])

        for sid in steamer_id:
            res = requests.get(self.base_url.format(sid), headers=self.headers)
            username = re.findall(self.pat_username, string=res.text)
            if len(username) > 0:
                username = username[0]
                following, follower = re.findall(self.pat_follow, string=res.text)
                description = self.handle_list(re.findall(self.pat_description, string=res.text))
                auth = self.handle_list(re.findall(self.pat_auth, string=res.text))

                item = {'user_id': sid, 'username': username, 'following': following,
                        'follower': follower, 'description': description, 'auth': auth}
                self.col.insert_one(item)
                print('Successfully crawled and saved user :{}!'.format(username))

    @staticmethod
    def handle_list(li):
        if len(li) > 0:
            return li[0]


if __name__ == '__main__':
    steamer = SteamerInfo()
    steamer.get_steamer_info()
