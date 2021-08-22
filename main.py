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
    psr.add_argument('-s', '--show')

    return psr.parse_args()


def main(user_name=None, keyword=None, stopwords_path=None, media_dl=False, show=True):
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

    if not media_dl:
        # ストップワードのリストの読み込み
        stopword_list = MakeStopwordList(stopwords_path)

        # ツイート内に出てくる名詞の頻度を計算
        freq_dict = CountWord(
            tweets, keyword=user_name or keyword, stopword_list=stopword_list)

        # TFの計算と表示
        # tf_dict = CalcTF(freq_dict)
        # PrintWordsTF(tf_dict)

        # ワードクラウドの作成
        DrawWordCloud(freq_dict, title=title, show=show)

        elapsed_time = time.time() - start
        print(f"\nElapsed time: {round(elapsed_time, 2)}s")


if __name__ == '__main__':
    args = get_args()
    media_dl = False
    show = True
    if args.download is not None and args.download.lower() == "true":
        media_dl = True
    if args.show is not None and args.show.lower() == "true":
        show = True
    main(user_name=args.user, keyword=args.keyword,
         stopwords_path="stopword_ja.txt", media_dl=media_dl, show=show)
