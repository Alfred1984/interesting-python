#!/usr/bin/python
# -*- coding:utf-8 -*-
import requests
import pandas as pd


def sxs_crawl(pages=30, kw='数据挖掘', c='全国'):
    list_urls = ["https://iosapi.shixiseng.com/app/interns/search?c={}&d=&ft=&i=&k={}"
                "&m=&page={}&s=-0&st=&t=zj&x=&z=".format(c, kw, page) for page in range(pages)]
    job_list_data = []
    for url in list_urls:
        response = requests.get(url)
        if response.json()['msg']:
            job_list_data.extend(response.json()['msg'])
        else:
            break
    job_list = pd.DataFrame(job_list_data)
    job_list.to_csv('/Users/apple/Desktop/job_list.csv', index=False)

    # 职位详情ID爬取
    uuids = list(job_list['uuid'])
    job_detailed_url = ['https://iosapi.shixiseng.com/app/intern/info?uuid={}'.format(uuid) for uuid in uuids]

    job_detailed_data = []
    for url in job_detailed_url:
        response = requests.get(url)
        job_detailed_data.append(response.json()['msg'])
    job_detailed = pd.DataFrame(job_detailed_data)
    job_detailed.to_csv('/Users/apple/Desktop/job_detailed.csv', index=False)

    # 公司信息爬取
    cuuids = list(job_detailed['cuuid'])
    com_detailed_url = ['https://iosapi.shixiseng.com/app/company/info?uuid={}'.format(cuuid) for cuuid in cuuids]
    com_detailed_data = []
    for url in com_detailed_url:
        response = requests.get(url)
        com_detailed_data.append(response.json()['msg'])
    com_detailed = pd.DataFrame(com_detailed_data)
    com_detailed.to_csv('/Users/apple/Desktop/com_detailed.csv', index=False)

    print('Successfully crawled {} jobs.'.format(job_list.shape[0]))


if __name__ == '__main__':
    sxs_crawl(pages=30, kw='数据挖掘', c='全国')