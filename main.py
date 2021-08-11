import sys

from twitterapi import getAccountTwitterData
from stopword import MakeStopwordList
from analysis import CountWord
from utils import DrawWordCloud

def main(user_name, stopwords_path):
    tweets = getAccountTwitterData(user_name, repeat=10)
    stopword_list = MakeStopwordList(stopwords_path)
    freq_dict = CountWord(tweets, stopword_list=stopword_list)
    DrawWordCloud(freq_dict, user_name=user_name, show=True)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit(1)
    user_name = sys.argv[1]
    main(user_name, "stopword_ja.txt")