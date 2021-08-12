import json
import os
import math
import random
import string
import tqdm
import urllib.request

from dotenv import find_dotenv, load_dotenv
from requests_oauthlib import OAuth1Session

from utils import removeSameImage

env_file = find_dotenv()
load_dotenv(env_file)

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
ACCESS_KEY_SECRET = os.environ.get('ACCESS_KEY_SECRET')

twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET,
                        ACCESS_KEY, ACCESS_KEY_SECRET)

URL_USER_TIMELINE = "https://api.twitter.com/1.1/statuses/user_timeline.json"
URL_KEYWORD_TIMELINE = "https://api.twitter.com/1.1/search/tweets.json"


def getAccountTwitterData(user_name, repeat=3, media_dl=False):
    params = {'screen_name': user_name, 'exclude_replies': True,
              'include_rts': False, 'count': 200}  # 取得パラメータ
    tweets = []
    media_urls = set()

    mid = -1

    for i in range(repeat):
        if mid != -1:  # 初回のみmax_idの指定を解除する
            params['max_id'] = mid  # midよりも古いIDのツイートのみを取得する

        res = twitter.get(URL_USER_TIMELINE, params=params)

        if res.status_code == 200:  # 正常通信出来た場合
            sub_tweets = json.loads(res.text)  # レスポンスからツイート情報を取得
            user_ids = []

            for tweet in sub_tweets:
                user_ids.append(int(tweet['id']))
                tweets.append(tweet)

                try:
                    media_list = tweet["extended_entities"]["media"]
                    for media in media_list:
                        media_urls.add(media["media_url"])
                except KeyError:
                    pass

            if len(user_ids) > 0:
                min_user_id = min(user_ids)
                mid = min_user_id - 1

            else:
                mid = -1

        else:  # 正常通信出来なかった場合
            print("Failed: %d" % res.status_code)
            break

    if media_dl:
        downloadAllImage(media_urls, keyword=user_name)
        removeSameImage(f"./output/img/{user_name}")

    print("Number of tweets acquired：%s" % len(tweets))
    return tweets


def getKeywordTwitterData(keyword, repeat=3, media_dl=False):
    params = {'q': keyword.replace(
        "_", " "), 'count': 200, 'result_type': 'mixed'}  # 取得パラメータ
    tweets = []
    media_urls = set()

    mid = -1

    for i in range(repeat):
        if mid != -1:  # 初回のみmax_idの指定を解除する
            params['max_id'] = mid  # midよりも古いIDのツイートのみを取得する

        res = twitter.get(URL_KEYWORD_TIMELINE, params=params)

        if res.status_code == 200:  # 正常通信出来た場合
            timeline = json.loads(res.text)  # レスポンスからツイート情報を取得
            user_ids = []

            for tweet in timeline["statuses"]:
                user_ids.append(int(tweet['id']))
                tweets.append(tweet)

                try:
                    media_list = tweet["extended_entities"]["media"]
                    for media in media_list:
                        media_urls.add(media["media_url"])
                except KeyError:
                    pass

            if len(user_ids) > 0:
                min_user_id = min(user_ids)
                mid = min_user_id - 1

            else:
                mid = -1

        else:  # 正常通信出来なかった場合
            print("Failed: %d" % res.status_code)
            break

    if media_dl:
        downloadAllImage(media_urls, keyword=keyword)
        removeSameImage(f"./output/img/{keyword}")

    print("\nNumber of tweets acquired：%s" % len(tweets))
    return tweets


def downloadAllImage(url_list, keyword="unknown"):
    print("\nDownload Progress: ")
    for url in tqdm.tqdm(url_list):
        downloadFromURL(url, keyword=keyword)


def downloadFromURL(url, keyword="unknown"):
    file_path = f"./output/img/{keyword}"
    os.makedirs(file_path, exist_ok=True)
    urllib.request.urlretrieve(url, f"{file_path}/{randomName(6)}.jpg")


def randomName(n):
    randlst = [random.choice(string.ascii_letters + string.digits)
               for i in range(n)]
    return "".join(randlst)
