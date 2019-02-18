#!/usr/bin/python
# -*- coding:utf-8 -*-
import time
import requests
import pandas as pd
from lxml import etree


class AQI(object):
    """
    爬取城市AQI实时数据
    """
    def __init__(self):
        """
        初始化函数
        :attr encoding: 编码
        """
        self.encoding = None

    def get_encoding(self):
        """
        获取网页的编码
        :return: None
        """
        res = requests.get('http://datacenter.mee.gov.cn/aqiweb2/')
        self.encoding = res.apparent_encoding
        print('Successfully crawled encoding!')
        time.sleep(2)

    def crawl_aqi(self, sleep_time=3600):
        """
        爬取全国具有监测点的所有城市的AQI实时数据，每小时爬取一次
        :param sleep_time: 爬取间隔时间，默认3600秒
        :return: None
        """
        write_header = True
        while 1:
            res = requests.get('http://datacenter.mee.gov.cn/aqiweb2/')
            parsed_text = etree.HTML(res.text)
            timestamp = parsed_text.xpath('/html/body/div[3]/p/i/text()')[0].replace('年', '-'). \
                replace('月', '-').replace('日', ' ').replace('时', ':00:00')
            print('Successfully crawled timestamp!')

            # 直接使用pandas获取和解析数据
            data_res = pd.read_html('http://datacenter.mee.gov.cn/aqiweb2/', encoding=self.encoding)
            data = data_res[0]
            header = ['city', 'AQI', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'main_pollution']
            data.columns = header
            data['time'] = timestamp
            if write_header is True:
                data.to_csv('/root/dmproj/AQI/data.csv', index=False, mode='a', header=True)
                write_header = False
            else:
                data.to_csv('/root/dmproj/AQI/data.csv', index=False, mode='a', header=False)
            print('Successfully crawled data of {} and saved it to file!'.format(timestamp))
            time.sleep(sleep_time)


if __name__ == '__main__':
    aqi = AQI()
    aqi.get_encoding()
    aqi.crawl_aqi()
