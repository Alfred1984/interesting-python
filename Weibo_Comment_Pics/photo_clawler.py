import os
import time
import requests


class CommentPhotoCrawler(object):
    """
    微博评论图片爬虫
    """
    def __init__(self, sleep_time=2):
        """
        初始化函数
        :param sleep_time: int, 默认为2, 爬取评论数据及图片的间隔时间

        :attr mid: string, 初始化为None, 由get_m_url方法爬取
        :attr login_headers: dict, 模拟登录请求头
        :attr session: requests Session
        """
        self.sleep_time = sleep_time
        self.mid = None
        self.login_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 '
                          '(KHTML, like Gecko)Chrome/48.0.2564.116 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Origin': 'https://passport.weibo.cn',
            'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo&r'
                       '=https%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt='
        }
        self.session = None

    def get_m_url(self, url):
        """
        爬取电脑端微博url对应的手机端微博id，从而拼接出手机端微博的url
        :param url: 所需爬取的电脑端微博url，结构为：https://weibo.com/博主的id/9位的字母+数字
        :return: None
        """
        # 电脑端微博爬取需要Cookie，具有时效性，需要自行更新，Cookie保存在cookie.txt
        with open('cookie.txt', 'r') as f:
            cookie = f.read()
        headers = {'Cookie': cookie}
        res = requests.get(url, headers=headers)
        idx = res.text.find('mblog&act=')  # 手机网页端id就在网页源代码的"mblog&act="字符串后面16位
        self.mid = res.text[idx+10:idx+26]
        print('对应的手机网页端id是：'+self.mid)

    def login(self, user, password):
        """
        模拟登录手机微博
        :param user: string, 你的微博用户名
        :param password: string, 你的微博密码
        :return: None
        """
        self.session = requests.Session()
        login_data = {
            'username': user,
            'password': password,
            'savestate': '1',
            'r': 'https://weibo.cn/',
            'ec': '0',
            'pagerefer': 'https://passport.weibo.cn/signin/welcome?entry='
                         'mweibo&r=https%3A%2F%2Fm.weibo.cn%2Fdetail%2F4333036507864049',
            'entry': 'mweibo',
            'mainpageflag': '1'
        }  # 表单数据
        login_url = 'https://passport.weibo.cn/sso/login'
        self.session.post(login_url, headers=self.login_headers, data=login_data)
        print('模拟登录手机网页端微博成功！')

    def get_comments(self, max_page):
        """
        爬取评论数据
        :param max_page: int or "all", 传入数字时，代表想要爬取的页数，传入"all"时，代表爬取该微博下的所有页数
        :return: None
        """
        if isinstance(max_page, int):  # 爬有限的页数
            # 第一页url不一样，需要单独处理
            url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0'.format(self.mid, self.mid)
            response = self.session.get(url, headers=self.login_headers)
            max_id = response.json()['data']['max_id']  # 找出下一页需要用的max_id
            max_id_type = response.json()['data']['max_id_type']  # 找出下一页需要用的max_id_type，每爬16页会变更
            self._store_pic_url(response)  # 保存图片url
            print('成功抓取第1页的图片链接！')

            if max_page > 1:
                for page in range(1, max_page):
                    url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}' \
                          '&max_id_type={}'.format(self.mid, self.mid, max_id, max_id_type)
                    response = self.session.get(url, headers=self.login_headers)
                    max_id = response.json()['data']['max_id']
                    max_id_type = response.json()['data']['max_id_type']
                    self._store_pic_url(response)
                    print('成功抓取第{}页的图片链接！'.format(page + 1))
                    time.sleep(self.sleep_time)  # 隔两秒再爬下一页

        if max_page == 'all':  # 爬取所有页数
            url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0'.format(self.mid, self.mid)
            response = self.session.get(url, headers=self.login_headers)
            max_id = response.json()['data']['max_id']
            max_id_type = response.json()['data']['max_id_type']
            self._store_pic_url(response)
            print('成功抓取第1页的图片链接！')
            page = 2

            while max_id != 0:  # 当返回的max_id为0时，说明我们来到了最后一页
                url = 'https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}' \
                      '&max_id_type={}'.format(self.mid, self.mid, max_id, max_id_type)
                response = self.session.get(url, headers=self.login_headers)
                max_id = response.json()['data']['max_id']
                max_id_type = response.json()['data']['max_id_type']
                self._store_pic_url(response)
                print('成功抓取第{}页的图片链接！'.format(page))
                page += 1
                time.sleep(2)  # 隔两秒再爬下一页

    @staticmethod
    def _store_pic_url(response):
        """
        解析响应的JSON数据里面的图片url，并把图片url保存在photourl.txt里
        :param response: 响应的评论数据
        :return: None
        """
        for comment in response.json()['data']['data']:
            if 'pic' in comment.keys():  # 需要检查一下评论中是不是有图片
                with open('photourl.txt', 'a') as f:
                    f.write(comment['pic']['large']['url']+'\n')

    def download_photo(self, output='.'):
        """
        从photourl.txt提取图片url，并下载图片到指定文件夹photos
        :param output: string, 保存photos文件夹的路径, 默认为当前工作路径
        :return: None
        """
        os.mkdir(output+'/photos')
        with open('photourl.txt', 'r') as f:
            photo_urls = [url.strip() for url in f.readlines()]
        for url in photo_urls:
            res = requests.get(url)
            name = url.split('/')[-1]  # 取出图片名
            with open(output+'/photos/'+name, 'wb') as f:
                f.write(res.content)
            print('成功保存图片：{}'.format(name))
            time.sleep(self.sleep_time)


if __name__ == '__main__':
    com = CommentPhotoCrawler()
    com.get_m_url('https://weibo.com/2610874582/HdRqGwZNv')
    com.login('', '')  # 传入你的微博用户名和密码
    com.get_comments(max_page=20)
    com.download_photo()
