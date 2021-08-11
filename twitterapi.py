import json
import os

from dotenv import find_dotenv, load_dotenv
from requests_oauthlib import OAuth1Session

env_file = find_dotenv()
load_dotenv(env_file)

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
ACCESS_KEY_SECRET = os.environ.get('ACCESS_KEY_SECRET')

twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_KEY_SECRET)

def getAccountTwitterData(user_name, repeat=20):
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    params ={'screen_name':user_name,'exclude_replies':True,'include_rts':False,'count':200} #取得パラメータ
    tweets = []

    mid = -1

    for i in range(repeat):
        if mid != -1: # 初回のみmax_idの指定を解除する
            params['max_id'] = mid # midよりも古いIDのツイートのみを取得する

        res = twitter.get(url, params = params)

        if res.status_code == 200: #正常通信出来た場合
            sub_tweets = json.loads(res.text) #レスポンスからツイート情報を取得
            user_ids = []

            for tweet in sub_tweets:
                user_ids.append(int(tweet['id']))
                tweets.append(tweet)

            if len(user_ids) > 0:
                min_user_id = min(user_ids)
                mid = min_user_id - 1

            else:
                mid = -1

        else: #正常通信出来なかった場合
            print("Failed: %d" % res.status_code)
            break

    print("Number of tweets acquired：%s" % len(tweets))
    return tweets