from janome.tokenizer import Tokenizer
import collections
import re


def CountWord(tweets: list, keyword: str = None, stopword_list: set = None, jp_only: bool = True) -> dict:
    tweet_list = [tweet["text"] for tweet in tweets]
    all_tweet = "\n".join(tweet_list)

    t = Tokenizer()

    if jp_only:  # 原形に変形、名詞のみ、1文字を除去、漢字・平仮名・カタカナの連続飲みに限定
        c = collections.Counter(token.base_form for token in t.tokenize(all_tweet)
                                if token.part_of_speech.startswith('名詞') and len(token.base_form) > 1
                                and token.base_form.isalpha() and not re.match('^[a-zA-Z]+$', token.base_form))
    else:
        c = collections.Counter(token.base_form for token in t.tokenize(all_tweet)
                                if token.part_of_speech.startswith('名詞') and len(token.base_form) > 1
                                and token.base_form.isalpha())

    if keyword:  # キーワードに含まれる言葉を除外
        ck = [token.base_form for token in t.tokenize(keyword) if len(
            token.base_form) > 1 and token.base_form.isalpha()]

    freq_dict = {}
    mc = c.most_common()
    if stopword_list:
        if keyword:
            for w in ck:
                stopword_list.add(w)

        for elem in mc:
            if elem[0] not in stopword_list:
                freq_dict[elem[0].lower()] = elem[1]
    else:
        for elem in mc:
            freq_dict[elem[0].lower()] = elem[1]

    return freq_dict


def CalcTF(freq_dict) -> dict:
    tf_dict = {}
    sum_of_words = 0
    for v in freq_dict.values():
        sum_of_words += v

    for k, v in freq_dict.items():
        tf_dict[k] = round(v/sum_of_words, 6)

    return tf_dict


def PrintWordsTF(tf_dict, target=30):
    print("\n{0:3}. {1:6} - {2}".format("rank", "TF", "word"))

    rank = 0
    for k, v in tf_dict.items():
        if rank >= target:
            break
        rank += 1
        print("{0:3}. {1:6} - {2}".format(rank, v, k))
