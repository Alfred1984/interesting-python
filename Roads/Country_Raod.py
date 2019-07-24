import re
import requests
from lxml import etree
from pymongo import MongoClient


class Roads(object):
    def __init__(self):
        self.city_list = None
        self.alphabets = None
        self.na_city = []
        client = MongoClient('127.0.0.1', 27017)
        self.col = client.get_database('Country_Road').get_collection('city_roads')

    def get_city_list(self):
        url = 'http://www.city8.com/'
        res = requests.get(url)

        pat1 = r"city8.com/'>(.*?)</a></li>"
        pat2 = r"<a target='_blank' href='(.*?)/'>"
        city = re.findall(string=res.text, pattern=pat1)
        href = re.findall(string=res.text, pattern=pat2)
        self.city_list = dict(zip(city, href))
        print('Got city list!')

    def get_alphabet(self):
        url = 'http://gz.city8.com/road/A/'
        res = requests.get(url)
        parsed = etree.HTML(res.text)
        self.alphabets = parsed.xpath("/html/body/div/div[2]/div[3]/div[1]/div[1]/div[1]/a/text()")
        print('Got alphabets!')

    def get_city_roads(self):
        for city, href in self.city_list.items():
            res_test = requests.get(href+'/road')

            if res_test.text.find('/road/a/') != -1:
                print('Crawling road data of city: {}'.format(city))

                for alpha in self.alphabets:
                    res_road = requests.get(href+'/road/'+alpha)
                    parsed = etree.HTML(res_road.text)
                    roads = parsed.xpath('/html/body/div/div[2]/div[3]/div[1]/div[2]/a/text()')
                    if len(roads) > 0:
                        for rd in roads:
                            self.col.insert_one({'city': city, 'road': rd.strip()})
                        print('Successfully crawled city: {}, alphabet: {}'.format(city, alpha))
                    else:
                        print('City: {} alphabet: {} got no data'.format(city, alpha))

            else:
                print('There is no road data of city: {}'.format(city))
                self.na_city.append(city)

        print('These are cities with no road data: {} \n '
              'You might want to crawl road data of these cities from elsewhere.'.format(self.na_city))


if __name__ == '__main__':
    r = Roads()
    r.get_city_list()
    r.get_alphabet()
    r.get_city_roads()
