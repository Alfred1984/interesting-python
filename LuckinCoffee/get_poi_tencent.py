import time
import requests
import pandas as pd
from pymongo import MongoClient


class Location(object):
    def __init__(self, keyword='瑞幸咖啡'):
        self.keyword = keyword
        self.key = ''  # 你申请的腾讯地图API key
        self.url = 'https://apis.map.qq.com/ws/place/v1/search?keyword={}&boundary=region({},0)' \
                   '&page_size=20&page_index={}&key={}'
        self.data = pd.read_csv('city_tencent.csv')

        client = MongoClient(host='localhost', port=27017)
        db = client.TCmap
        self.col = db.xsd

    def get_location_data(self):
        for index, row in self.data.iterrows():
            page = 1
            while 1:
                url = self.url.format(self.keyword,
                                      row['fullname'],
                                      page,
                                      self.key)
                res = requests.get(url)
                if res.json()['count'] > 0:
                    pois = res.json()['data']
                    time.sleep(0.2)
                    if len(pois) > 0:
                        self.col.insert_many(pois)
                        print('成功爬取并保存城市:{}第{}页的数据!'.format(
                            row['fullname'],
                            page))
                        if ((res.json()['count'] / 20) > page) and (page < 10):
                            page += 1
                        else:
                            break
                else:
                    break


if __name__ == '__main__':
    loc = Location('瑞幸咖啡')
    loc.get_location_data()
