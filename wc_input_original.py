#$ python3 word_cloud.py -d /usr/lib/aarch64-linux-gnu/mecab/dic/mecab-ipadic-neologd -s stop_words.txt
#https://github.com/amueller/word_cloud/blob/master/wordcloud/wordcloud.py

from MeCab import Tagger
import argparse
import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

parser = argparse.ArgumentParser(description="convert csv")
#parser.add_argument("input", "-i", type=str, help="csv file")
parser.add_argument("--dictionary", "-d", type=str, help="mecab dictionary")
parser.add_argument("--stop_words", "-s", type=str, help="stop words list")
args = parser.parse_args()

#t = Tagger("-Ochasen" + " -d " + args.dictionary)
t = Tagger( " -d " + args.dictionary)
#t = Tagger("-Owakati" + ("" if not args.dictionary else " -d " + args.dictionary))
#text = "　名城大（名古屋市）は25日、リチウムイオン電池の開発でノーベル化学賞を受賞した同大学教授で旭化成名誉フェローの吉野彰さん（72）に「特別栄誉教授」の称号を授与した。吉野さんは2017年から、大学院理工学研究科の教授を務めており、週1回の講義を受け持っている。名城大によると、特別栄誉教授はノーベル賞を受賞した教員などをたたえるための称号。14年に終身教授の赤崎勇さんと元教授の天野浩さんが、青色発光ダイオード（LED）の開発でノーベル物理学賞を受賞したことをきっかけに創設した。"
#text = "　会見の冒頭、本庶氏は「大変名誉なこと。このような賞をいただき、幸運な人間だと思っている」と心境を語った。学賞候補の一人として取り上げられている。待ちに待った受賞かと記者から問われると、「賞というものはそれぞれの（賞の）団体が独自の基準で決めること。長いとか待ったとか、僕自身は感じていない」。それよりも、趣味のゴルフで顔を合わせる男性から「あなたの薬のおかげで、肺がんが良くなってまたゴルフができる」と感謝されたエピソードを紹介し、「これ以上の幸せはない。何の賞をもらうことよりも、何よりも嬉しい」と述べ、自身の基礎的な研究が臨床を経て実際のがん患者のためになったことを喜んだ。免疫の仕組みを解明した本庶氏の研究は、新しいがんの治療法の開発につながった。本庶氏は1992年に「PD-1」という分子を発見。この分子が免疫反応のブレーキとして大きな役割を果たしていることを明らかにした。がんに対して、このブレーキの機能を抑えることで、がんの増殖や転移を抑えられるという画期的ながん治療の理論を示した。このがん免疫治療法は実際に世界のがん患者に適応されている。本庶氏は「免疫療法がこれまで以上に多くのがん患者を救うことになるように、もうしばらく研究を続けたい」と語った。　がん免疫治療法については、効かないがんもあり、なぜ効かないのかという研究が必要で「まだまだ発展途上」だと指摘。ただ、感染症に対するペニシリンの例を挙げ、「感染症が大きな脅威でなくなった日が（来たように）、遅くとも今世紀中には（がんにもそういう日が）訪れると思っている」と見据えた。"
#text = "免疫の仕組みを解明した本庶氏の研究は、新しいがんの治療法の開発につながった。本庶氏は1992年に「PD-1」という分子を発見。この分子が免疫反応のブレーキとして大きな役割を果たしていることを明らかにした。がんに対して、このブレーキの機能を抑えることで、がんの増殖や転移を抑えられるという画期的ながん治療の理論を示した。このがん免疫治療法は実際に世界のがん患者に適応されている。"
#text = "本庶氏は1992年に「PD-1」という分子を発見。この分子が免疫反応のブレーキとして大きな役割を果たしていることを明らかにした。"


import matplotlib.pyplot as plt

fpath="/home/muauan/.fonts/NotoSansCJKjp-Regular.otf"
#wc = WordCloud(font_path=fpath, regexp="[\w']+")

def get_wordcrowd_color_mask(sk, text, imgpath ):
    plt.figure(figsize=(6,6), dpi=200)
    if imgpath != "":
        img_color = np.array(Image.open( imgpath ))
        image_colors = ImageColorGenerator(img_color)
        wc = WordCloud(width=400,
                   height=300,
                   font_path=fpath,
                   mask=img_color,
                   collocations=False, # 単語の重複しないように
                  ).generate( text )
        plt.imshow(wc.recolor(color_func=image_colors), # 元画像の色を使う
               interpolation="bilinear")
    else:
        #wc = WordCloud(font_path=fpath, regexp="[\w']+").generate( text )
        wc = WordCloud(font_path=fpath, width=400, height=200, margin=2,
                 ranks_only=None, prefer_horizontal=.9, mask=None, scale=1,
                 color_func=None, max_words=200, min_font_size=4,
                 stopwords=None, random_state=None, background_color='black',
                 max_font_size=None, font_step=1, mode="RGB",
                 relative_scaling='auto', regexp=r"\w[\w']+" , collocations=True,
                 colormap=None, normalize_plurals=True, contour_width=0,
                 contour_color='black', repeat=False,
                 include_numbers=False, min_word_length=0).generate(text)
        plt.imshow(wc)

    # show

    plt.axis("off")
    plt.pause(1)
    plt.savefig('./output_images/{}-yosino_{}.png'.format(sk,text[0])) 
    plt.close()

    
# ストップワード読込関数
stop_words = []
if args.stop_words:
    for line in open(args.stop_words, "r", encoding="utf-8"):
        stop_words.append(line.strip())
    print(stop_words)

# リストを文字列に変換する関数
def join_list_str(list):
    return ' '.join(list)

# ストップワード除外関数
def exclude_stopword(text):
    changed_text = [token for token in text.lower().split(" ") if token != "" if token not in stop_words]
    # 上記のままだとリスト形式になってしまうため、空白区切の文字列に変換
    changed_text = join_list_str(changed_text)
    return changed_text        
        
while True:
    line = input("> ")
    if not line:
        break
        
    splitted = " ".join([x.split("\t")[0] for x in t.parse(line).splitlines()[:-1] if x.split("\t")[1].split(",")[0] not in [""]])
    print("0",splitted)
    get_wordcrowd_color_mask(0,splitted, '')
    get_wordcrowd_color_mask(1,splitted, './mask_images/alice_color.png') 
    
    splitted = " ".join([x.split("\t")[0] for x in t.parse(line).splitlines()[:-1] if x.split("\t")[1].split(",")[0] not in ["助詞", "助動詞", "副詞", "連体詞","接続詞","動詞","記号"]])
    print("1",splitted)
    get_wordcrowd_color_mask(2,splitted, '')
    get_wordcrowd_color_mask(3,splitted, './mask_images/alice_color.png') 

    splitted = exclude_stopword(splitted)
    print("2",splitted)
    get_wordcrowd_color_mask(4,splitted, '')
    get_wordcrowd_color_mask(5,splitted, './mask_images/alice_color.png')  #Keyakizaka46_logo_2.png alice_color.png alice_mask.png fulflat.jpeg
    