import pandas as pd
import requests
from snownlp import SnowNLP
from aip import AipNlp
from QcloudApi.qcloudapi import QcloudApi


data = pd.read_csv('/root/dmproj/mongotv/data/data.csv')

# SnowNLP API


def get_sent_snownlp(data):
    s = SnowNLP(str(data))
    return s.sentiments


data['sent_snownlp'] = data['content'].apply(get_sent_snownlp)

# 百度API
APP_ID = '你的 APP_ID'
API_KEY = '你的 API_KEY'
SECRET_KEY = '你的 SECRET_KEY'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


def get_sent_baidu(data):
    return_data = client.sentimentClassify(data)
    items = return_data.get('items')
    if items:
        return items[0]['positive_prob']


data['sent_baidu'] = data['content'].apply(get_sent_baidu)

# 腾讯API
module = 'wenzhi'
action = 'TextSentiment'
config = {'Region':'gz',
          'secretId':'你的 secretId',
          'secretKey':'你的 secretKey'}
service = QcloudApi(module, config)


def get_sent_tc(data):

    action_params = {'content': data}
    url = service.generateUrl(action, action_params)
    response = requests.get(url).json()
    positive = response.get('positive')
    if positive is not None:
        return positive


data['sent_tencent'] = data['content'].apply(get_sent_tc)

