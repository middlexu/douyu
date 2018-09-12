# -*- encoding: utf-8 -*-


import jieba, jieba.analyse
import json
from PIL import Image
import numpy as np
from wordcloud import WordCloud, STOPWORDS
# import matplotlib.pyplot as plt


# Read the whole text.
# text = open(path.join(d, 'danmu.txt'), encoding='utf-8').read()
stopwords = json.load(open('stopwords_zh.json', 'r', encoding='utf-8'))
# print(stopwords)
stopwords.append(' ')
stopwords.append('nba5574')
stopwords.append('nba5744')
stopwords.append('emot')
stopwords.append('dy111')
stopwords.append('dy115')
stopwords.append('dy101')
stopwords.append('dy102')
stopwords.append('dy110')
stopwords.append('10')
stopwords.append('胖子')
stopwords.append('一下')
stopwords.append('kk')



def seg_sentence(sentence):
    sentence_segd = jieba.cut(sentence)
    outstr = ''
    for word in sentence_segd:
        if word not in stopwords:
            outstr = outstr + word + ' '
    return outstr

cut_text = ''
with open('danmu.txt', 'r', encoding='utf-8') as f:
    while True:
        line = f.readline()
        if not line:
            break
        cut_text += seg_sentence(line)


cut_an= jieba.analyse.extract_tags(cut_text,150)  # 关键词提取,返回权重最高的前30，数字可以不填默认20
for i in cut_an:
    print(i)


# Generate a word cloud image
# 画简单的图
# wc = WordCloud(background_color = 'white',
#                       stopwords = STOPWORDS,
#                       font_path='C:/Users/Windows/fonts/msyh.ttf',)
# wc.generate(cut_text)
#
# # Display the generated image:
# # the matplotlib way:
# import matplotlib.pyplot as plt
# plt.figure()
# plt.imshow(wc, interpolation='bilinear')
# plt.axis("off")
# plt.show()




# read the mask image
bjun_mask = np.array(Image.open("空军.png"))

wc = WordCloud(background_color="white",
               max_words=2000,
               mask=bjun_mask,
               stopwords=stopwords,
               font_path='./msyh.ttf')

# generate word cloud
wc.generate(cut_text)

# store to file
wc.to_file("空军2.png")


# show
# plt.imshow(wc, interpolation='bilinear')
# plt.axis("off")
# plt.figure()
# plt.imshow(alice_mask, cmap=plt.cm.gray, interpolation='bilinear')
# plt.axis("off")
# plt.show()