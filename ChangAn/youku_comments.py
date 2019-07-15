import json
import requests
from pymongo import MongoClient


class CommentCrawler(object):
    def __init__(self):
        self.video_id = None
        client = MongoClient('127.0.0.1', 27017)
        self.db = client.get_database('Changan')
        self.col = None

    def get_video_id(self, v_url):
        res = requests.get(v_url)
        idx = res.text.find("videoId: '")
        if idx != -1:
            self.video_id = res.text[idx+10:idx+20]
            print('Video ID for corresponding url is :{}'.format(self.video_id))
        else:
            print('Can not get video id, please check the url you just input.')

    def get_comments(self, video_url, collection):
        self.get_video_id(video_url)

        self.col = self.db.get_collection(collection)
        self.col.ensure_index('id', unique=True)
        print('Built collection of: {}'.format(collection))

        base_url = 'https://p.comments.youku.com/ycp/comment/pc/commentList?jsoncallback=n_commentList' \
                   '&app=100-DDwODVkv&objectId={}&objectType=1&listType=0&' \
                   'currentPage={}&pageSize=30&sign=edb9eab487e78a7729408772d8691134&time=1562320232'
        page = 1
        while 1:
            try:
                res = requests.get(base_url.format(self.video_id, page), timeout=5)
                data = json.loads(res.text[res.text.find('{'):-1])
                for com in data['data']['comment']:
                    self.col.update({'id': com['id']}, {'$set': com}, upsert=True)

                print('Successfully crawl comments of video : {}, page :{}'.format(self.video_id, page))
                if page == data['data']['totalPage']:
                    print('Finished crawling all pages.')
                    break
                else:
                    page += 1
            except:
                print('Video: {} Page: {} request timeout! Moving to next page!'.format(self.video_id, page))
                page += 1


if __name__ == '__main__':
    cc = CommentCrawler()
    d = {'youku1': 'https://v.youku.com/v_show/id_XNDI0NDYyNjk1Mg'
                   '==.html?spm=a2h0j.11185381.listitem_page1.5~A&&s=efbfbd78efbfbd5cefbf',
         'youku2': 'https://v.youku.com/v_show/id_XNDI0NDQ0ODEwNA'
                   '==.html?spm=a2h0j.11185381.listitem_page1.5!2~A&&s=efbfbd78efbfbd5cefbf',
         'youku3': 'https://v.youku.com/v_show/id_XNDI0NDQ2MzU3Mg'
                   '==.html?spm=a2h0j.11185381.listitem_page1.5!3~A&&s=efbfbd78efbfbd5cefbf',
         'youku4': 'https://v.youku.com/v_show/id_XNDI0NDQ3NTMwMA'
                   '==.html?spm=a2h0j.11185381.listitem_page1.5!4~A&&s=efbfbd78efbfbd5cefbf',
         'youku5': 'https://v.youku.com/v_show/id_XNDI0NDQ5NzE3Ng'
                   '==.html?spm=a2h0j.11185381.listitem_page1.5!5~A&&s=efbfbd78efbfbd5cefbf',
         'youku6': 'https://v.youku.com/v_show/id_XNDI0NDUwODUxMg'
                   '==.html?spm=a2h0j.11185381.listitem_page1.5!6~A&&s=efbfbd78efbfbd5cefbf',
         'youku7': 'https://v.youku.com/v_show/id_XNDI0NDUxOTgyNA'
                   '==.html?spm=a2h0j.11185381.listitem_page1.5!7~A&&s=efbfbd78efbfbd5cefbf',
         'youku8': 'https://v.youku.com/v_show/id_XNDI0NDU1MjQxMg'
                   '==.html?spm=a2h0j.11185381.listitem_page1.5!8~A&&s=efbfbd78efbfbd5cefbf',
         'youku9': 'https://v.youku.com/v_show/id_XNDI0NDYzMzAyOA'
                   '==.html?spm=a2h0j.11185381.listitem_page1.5!9~A&&s=efbfbd78efbfbd5cefbf',
         'youku10': 'https://v.youku.com/v_show/id_XNDI0NDY1MzA3Ng='
                    '=.html?spm=a2h0j.11185381.listitem_page1.5!10~A&&s=efbfbd78efbfbd5cefbf'
         }
    for col, u in d.items():
        cc.get_comments(video_url=u, collection=col)
