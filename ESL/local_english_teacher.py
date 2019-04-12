import requests
import pandas as pd
from lxml import etree


class Job910(object):
    def __init__(self, max_page, com_type):
        self.start_urls = ['http://www.job910.com/search.aspx?funtype={}&keyword=英语老师&pageSize=20&' \
                           'pageIndex={}'.format(com_type, i) for i in range(1, max_page+1)]

    def get_data(self):
        for url in self.start_urls:
            res = requests.get(url)
            page = url.split('=')[-1]
            self.parse_data(res, page)
            print('成功爬取并保存第{}页数据!'.format(page))

    @staticmethod
    def parse_data(res, page):
        if res.status_code == 200:
            parsed = etree.HTML(res.text)

            title = parsed.xpath('//*[@class="position title"]/a/text()')
            link = parsed.xpath('//*[@class="position title"]/a/@href')
            salary = parsed.xpath('//*[@class="salary title"]/text()')
            company = parsed.xpath('//*[@class="com title adclick"]/text()')
            area = parsed.xpath('//*[@class="area title2"]/text()')
            update_time = parsed.xpath('//*[@class="time title2"]/text()')
            exp_title = parsed.xpath('//*[@class="exp title2"]/text()')

            data = pd.DataFrame({'title': title, 'link': link, 'salary': salary,
                                 'company': company, 'area': area, 'update_time': update_time,
                                 'exp_title': exp_title})
            if page == '1':
                data.to_csv('外语培训.csv', index=False, mode='a', header=True)
            else:
                data.to_csv('外语培训.csv', index=False, mode='a', header=False)

        else:
            print('链接{}请求不成功!'.format(res.url))


if __name__ == '__main__':
    job = Job910(26, 19)
    job.get_data()
"""
preschool: 207
certified: 547
ESL:561


"""