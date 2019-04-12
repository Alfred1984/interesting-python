import requests
import pandas as pd
from lxml import etree


class TeachInChina(object):
    def __init__(self, max_page):
        self.start_urls = ['http://www.jobleadchina.com/job?job_industry=Teaching' \
                           '&company_name=&page={}'.format(page) for page in range(1, max_page+1)]

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

            title = parsed.xpath('//*[@class="positionTitle"]/a/text()')
            link = parsed.xpath('//*[@class="positionTitle"]/a/@href')
            salary = [slr.strip() for slr in parsed.xpath('//*[@class="salaryRange"]/text()')]
            company = parsed.xpath('//*[@class="companyName"]/a/text()')
            area = parsed.xpath('//*[@class="jobThumbnailCompanyIndustry"]/span[3]/text()')
            update_time = parsed.xpath('//*[@class="post-time"]/text()')
            exp_title = parsed.xpath('//*[@class="jobThumbnailPositionRequire"]/span[3]/text()')
            education = parsed.xpath('//*[@class="jobThumbnailPositionRequire"]/span[1]/text()')
            com_type = parsed.xpath('//*[@class="jobThumbnailCompanyIndustry"]/span[1]/text()')

            data = pd.DataFrame({'title': title, 'link': link, 'salary': salary,
                                 'company': company, 'area': area, 'update_time': update_time,
                                 'exp_title': exp_title, 'education': education,
                                 'com_type': com_type})
            if page == '1':
                data.to_csv('jobleadchina.csv', index=False, mode='a', header=True)
            else:
                data.to_csv('jobleadchina.csv', index=False, mode='a', header=False)

        else:
            print('链接{}请求不成功!'.format(res.url))


if __name__ == '__main__':
    job = TeachInChina(96)
    job.get_data()
