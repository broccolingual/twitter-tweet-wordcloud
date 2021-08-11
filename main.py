import sys

from twitterapi import getAccountTwitterData, getKeywordTwitterData, getMediaData
from stopword import MakeStopwordList
from analysis import CountWord, CalcTF, PrintWordsTF
from utils import DrawWordCloud

def main(user_name=None, keyword=None, stopwords_path=None, media_dl=False):
    if user_name:
        tweets = getAccountTwitterData(user_name, repeat=10)
    elif keyword:
        tweets =getKeywordTwitterData(keyword, repeat=10)
    
    # if media_dl:
    #     getMediaData(keyword)

    stopword_list = MakeStopwordList(stopwords_path)
    freq_dict = CountWord(tweets, stopword_list=stopword_list)
    tf_dict = CalcTF(freq_dict)
    PrintWordsTF(tf_dict)
    DrawWordCloud(freq_dict, title=keyword, show=True)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit(1)
    search_word = sys.argv[1]
    main(user_name=None, keyword=search_word, stopwords_path="stopword_ja.txt", media_dl=False)