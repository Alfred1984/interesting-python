#!/usr/bin/python
# -*- coding:utf-8 -*-

import time
import requests
from lxml import etree
import pandas as pd


def sxs_spider(job, pages):
    # 定义函数，爬取通过职位搜索得到的每个职位信息，把爬取的内容保存到本地的csv文件中，参数为：
    # job：搜索的职位
    # pages：爬取的页数（需要根据总共有多少页而定）
    print('Job: {}, '.format(job), 'pages: {}. '.format(str(pages)), 'Challenge accepted!')
    base_url = 'https://www.shixiseng.com/interns?'
    for page in range(1, pages+1):
        url = base_url + 'k=' + job + '&p=' + str(page)
        response = requests.get(url=url)
        time.sleep(2)  # 怕有反爬，每页睡两秒，当然也可以去掉
        decrypted_text = decrypt_text(response.text)  # 爬取回来的原始数据都是经过字体加密的，需要定义一个函数解密
        basic_data = process_text(decrypted_text)  # 定义一个函数处理解密后的文本，返回一个pd.DataFrame格式数据
        if page == 1:
            basic_data.to_csv('/Users/apple/Desktop/{}.csv'.format(job), index=False)  # 保存数据，注意第一页与其它页的区别
        else:
            basic_data.to_csv('/Users/apple/Desktop/{}.csv'.format(job), index=False, header=False, mode='a')
            # 第二页及以后要省去header，mode改为"a"， 即append

        print('Successfully crawled page {} and saved it to csv file.'.format(page))


mapping = {'&#xe66f': '0', '&#xe50e': '1', '&#xf19c': '2', '&#xe2d1': '3', '&#xe372': '4',
           '&#xeb5a': '5', '&#xf37c': '6', '&#xf8b6': '7', '&#xf252': '8', '&#xf3a0': '9'}  # 映射字典，使用时需自行更新


def decrypt_text(text):
    # 定义文本信息处理函数，通过字典mapping中的映射关系解密
    for key, value in mapping.items():
        text = text.replace(key, value)
    return text


def process_text(text):
    # 文本处理函数
    parsed_text = etree.HTML(text)
    com_links = process_links(parsed_text.xpath('//*[@class="company-box"]/a/@href'))
    # 爬取回来的链接是相对路径，定义一个process_links函数把路径补全
    job_links = process_links(parsed_text.xpath('//*[@class="name-box clearfix"]/a/@href'))
    tag = parsed_text.xpath('//*[@class="company-box"]/span[2]/text()')
    released_time = parsed_text.xpath('//*[@class="name-box clearfix"]/span/text()')
    wage = parsed_text.xpath('//*[@class="more"]/span[1]/text()')
    day_per_week = parsed_text.xpath('//*[@class="more"]/span[2]/text()')
    time_span = parsed_text.xpath('//*[@class="more"]/span[3]/text()')
    (com_name, com_intro, city, num_employee, industry, com_logo, detailed_intro, com_fullname,
     com_website, com_class, com_id, est_date, auth_capital, com_welfare) = com_detailed_data(com_links)
    # 定义一个com_detailed_data函数爬取公司详情页信息
    (job_title, update_time, job_academic, job_detail, job_deadline, com_location) = job_detailed_data(job_links)
    # 定义一个job_detailed_data函数爬取职位详情页信息

    data = {'com_links': com_links, 'job_links': job_links, 'tag': tag,
            'released_time': released_time, 'wage': wage, 'day_per_week': day_per_week, 'time_span': time_span,
            'com_name': com_name, 'com_intro': com_intro, 'city': city, 'num_employee': num_employee,
            'industry': industry, 'com_logo': com_logo, 'detailed_intro': detailed_intro, 'com_fullname': com_fullname,
            'com_website': com_website, 'com_class': com_class, 'com_id': com_id, 'est_date': est_date,
            'auth_capital': auth_capital, 'com_welfare': com_welfare, 'job_title': job_title,
            'update_time': update_time, 'job_academic': job_academic, 'job_detail': job_detail,
            'job_deadline': job_deadline, 'com_location': com_location,
            }

    basic_data = pd.DataFrame.from_dict(data=data)

    return basic_data


def process_links(links):
    # 链接处理函数
    return ['https://www.shixiseng.com' + link for link in links]


def com_detailed_data(links):
    # 爬取公司详情页信息
    com_name, com_intro, city, num_employee, industry, com_logo, detailed_intro, com_fullname, com_website,\
    com_class, com_id, est_date, auth_capital, com_welfare = [], [], [], [], [], [], [], [], [], [], [], [], [], []

    for link in links:
        response = requests.get(link)
        time.sleep(2)  # 怕有反爬，每页再睡两秒
        parsed_text = etree.HTML(response.text)
        com_name.append(process_list(parsed_text.xpath('//*[@class="com_name"]/text()')))
        # xpath在匹配不到内容的时候会返回空列表，很蛋疼，所以定义了一个process_list函数，匹配到返回字符串，匹配不到返回None，下同
        com_intro.append(process_list(parsed_text.xpath('//*[@class="com_introduce"]/text()')))
        city.append(process_list(parsed_text.xpath('//*[@class="com_position"]/text()')))
        num_employee.append(process_list(parsed_text.xpath('//*[@class="com_num"]/text()')))
        industry.append(process_list(parsed_text.xpath('//*[@class="com_class"]/text()')))
        com_logo.append(process_list(parsed_text.xpath('/html/body/div[1]/div[2]/div[1]/img/@src')))

        if len(parsed_text.xpath('//*[@class="content_left"]/div[1]/div[1]/div[2]/text()')) > 0:  # 简介信息需要特殊处理
            detailed_intro.append(parsed_text.xpath('//*[@class="content_left"]/div[1]/div[1]/div[2]/text()')[0])
        elif len(parsed_text.xpath('//*[@class="content_left"]/div[1]/div[1]/div[2]/p/text()')) > 0:
            detailed_intro.append(''.join(
                parsed_text.xpath('//*[@class="content_left"]/div[1]/div[1]/div[2]/p/text()')))
        else:
            detailed_intro.append(None)

        com_fullname.append(process_list(parsed_text.xpath('//*[@class="content_right"]/div[1]/div[2]/text()')))
        com_class.append(process_list(parsed_text.xpath('//*[@class="content_right"]/div[2]/div[2]/text()')))
        com_id.append(process_list(parsed_text.xpath('//*[@class="content_right"]/div[2]/div[3]/text()')))
        est_date.append(process_list(parsed_text.xpath('//*[@class="content_right"]/div[2]/div[4]/text()')))
        auth_capital.append(process_list(parsed_text.xpath('//*[@class="content_right"]/div[2]/div[5]/text()')))
        com_welfare.append(parsed_text.xpath('//*[@class="content_right"]/div[3]/div[2]/span/text()'))
        # 公司福利由于返回的是一个多元素列表，也特殊处理, 其实好像用''.join()更方便日后数据处理，不过这里先给自己挖一个坑
        com_website.append(process_list(parsed_text.xpath('//*[@class = "com_link"]/@href')))

    return (com_name, com_intro, city, num_employee, industry, com_logo, detailed_intro,
            com_fullname, com_website, com_class, com_id, est_date, auth_capital, com_welfare)


def process_list(li):
    # xpath返回的列表处理函数
    if len(li) > 0:
        return li[0]
    else:
        return None


def job_detailed_data(links):
    # 爬取职位详情页信息
    job_title, update_time, job_academic, job_detail, job_deadline, com_location = [], [], [], [], [], []
    for link in links:
        response = requests.get(link)
        time.sleep(2)
        parsed_text = etree.HTML(decrypt_text(response.text))  # 这个文本内容也是需要解密的
        job_title.append(process_list(parsed_text.xpath('//*[@class="new_job_name"]/text()')))
        update_time.append(process_list(parsed_text.xpath('//*[@class="cutom_font"]/text()')))
        job_academic.append(process_list(parsed_text.xpath('//*[@class="job_academic"]/text()')))

        if len(parsed_text.xpath('//*[@class = "job_detail"]/p/text()')) > 0:
            job_detail.append(parsed_text.xpath('//*[@class = "job_detail"]/p/text()'))
        elif len(parsed_text.xpath('//*[@class = "job_detail"]/p/span/text()')) > 0:
            job_detail.append(parsed_text.xpath('//*[@class = "job_detail"]/p/span/text()'))
        else:
            job_detail.append(None)

        job_deadline.append(process_list(parsed_text.xpath('//*[@class="job_detail cutom_font"]/text()')))
        com_location.append(process_list(parsed_text.xpath('//*[@class="com_position"]/text()')))

    return (job_title, update_time, job_academic,
            job_detail, job_deadline, com_location)


if __name__ == '__main__':
    sxs_spider('算法', 64)
    print('Mission completed!')
