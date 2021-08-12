import argparse

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
    if user_name:
        print(f"Search from @{user_name}(user)")
        tweets = getAccountTwitterData(user_name, repeat=10, media_dl=media_dl)
        title = user_name
    elif keyword:
        print(f"Search from {keyword.replace('_', ' ')}(timeline)")
        tweets = getKeywordTwitterData(keyword, repeat=10, media_dl=media_dl)
        title = keyword
    else:
        print("Error: 引数が指定されていません.")
        exit(1)

    stopword_list = MakeStopwordList(stopwords_path)
    freq_dict = CountWord(tweets, stopword_list=stopword_list)
    tf_dict = CalcTF(freq_dict)
    PrintWordsTF(tf_dict)
    DrawWordCloud(freq_dict, title=title, show=False)


if __name__ == '__main__':
    args = get_args()
    media_dl = False
    if args.download is not None and args.download.lower() == "true":
        media_dl = True
    main(user_name=args.user, keyword=args.keyword,
         stopwords_path="stopword_ja.txt", media_dl=media_dl)
