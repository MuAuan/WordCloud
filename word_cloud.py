#$ python3 word_cloud.py -d /usr/lib/aarch64-linux-gnu/mecab/dic/mecab-ipadic-neologd

from MeCab import Tagger
import argparse
import matplotlib.pyplot as plt
from wordcloud import WordCloud

parser = argparse.ArgumentParser(description="convert csv")
parser.add_argument("--dictionary", "-d", type=str, help="mecab dictionary")
args = parser.parse_args()

t = Tagger()
#t = Tagger(" -d " + args.dictionary)
#t = Tagger("-Ochasen" + ("" if not args.dictionary else " -d " + args.dictionary))

text = "名城大（名古屋市）は25日、リチウムイオン電池の開発でノーベル化学賞を受賞した同大学教授で旭化成名誉フェローの吉野彰さん（72）に「特別栄誉教授」の称号を授与した。吉野さんは2017年から、大学院理工学研究科の教授を務めており、週1回の講義を受け持っている。名城大によると、特別栄誉教授はノーベル賞を受賞した教員などをたたえるための称号。14年に終身教授の赤崎勇さんと元教授の天野浩さんが、青色発光ダイオード（LED）の開発でノーベル物理学賞を受賞したことをきっかけに創設した。"

splitted = " ".join([x.split("\t")[0] for x in t.parse(text).splitlines()[:-1]])
print("1",splitted)
wc = WordCloud(font_path="/home/muauan/.fonts/NotoSansCJKjp-Regular.otf")
wc.generate(splitted)
plt.axis("off")
plt.imshow(wc)
plt.pause(1)
plt.savefig('./output_images/yosino0_{}.png'.format(text[0])) 
plt.close()

splitted = " ".join([x.split("\t")[0] for x in t.parse(text).splitlines()[:-1] if x.split("\t")[1].split(",")[0] not in ["助詞", "助動詞", "副詞", "連体詞"]])
print("2",splitted)
wc = WordCloud(font_path="/home/muauan/.fonts/NotoSansCJKjp-Regular.otf")
wc.generate(splitted)
plt.axis("off")
plt.imshow(wc)
plt.pause(1)
plt.savefig('./output_images/yosino1_{}.png'.format(text[0])) 
plt.close()
