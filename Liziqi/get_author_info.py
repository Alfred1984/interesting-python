import os
import math
import random
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from pymongo import MongoClient


class YoutubeChannel(object):
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.comment_col = client.get_database('Youtube').get_collection('comments')
        author_id_list = self.comment_col.find({}, {'author_id': 1, '_id': 0})
        self.author_id = list(set([i['author_id'] for i in author_id_list]))
        random.shuffle(self.author_id)

        self.author_info_col = client.get_database('Youtube').get_collection('author_info')
        self.author_info_col.ensure_index('author_id', unique=True)

        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = ""  # .json file that you got from YouTube Data API v3

        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        self.youtube = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

    def get_channels(self, number):
        """
        get YouTube channel information by channel id (self.author_id),
        requesting 50 channel ids per request would accelerate
        :param number: number of channel ids
        :return:
        """
        pages = math.ceil(number/50)
        for page in range(pages):

            a_id = ','.join(self.author_id[page*50: (page+1)*50])

            request = self.youtube.channels().list(
                part="snippet, statistics",
                id=a_id,
                maxResults=50
            )
            response = request.execute()

            if response.get('pageInfo').get('totalResults') > 0:
                print(f'Crawling page: {page}')

                for item in response.get('items'):
                    author = item.get('snippet').get('title')
                    author_id = item.get('id')
                    description = item.get('snippet').get('description')
                    country = item.get('snippet').get('country')
                    view_count = item.get('statistics').get('viewCount')
                    comment_count = item.get('statistics').get('commentCount')
                    subscriber_count = item.get('statistics').get('subscriberCount')
                    video_count = item.get('statistics').get('videoCount')

                    author_info = {'author_id': author_id,
                                   'author': author,
                                   'description': description,
                                   'country': country,
                                   'view_count': view_count,
                                   'comment_count': comment_count,
                                   'subscriber_count': subscriber_count,
                                   'video_count': video_count}
                    self.author_info_col.update({'author_id': author_id},
                                                {'$set': author_info},
                                                upsert=True)
                    print(f'Inserted comment: {author_info}')

            else:
                print(f'Can not get crawl page: {page}')


if __name__ == '__main__':
    yc = YoutubeChannel()
    yc.get_channels(number=63768)
