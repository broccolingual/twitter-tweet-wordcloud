import argparse
import time

from matplotlib.pyplot import title

from twitterapi import getAccountTwitterData, getKeywordTwitterData
from stopword import MakeStopwordList
from analysis import CountWord, CalcTF, PrintWordsTF
from utils import DrawWordCloud


def get_args():
    psr = argparse.ArgumentParser()
    psr.add_argument('-u', '--user')
    psr.add_argument('-k', '--keyword')
    psr.add_argument('-d', '--download')

    return psr.parse_args()


def main(user_name=None, keyword=None, stopwords_path=None, media_dl=False):
    start = time.time()

    # Twitter APIからツイートの本文のリストを取得
    if user_name:
        print(f"Search from @{user_name}(user)")
        tweets = getAccountTwitterData(user_name, repeat=20, media_dl=media_dl)
        title = user_name
    elif keyword:
        print(f"Search from {keyword.replace('_', ' ')}(timeline)")
        tweets = getKeywordTwitterData(keyword, repeat=20, media_dl=media_dl)
        title = keyword
    else:
        print("Error: 引数が指定されていません.")
        exit(1)

    # ストップワードのリストの読み込み
    stopword_list = MakeStopwordList(stopwords_path)

    # ツイート内に出てくる名詞の頻度を計算
    freq_dict = CountWord(
        tweets, keyword=user_name or keyword, stopword_list=stopword_list, jp_only=True)

    # TFの計算と表示
    tf_dict = CalcTF(freq_dict)
    PrintWordsTF(tf_dict)

    # ワードクラウドの作成
    DrawWordCloud(freq_dict, title=title, show=False)

    elapsed_time = time.time() - start
    print(f"\nElapsed time: {round(elapsed_time, 2)}s")


if __name__ == '__main__':
    args = get_args()
    media_dl = False
    if args.download is not None and args.download.lower() == "true":
        media_dl = True
    main(user_name=args.user, keyword=args.keyword,
         stopwords_path="stopword_ja.txt", media_dl=media_dl)
