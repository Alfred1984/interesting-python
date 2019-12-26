import os
import math
import googleapiclient.discovery
from pymongo import MongoClient


class YoutubeComment(object):
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.comment_col = client.get_database('Youtube').get_collection('comments')
        self.comment_col.ensure_index('c_id', unique=True)

        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        key = ""  # API key that you get from YouTube Data API v3

        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, developerKey=key)

        self.pageToken = ''

    def get_comments(self, video_id, number):
        pages = math.ceil(number/100)
        for page in range(1, pages+1):

            request = self.youtube.commentThreads().list(
                part="snippet",
                pageToken=self.pageToken,
                videoId=video_id,
                maxResults=100
            )
            response = request.execute()
            if response.get('pageInfo').get('totalResults') > 0:
                print(f'Crawling page: {page}')
                self.pageToken = response.get('nextPageToken')

                for item in response.get('items'):
                    try:
                        tl_item = item.get('snippet').get('topLevelComment')
                        c_id = tl_item.get('id')
                        author = tl_item.get('snippet').get('authorDisplayName')
                        author_id = tl_item.get('snippet').get('authorChannelId').get('value')
                        video_id = tl_item.get('snippet').get('videoId')
                        text = tl_item.get('snippet').get('textOriginal')
                        rating = tl_item.get('snippet').get('viewerRating')
                        like_count = tl_item.get('snippet').get('likeCount')
                        publish_time = tl_item.get('snippet').get('publishedAt')
                        reply_count = item.get('snippet').get('totalReplyCount')

                        comment = {'c_id': c_id,
                                   'author': author,
                                   'author_id': author_id,
                                   'video_id': video_id,
                                   'text': text,
                                   'rating': rating,
                                   'like_count': like_count,
                                   'publish_time': publish_time,
                                   'reply_count': reply_count}
                        self.comment_col.update({'c_id': c_id},
                                                {'$set': comment},
                                                upsert=True)
                        print(f'Inserted comment: {comment}')
                    except AttributeError:
                        print('------AttributeError occurred!-------')

            else:
                print(f'Can not get crawl page: {page}')


if __name__ == '__main__':
    yc = YoutubeComment()
    for v_id, num in {'FWMIPukvdsQ': 30784,
                      'QHTnuI9IKBA': 14888,
                      'LTejJnrzGPM': 46285}:
        yc.get_comments(video_id=v_id,
                        number=num)
