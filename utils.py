import glob
import hashlib
import os
import sys

from wordcloud import WordCloud
import matplotlib.pyplot as plt
# get_ipython().run_line_magic('matplotlib', 'inline')
from matplotlib.font_manager import FontProperties
fp = FontProperties(fname=r'C:\WINDOWS\Fonts\meiryo.ttc', size=50)  # 日本語対応


def DrawWordCloud(word_freq_dict, title="unknown", show=True):
    # デフォルト設定を変更して、colormapを"rainbow"に変更
    wordcloud = WordCloud(background_color='white', min_font_size=15, font_path='C:\WINDOWS\Fonts\meiryo.ttc',
                          max_font_size=200, width=1000, height=500, prefer_horizontal=1.0, relative_scaling=0.0, colormap="rainbow")
    wordcloud.generate_from_frequencies(word_freq_dict)
    plt.figure(figsize=[15, 10])
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    os.makedirs("./output/wordcloud", exist_ok=True)
    plt.savefig(f"./output/wordcloud/{title}.png")
    if show is True:
        plt.show()


def color_func(word, font_size, position, orientation, random_state, font_path):
    return "white"


def removeSameImage(path):
    os.makedirs(path, exist_ok=True)
    hash_list = {}

    for f in [path + '\\' + f for f in os.listdir(path)]:
        data = open(f, 'rb').read()
        h = hashlib.sha256(data).hexdigest()
        if h in hash_list:
            if data == open(hash_list[h], 'rb').read():
                print(hash_list[h] + 'and' + f + 'are the same image file.')
                os.remove(f)
        else:
            hash_list[h] = f
