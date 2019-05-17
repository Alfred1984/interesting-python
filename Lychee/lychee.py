import time
import json
import requests
import pandas as pd
from pymongo import MongoClient
from utils import mt_data, mt_headers


class PriceCrawler(object):
    def __init__(self, fruit):
        self.city_data = pd.read_csv('city_data.csv')
        self.loc_url = 'https://apis.map.qq.com/jsapi?qt=geoc&addr={}&key=TU5BZ-MKD3W-L43RW-O3ZBW-GWMZK-QBB25' \
                       '&output=jsonp&pf=jsapi&ref=jsapi&cb=qq.maps._svcb2.geocoder0'
        self.mt_url = 'http://i.waimai.meituan.com/openh5/search/poi?_={}' \
                      '&X-FOR-WITH=mP9tsFEnb9hfrEHTrmpMSE8Y1za6R%2B5jgLtj%2FaCEkv9mUzq9C90xx7W8ztsISSWV3ccaw7' \
                      'm5H2%2FEKCO4ybaM13BHe5NUV%2BwIfo17kPUjMBKTvhGk21LspnQJ8CJAiH6KAI2CF5K44l%2BJjx1VgIpnVg%3D%3D'
        client = MongoClient(host='localhost', port=27017)
        db = client.Fruit
        self.col = db.lychee

        mt_data['keyword'] = fruit

    def get_lat_lon(self, city):
        try:
            loc_res = requests.get(self.loc_url.format(city+'市'), timeout=5)
            loc_data = json.loads(loc_res.text[loc_res.text.find('(')+1: -1])
            if loc_data['info']['error'] == 0:
                lon = int(float(loc_data['detail']['pointx'])*1000000)
                lat = int(float(loc_data['detail']['pointy'])*1000000)
                return lon, lat, 1
            else:
                return None, None, 0
        except:
            print('Can not get city: {}'.format(city))
            return None, None, 0

    def get_fruit_data(self):
        idx = self.city_data.shape[0]
        for i in range(idx):
            city = self.city_data.iloc[i]['city']
            province = self.city_data.iloc[i]['province']
            mt_data['wm_actual_longitude'], mt_data['wm_actual_latitude'], validate = self.get_lat_lon(city)
            if validate:
                print('Crawling data of city: {}, province: {}'.format(city, province))
                res = requests.post(self.mt_url.format(int(time.time()*1000)),
                                    headers=mt_headers,
                                    data=mt_data)
                time.sleep(5)
                self.format_response(res.json(), city, province)

    def format_response(self, res, city, province):
        if len(res['data']['searchPoiList']) > 0:
            for store in res['data']['searchPoiList']:
                store_name = store['name']
                print('Crawling data of Store: {}'.format(store_name))
                for prod in store['productList']:
                    del prod['logField']
                    del prod['picture']
                    del prod['productLabelPictureList']
                    prod['city'] = city
                    prod['province'] = province
                    prod['store'] = store_name
                    self.col.insert_one(prod)


if __name__ == '__main__':
    pc = PriceCrawler('荔枝')
    pc.get_fruit_data()
