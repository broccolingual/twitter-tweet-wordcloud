import os, sys, json
from requests_oauthlib import OAuth1Session
from dotenv import find_dotenv, load_dotenv

env_file = find_dotenv()
load_dotenv(env_file)

CONSUMER_KEY = os.environ.get('CONSUMER_KEY')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET')
ACCESS_KEY = os.environ.get('ACCESS_KEY')
ACCESS_KEY_SECRET = os.environ.get('ACCESS_KEY_SECRET')

twitter = OAuth1Session(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_KEY_SECRET)

def getAccountTwitterData(user_name, repeat=10):

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
            print(mid) # 時系列で見た時に最も古いツイートID

        else: #正常通信出来なかった場合
            print("Failed: %d" % res.status_code)
            break

    print("ツイート取得数：%s" % len(tweets))
    return tweets

from janome.tokenizer import Tokenizer
import collections
import re

# こそあど言葉や敬称等の単語の除外リスト
EXCLUSION_WORDS_LIST = ["さん", "さま", "こと", "これ", "それ", "あれ", "どれ", "たち", "よう", "ため", "みたい", "そう", "こっち", "そっち", "あっち", "どっち", "こちら", "そちら", "あちら", "どちら", "ここ", "そこ", "あそこ", "どこ"]

def CountWord(tweets):
    tweet_list = [tweet["text"] for tweet in tweets]
    all_tweet = "\n".join(tweet_list)

    t = Tokenizer()

    # 原形に変形、名詞のみ、1文字を除去、漢字・平仮名・カタカナの連続飲みに限定
    c = collections.Counter(token.base_form for token in t.tokenize(all_tweet) 
                            if token.part_of_speech.startswith('名詞') and len(token.base_form) > 1 
                            and token.base_form.isalpha() and not re.match('^[a-zA-Z]+$', token.base_form)) 

    freq_dict = {}
    mc = c.most_common()
    for elem in mc:
        if elem[0] not in EXCLUSION_WORDS_LIST:
            freq_dict[elem[0]] = elem[1]

    return freq_dict

# Word Cloudで可視化、WordCloud可視化関数
def color_func(word, font_size, position, orientation, random_state, font_path):
    return 'white'

from wordcloud import WordCloud
import matplotlib.pyplot as plt
# get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib.font_manager import FontProperties
fp = FontProperties(fname=r'C:\WINDOWS\Fonts\meiryo.ttc', size=50) #日本語対応

def DrawWordCloud(word_freq_dict, user_name="unknown"):

    # デフォルト設定を変更して、colormapを"rainbow"に変更
    wordcloud = WordCloud(background_color='white', min_font_size=15, font_path='C:\WINDOWS\Fonts\meiryo.ttc',
                          max_font_size=200, width=1000, height=500, prefer_horizontal=1.0, relative_scaling=0.0, colormap="rainbow")    
    wordcloud.generate_from_frequencies(word_freq_dict)
    plt.figure(figsize=[20,20])
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig(f"./output/{user_name}.png")
    plt.show()

if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit(1)
    user_name = sys.argv[1]
    tweets = getAccountTwitterData(user_name, repeat=10)
    freq_dict = CountWord(tweets)
    DrawWordCloud(freq_dict, user_name=user_name)