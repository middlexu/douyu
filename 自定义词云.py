# !usr/bin/env python
# -*- encoding: utf-8 -*-
# author: middle
# time: 2018/4/21


from wordcloud import WordCloud
from PIL import Image
import numpy as np



# Read the whole text.
#  此处原为处理英文文本，我们修改为传入中文数组
#text = open(path.join(d, 'constitution.txt')).read()
frequencies = {u'F4':50, u'三炮':35, u'贾斯丁·逼俊':35, u'狗子哥':35,
               u'突突突':20, u'出大事了':16, u'过气主播':16, u'哈哈哈':12,
               u'黑幕':15, u'办卡':13, u'过分':10, u'基佬':17,
               u'出货':9, u'忍忍':10, u'取关':10, u'操盘':11,
               u'非洲牛蛙':10, u'跳水':10, u'暗示':5, u'裤裆藏蛇':20,
               u'蜂衣':10, u'口嗨':21, u'坦克':14, u'日常洗网':22,
               u'妹崽错别吗':5, u'推车':8, u'寂寞房间':13, u'乡村土嗨':25,
               u'大兄弟':7, u'头子':7, u'帆姐':7, u'公子':7, u'永不出货':19,
               u'锦衣卫':9, u'看货':6, u'血亏':8, u'天台':8,
               u'牛肉干':9, u'打桩机':7, u'种猪':7, u'了解一下':9,
               u'他不要了':14, u'挖蛇狂魔':19, u'内壁光滑':16, u'秀':5,
               u'多多':10, u'打野':10, u'干塘':10, u'液体黄金':10,
               u'金锄头':9, u'滴滴滴':11, u'漂移':6, u'弹射起步':6,
               u'铁路镇':7, u'冯旗村':7, u'钢鞭村':7, u'村霸':15,
               u'666':9, u'家暴节目':8, u'开车TV':7, u'吃饭TV':7,
               u'辣椒':14, u'收汁':10, u'加水':9, u'小龙虾':12,
               u'十二道炮味':16, u'套鞋走天下':8, u'军中绿发':9, u'竹鼠':10,
               u'火箭动作':9, u'五菱宏光':7, u'斑马':6, u'捉迷藏':8,
               u'野营':14, u'挨饿':10, u'上山求雨':11, u'下夹子':9,
               u'弹弓':8, u'灵堂布':12, u'竹筒饭':8, u'打爆眼睛':19,
               u'野区霸主':19, u'黑粉家族':9, u'尼古拉斯家族':9, u'西索家族':8,
               u'安静家族':8, u'鲱鱼罐头':18, u'芥末':12, u'醋':10,
               u'开盘':14, u'炒粉':9, u'落地成盒':7, u'色情主播':11,
               u'背锅':6, u'摔跤':7, u'颜值一哥':12, u'结账':6, u'演员':5,
               u'混吃等死':9, u'孤岛求生':11, u'暴富':9, u'GG':6,
               u'卡':6, u'喂鱼':7, u'扶贫':8, u'痒':6, u'尬舞':6,
               u'你们来':9, u'李十针':8, u'能行吗':15, u'一天天的':14,
               u'我想摸你的头发啊':3, u'蒋八碗':5, u'蒋得对':5, u'廖不接':6,
               u'小跳蛙':8, u'啦啦啦啦啦':4, u'道歉':9, u'见面恰根烟':6,
               u'MMP':5, u'凉凉':6, u'大大大':10, u'又是这个逼':3,
               u'文盲':14, u'嘤嘤嘤':8, u'三元一只十元三只':3, u'挖竹笋':5,
               u'板上钉钉':13, u'西装打野':8, u'开门':5, u'追梦':6,
               u'黑白皮带':5, u'下网':6, u'下地龙':6, u'渣渣':4, u'人均皇帝':4,


               }

# Generate a word cloud image 此处原为 text 方法，我们改用 frequencies
#wordcloud = WordCloud().generate(text)
# wordcloud = WordCloud().fit_words(frequencies)

bjun_mask = np.array(Image.open("空军.png"))
# take relative word frequencies into account, lower max_font_size
#wordcloud = WordCloud(max_font_size=40, relative_scaling=.5).generate(text)
wordcloud = WordCloud(background_color="white", max_words=160, max_font_size=100, relative_scaling=.5, mask=bjun_mask, font_path='./msyh.ttf').fit_words(frequencies)
wordcloud.to_file("空军3.png")

