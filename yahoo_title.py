#$ python3 yahoo_title.py -d /usr/lib/aarch64-linux-gnu/mecab/dic/mecab-ipadic-neologd conversation_anzen.csv -s stop_words.txt

import requests
from bs4 import BeautifulSoup
import urllib3
import re
import argparse
from MeCab import Tagger
from wordcloud import WordCloud
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="convert csv")
parser.add_argument("input", type=str, help="csv file")
parser.add_argument("--dictionary", "-d", type=str, help="mecab dictionary")
parser.add_argument("--stop_words", "-s", type=str, help="stop words list")
args = parser.parse_args()

t = Tagger(" -d " + args.dictionary)

#url = "https://news.yahoo.co.jp"
url = "https://www.nikkei.com/article/DGXMZO56522090X00C20A3000000/"

stop_words = []
if args.stop_words:
    for line in open(args.stop_words, "r", encoding="utf-8"):
        stop_words.append(line.strip())

# リストを文字列に変換する関数
def join_list_str(list):
    return ' '.join(list)

# ストップワード除外関数
def exclude_stopword(text):
    changed_text = [token for token in text.lower().split(" ") if token != "" if token not in stop_words]
    # 上記のままだとリスト形式になってしまうため、空白区切の文字列に変換
    changed_text = join_list_str(changed_text)
    return changed_text

# urllib3を使うならこっち
http = urllib3.PoolManager()
r = http.request('GET', url)

yahoo = BeautifulSoup(r.data, 'html.parser')
#print(yahoo)
#print(yahoo.select("p"))
wc = WordCloud(font_path="/home/muauan/.fonts/NotoSansCJKjp-Regular.otf")
sk=0
for title in yahoo.select("p"):
    title = title.getText()
    title = re.sub(r"[^一-龥ぁ-んァ-ン0-9]", "", title)
    #title = title.replace(r"[^一-龥ぁ-んァ-ン0-9]",'')
    if len(title)>50:
        print("content{};{}".format(sk,title))
        splitted = " ".join([x.split("\t")[0] for x in t.parse(title).splitlines()[:-1] if x.split("\t")[1].split(",")[0] not in ["助詞", "助動詞", "副詞", "連体詞", "動詞"]])
        splitted = exclude_stopword(splitted)
        wc.generate(splitted)
        plt.axis("off")
        plt.title("content_{};".format(sk))
        plt.tight_layout()
        plt.imshow(wc)
        plt.pause(0.05)
        plt.savefig('./output_yahoo/yahoo{}_{}.png'.format(sk,title[0:10])) 
        plt.close()
        sk += 1