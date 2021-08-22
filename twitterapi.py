import asyncio
import json
import os
import math
import random
import string
import time
import urllib.request
from urllib.parse import urlparse

import aiohttp
from dotenv import find_dotenv, load_dotenv
from requests_oauthlib import OAuth1Session
import tqdm

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


def getAccountTwitterData(user_name, repeat=20, media_dl=False):
    params = {'screen_name': user_name, 'exclude_replies': True,
              'include_rts': False, 'count': 200}  # 取得パラメータ
    tweets = []
    image_urls = set()
    video_urls = set()

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
                        image_urls.add(media["media_url"])

                        video_info = media["video_info"]["variants"]
                        info = sorted(
                            video_info, key=lambda x: "bitrate" in x and -x["bitrate"])
                        video_urls.add(info[0]["url"])
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
        downloadAllImage(image_urls, keyword=user_name)
        removeSameImage(f"./output/img/{user_name}")

        a_s = time.time()
        asyncDownloadAllVideo(video_urls, keyword=user_name)
        e_s = time.time() - a_s

        print(f"\nAsync Download : {e_s}s")

    print("Number of tweets acquired：%s" % len(tweets))
    return tweets


def getKeywordTwitterData(keyword, repeat=20, media_dl=False):
    params = {'q': keyword.replace(
        "_", " "), 'count': 200, 'result_type': 'mixed'}  # 取得パラメータ
    tweets = []
    image_urls = set()
    video_urls = set()

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
                        image_urls.add(media["media_url"])

                        video_info = media["video_info"]["variants"]
                        info = sorted(
                            video_info, key=lambda x: "bitrate" in x and -x["bitrate"])
                        video_urls.add(info[0]["url"])
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
        downloadAllImage(image_urls, keyword=keyword)
        removeSameImage(f"./output/img/{keyword}")

        downloadAllVideo(video_urls, keyword=keyword)

    print("\nNumber of tweets acquired：%s" % len(tweets))
    return tweets


def downloadAllImage(url_list, keyword="unknown"):
    print("\nDownload Progress(Image): ")
    for url in tqdm.tqdm(url_list):
        downloadImageFromURL(url, keyword=keyword)


def downloadAllVideo(url_list, keyword="unknown"):
    print("\nDownload Progress(Video): ")
    for url in tqdm.tqdm(url_list):
        downloadVideoFromURL(url, keyword=keyword)


def asyncDownloadAllImage(url_list, keyword="unknown"):
    pass


def asyncDownloadAllVideo(url_list, keyword="unknown"):
    # for windows
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.get_event_loop()
    to_do = [asyncDownloadVideoFromURL(
        url, keyword=keyword) for url in url_list]
    wait_coro = asyncio.wait(to_do)
    r, _ = loop.run_until_complete(wait_coro)
    loop.close()


async def asyncDownloadImageFromURL(url, keyword="unknown"):
    pass


async def asyncDownloadVideoFromURL(url, keyword="unknown"):
    path = urlparse(url).path
    ext = os.path.splitext(path)[1]

    file_path = f"./output/video/{keyword}"
    os.makedirs(file_path, exist_ok=True)

    chunk_size = 10

    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=600) as r:
            with open(f"{file_path}/{randomName(6)}{ext}", "wb") as f:
                while True:
                    chunk = await r.content.read(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)


def downloadImageFromURL(url, keyword="unknown"):
    file_path = f"./output/img/{keyword}"
    os.makedirs(file_path, exist_ok=True)
    urllib.request.urlretrieve(url, f"{file_path}/{randomName(6)}.jpg")


def downloadVideoFromURL(url, keyword="unknown"):
    path = urlparse(url).path
    ext = os.path.splitext(path)[1]

    file_path = f"./output/video/{keyword}"
    os.makedirs(file_path, exist_ok=True)

    try:
        with urllib.request.urlopen(url) as r:
            with open(f"{file_path}/{randomName(6)}{ext}", "wb") as f:
                f.write(r.read())
    except Exception:
        pass


def randomName(n):
    randlst = [random.choice(string.ascii_letters + string.digits)
               for i in range(n)]
    return "".join(randlst)
