import collections
import re

import numpy as np
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.tokenfilter import POSStopFilter


def CountWord(tweets: list, keyword: str = None, stopword_list: set = None) -> dict:
    tweet_list = [tweet["text"] for tweet in tweets]
    all_tweet = "\n".join(tweet_list)

    token_filters = [POSStopFilter(['接続詞', '記号', '助詞', '助動詞'])]
    t = Analyzer(tokenizer=Tokenizer(), token_filters=token_filters)

    c = collections.Counter(token.base_form for token in t.analyze(all_tweet)
                            if token.part_of_speech.startswith('名詞') and len(token.base_form) > 1 and token.base_form.isalpha())

    if keyword:  # キーワードに含まれる言葉を除外
        ck = [token.base_form for token in t.analyze(
            keyword) if token.part_of_speech.startswith('名詞') and len(token.base_form) > 1 and token.base_form.isalpha()]

    freq_dict = {}
    mc = c.most_common()
    if stopword_list:
        if keyword:
            for w in ck:
                stopword_list.add(w)

        for elem in mc:
            if elem[0].lower() not in stopword_list:
                freq_dict[elem[0].lower()] = elem[1]
    else:
        for elem in mc:
            freq_dict[elem[0].lower()] = elem[1]

    tf_dict = CalcTF(freq_dict)
    # IDF計算
    split_tweet_list = []
    for tweet in tweet_list:
        l = [token.base_form for token in t.analyze(tweet)
             if token.part_of_speech.startswith('名詞') and len(token.base_form) > 1 and token.base_form.isalpha()]
        split_tweet_list.append(l)
    idf_list = CalcIDF(split_tweet_list)
    tf_idf_list = CalcTFIDF(tf_dict, idf_list)
    PrintWordsTF(tf_dict)
    PrintWordsIDF(idf_list)
    PrintWordsTFIDF(tf_idf_list)

    return freq_dict


def CalcTF(freq_dict) -> dict:
    tf_dict = {}
    sum_of_words = 0
    for v in freq_dict.values():
        sum_of_words += v

    for k, v in freq_dict.items():
        tf_dict[k] = round(v/sum_of_words, 6)

    return tf_dict


def getIDF(word, document):
    n_samples = len(document)
    df = np.sum(np.array([int(word in d) for d in document], dtype="float32"))
    df += 1
    return np.log2(n_samples / df)


def CalcIDF(in_corpus):
    word_idf_dict = {}
    for w in list(set([w for s in in_corpus for w in s])):
        word_idf_dict[w.lower()] = getIDF(w, in_corpus)
    idf_list = sorted(word_idf_dict.items(), key=lambda x: x[1])
    return idf_list


def CalcTFIDF(tf_dict, idf_list):
    tf_idf_dict = {}
    for item in idf_list:
        try:
            idf_val = item[1]
            tf_val = tf_dict[item[0]]
            tf_idf_dict[item[0]] = tf_val * idf_val
        except KeyError:
            pass
    tf_idf_list = sorted(tf_idf_dict.items(), key=lambda x: x[1], reverse=True)
    return tf_idf_list


def PrintWordsTF(tf_dict, target=10):
    print("\n{0:3}. {1:10} - {2}".format("rank", "TF (頻度)", "word"))

    rank = 0
    for k, v in tf_dict.items():
        if rank >= target:
            break
        rank += 1
        print("{0:3}. {1:10} - {2}".format(rank, v, k))


def PrintWordsIDF(idf_list: list, target=10):
    print("\n{0:3}. {1:10} - {2}".format("rank", "IDF(レア度)", "word"))

    rank = 0
    for item in idf_list:
        if rank >= target:
            break
        rank += 1
        print("{0:3}. {1:10} - {2}".format(rank, round(item[1], 6), item[0]))


def PrintWordsTFIDF(tf_idf_list: list, target=30):
    print("\n{0:3}. {1:10} - {2}".format("rank", "TF-IDF", "word"))

    rank = 0
    for item in tf_idf_list:
        if rank >= target:
            break
        rank += 1
        print("{0:3}. {1:10} - {2}".format(rank, round(item[1], 6), item[0]))
