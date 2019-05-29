import requests
import pandas as pd
from pymongo import MongoClient


class Location(object):
    def __init__(self, keyword='瑞幸咖啡'):
        self.keyword = keyword
        self.key = ''  # 你申请的高德地图API key
        self.url = 'https://restapi.amap.com/v3/place/text?keywords={}&city={}&' \
                   'output=json&offset=20&page={}&key={}&extensions=all'
        self.data = pd.read_csv('city.csv')

        client = MongoClient(host='localhost', port=27017)
        db = client.Amap
        self.col = db.luckin_coffee

    def get_location_data(self):
        for index, row in self.data.iterrows():
            page = 1
            while 1:
                url = self.url.format(self.keyword,
                                      row['name'],
                                      page,
                                      self.key)
                res = requests.get(url)
                if int(res.json()['count']) > 0:
                    pois = res.json()['pois']
                    if len(pois) > 0:
                        self.col.insert_many(pois)
                        print('成功爬取并保存城市:{}第{}页的数据!'.format(row['name'], page))
                    page += 1
                else:
                    print('城市:{}第{}页无数据!'.format(row['name'], page))
                    break


if __name__ == '__main__':
    loc = Location('luckin coffee')
    loc.get_location_data()
