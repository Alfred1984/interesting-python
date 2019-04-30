import requests
import pandas as pd
from pymongo import MongoClient


class DataCrawler(object):
    def __init__(self):
        self.cities = list(pd.read_csv('city_data.csv')['city'])
        client = MongoClient(host='localhost', port=27017)
        db = client.Laborday
        self.col = db.ticket

    def get_city_trip(self):
        for city in self.cities:
            print('正在爬取城市:{}的数据!'.format(city))
            res = requests.get('https://travelsearch.fliggy.com/async/queryItemResult.do?searchType='
                               'product&keyword={}&category=SCENIC&pagenum=1'.format(city))
            data = res.json()
            itemPagenum = data['data']['data'].get('itemPagenum')
            if itemPagenum is not None:
                page_count = itemPagenum['data']['count']

                data_list = data['data']['data']['itemProducts']['data']['list'][0]['auctions']
                for ticket in data_list:
                    ticket['city'] = city
                    self.col.insert_one(ticket)
                print('成功爬取城市:{}的第{}页数据!'.format(city, 1))

                if page_count > 1:
                    for page in range(2, page_count+1):
                        res = requests.get('https://travelsearch.fliggy.com/async/queryItemResult.do?searchType='
                                           'product&keyword={}&category=SCENIC&pagenum={}'.format(city, page))
                        data = res.json()
                        data_list = data['data']['data']['itemProducts']['data']['list'][0]['auctions']
                        for ticket in data_list:
                            ticket['city'] = city
                            self.col.insert_one(ticket)
                        print('成功爬取城市:{}的第{}页数据!'.format(city, page))


if __name__ == '__main__':
    data_crawler = DataCrawler()
    data_crawler.get_city_trip()
