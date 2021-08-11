from janome.tokenizer import Tokenizer
import collections
import re

def CountWord(tweets, stopword_list=None):
    tweet_list = [tweet["text"] for tweet in tweets]
    all_tweet = "\n".join(tweet_list)

    t = Tokenizer()

    # 原形に変形、名詞のみ、1文字を除去、漢字・平仮名・カタカナの連続飲みに限定
    c = collections.Counter(token.base_form for token in t.tokenize(all_tweet) 
                            if token.part_of_speech.startswith('名詞') and len(token.base_form) > 1 
                            and token.base_form.isalpha() and not re.match('^[a-zA-Z]+$', token.base_form)) 

    freq_dict = {}
    mc = c.most_common()
    if stopword_list:
        for elem in mc:
            if elem[0] not in stopword_list:
                freq_dict[elem[0]] = elem[1]
    else:
        for elem in mc:
            freq_dict[elem[0]] = elem[1]

    return freq_dict