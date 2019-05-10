import re
import time
import json
import requests
import pandas as pd
from threading import Thread
from queue import Queue
from pymongo import MongoClient


def run_time(func):
    def wrapper(*args, **kw):
        start = time.time()
        func(*args, **kw)
        end = time.time()
        print('running', end-start, 's')
    return wrapper


class GetDiamonds(object):

    def __init__(self):
        self.qurl = Queue()
        self.thread_num = 8
        self.headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_5) AppleWebKit'
                                      '537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
        self.game_dict = {'英雄联盟': 77, '绝地求生': 74, '穿越火线': 79, '棋牌游戏': 106,
                          '热门网游': 107, 'Apex英雄': 157, 'DOTA2': 161, 'DOTA': 172, '刀塔自走棋': 174,
                          '刺激战场': 75, '迷你世界': 76, '第五人格': 78, '香肠派对': 104, '热门手游': 105,
                          '明日之后': 153, '非人学园': 170, '决战平安京': 171, '自走棋手游': 176,
                          '主机游戏': 97, '我的世界': 98, '方舟': 151, '格斗游戏': 100, '怀旧经典': 99}
        self.pat = r"""fan_piao\': (\d*),"""
        self.pat2 = r"""list/(\d*)\?_signature"""
        self.data = None
        client = MongoClient(host='localhost', port=27017)
        db = client.LiveData
        self.col = db.livedata

    def get_live_list(self):
        present_time = str(int(time.time() * 1000))
        data = list()

        for game, game_id in self.game_dict.items():

            has_more = True

            while has_more:
                res = requests.get('https://live.ixigua.com/api/feed/category/more/1/{}/{}'
                                   '?_signature=jBjRbgAgEBl5f6GJqwpWXYwY0XAANCx'.format(present_time, game_id),
                                   headers=self.headers)
                game_list = res.json()['data'].get('liveSource')
                if game_list is not None:
                    data.extend(game_list)
                    has_more = res.json()['data']['hasMore']
                    print('Successfully crawled Game [{}] data!'.format(game))
                else:
                    print('There is no data of Game [{}]!'.format(game))
                    has_more = False

        df = pd.DataFrame(data)
        df['time'] = present_time
        df.drop(columns=['cover_url', 'user_avator'], inplace=True)
        df.to_csv('/root/alfred/live_list.csv', index=False)

    def produce_url(self):
        self.data = pd.read_csv('/root/alfred/live_list.csv')
        for i in range(5):
            for room_id in self.data['room_id']:
                url = 'https://live.ixigua.com/api/msg/list/{}?' \
                      '_signature=uK7QDAAgEBhNyaDrMFdslLiu0BAAOR9&AnchorID=108671743488&' \
                      'Cursor=6683707614813162251_{}'.format(room_id, int(time.time()*1000))
                self.qurl.put(url)

    def get_info(self):
        while not self.qurl.empty():
            url = self.qurl.get()
            print('crawling', url)
            res = requests.get(url, headers=self.headers)
            danmu_data = res.json()['data'].get('LiveMsgs')
            fan_piao = re.findall(self.pat, str(danmu_data))
            room_id = int(re.findall(self.pat2, url)[0])
            if len(fan_piao) > 0:
                self.data.loc[self.data['room_id'] == room_id, 'diamonds'] = fan_piao[0]
                print('Successfully saved the number of diamonds for room_id:{}!'.format(room_id))

    @run_time
    def run(self):
        self.produce_url()

        ths = []
        for _ in range(self.thread_num):
            th = Thread(target=self.get_info)
            th.start()
            ths.append(th)
        for th in ths:
            th.join()

        self.col.insert_many(json.loads(self.data.to_json(orient='records')))
        print('Data crawling is finished.')


if __name__ == '__main__':
    get_diamonds = GetDiamonds()
    while 1:
        start_time = time.time()
        get_diamonds.get_live_list()
        get_diamonds.run()
        end_time = time.time()
        time_cost = end_time - start_time
        if time_cost < 300:
            time.sleep(300-time_cost)
