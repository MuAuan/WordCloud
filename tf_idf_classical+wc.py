#$ python3 tf_idf_classical.py -d /usr/lib/aarch64-linux-gnu/mecab/dic/mecab-ipadic-neologd conversation_anzen.csv -s stop_words.txt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import MeCab
from MeCab import Tagger
from wordcloud import WordCloud
import matplotlib.pyplot as plt

import argparse

parser = argparse.ArgumentParser(description="convert csv")
parser.add_argument("input", type=str, help="csv file")
parser.add_argument("--dictionary", "-d", type=str, help="mecab dictionary")
parser.add_argument("--stop_words", "-s", type=str, help="stop words list")
args = parser.parse_args()

mecab = MeCab.Tagger("-Owakati" + ("" if not args.dictionary else " -d " + args.dictionary))
t = Tagger(" -d " + args.dictionary)

questions = []
questions_ = []

def train_conv(mecab,input_file,encoding):
    questions = []
    questions_ = []
    with open(input_file, encoding=encoding) as f:
        cols = f.read().strip().split('\n')
        for i in range(len(cols)):
            questions.append(mecab.parse(cols[i]).strip())
            questions_.append(cols[i])
    return questions, questions_

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

questions,questions_ = train_conv(mecab,args.input,encoding="cp932") #"shift-jis") #utf-8") #"cp932")        
vectorizer = TfidfVectorizer(token_pattern="(?u)\\b\\w+\\b", stop_words=stop_words)
vecs = vectorizer.fit_transform(questions)

#for k,v in vectorizer.vocabulary_.items():
#    print(k, v)
wc = WordCloud(font_path="/home/muauan/.fonts/NotoSansCJKjp-Regular.otf")
while True:
    line = input("> ")
    if not line:
        break

    #print(mecab.parse(line))
        
    #index = np.argmax(cosine_similarity(vectorizer.transform([mecab.parse(line)]), vecs))
    #print(questions[index])
    
    print()
    
    sims = cosine_similarity(vectorizer.transform([mecab.parse(line)]), vecs)    
    index = np.argsort(sims[0])
    sk=0
    for j in range(-1,-100,-1):
        if sims[0][index[j]]>=0.3:
            print("|{}|（{:.2f}）|{}|".format(sk,sims[0][index[j]],questions_[index[j]])) #questions_[index[j]]))
            text = questions[index[j]]
            splitted = " ".join([x.split("\t")[0] for x in t.parse(text).splitlines()[:-1] if x.split("\t")[1].split(",")[0] not in ["助詞", "助動詞", "副詞", "連体詞", "動詞"]])
            splitted = exclude_stopword(splitted)
            wc.generate(splitted)
            plt.axis("off")
            plt.title("{}_({:.2f})".format(sk,sims[0][index[j]]))
            plt.tight_layout()
            plt.imshow(wc)
            plt.pause(0.05)
            plt.savefig('./output_q/question{}_{}.png'.format(sk,text[0])) 
            plt.close()
            #print()
            sk += 1
