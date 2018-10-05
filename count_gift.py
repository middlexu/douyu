# !usr/bin/env python
# -*- coding: utf-8 -*-
# author: middle
# time: 2018/4/16


from pymongo import MongoClient
import pandas as pd
from functools import cmp_to_key
import datetime
# from urllib.parse import quote_plus

MONGO_TABLE = 'f4_gift'
# host = '127.0.0.1'
host = '47.98.221.227'
client = MongoClient(host)

client.douyu.authenticate("douyu", "password", mechanism='MONGODB-CR')
db = client["douyu"]
collection = db[MONGO_TABLE]


# 取某一日期数据，以后更改这个就行
nian = datetime.datetime.now().year
yue = datetime.datetime.now().month
ri = datetime.datetime.now().day

riqi = '%s-%s-%s'%(nian, yue, ri)
time_start = datetime.datetime(nian, yue, ri, 0, 0)
time_end = time_start + datetime.timedelta(days=1)
# time_end = datetime.datetime(2018, 8, 1, 0, 0)

# data = pd.DataFrame(list(collection.find({'time':{'$regex': riqi}} ,{'_id': 0})))
data = pd.DataFrame(list(collection.find({'time': {'$gte': time_start, '$lte': time_end}}, {'_id': 0})))

# print(data.head(10))
giftname_price = data[['giftname', 'price']]
giftname_price = giftname_price.groupby(by='giftname')['price'].first()
giftname_price = giftname_price.to_dict()
# print(giftname_price)
# {'好人卡': 0.1, '小飞碟': 1.0, '帐篷': 0.2, '火箭': 500.0, '超级火箭': 2000.0, '金锄头': 6.0, '飞机': 100.0}
giftname_jiangxu = []
# cmp(x[1], y[1]) cmp改成这个了 (a > b) - (a < b)
giftname_price = sorted(giftname_price.items(), key=cmp_to_key(lambda x, y: (x[1]>y[1])-(x[1]<y[1])), reverse=True)
for i in giftname_price:
    giftname_jiangxu.append(i[0])
# print(giftname_jiangxu)
# {'超级火箭': 2000.0, '火箭': 500.0, '飞机': 100.0, '金锄头': 6.0, '帐篷': 0.2, '好人卡': 0.1, '小飞碟': 1.0}
# 显示的时候，贵的礼物排在前面


data['real_price'] = data['price'] * data['gfcnt']  # 连击 计算真实花费 = 连击次数 * 一次花费
# print(data)
data_grouped = data.groupby(by=['usrname', 'giftname'])['real_price'].sum()
data_grouped = data_grouped.to_frame()

data_grouped = data_grouped.unstack()
# print(data_grouped)
data_grouped.columns = data_grouped.columns.droplevel()

# data_grouped = data_grouped[['火箭', '飞机', '金锄头', '帐篷', '好人卡']]
data_grouped = data_grouped[giftname_jiangxu]
# print(data_grouped)
data_grouped['总计'] = data_grouped.apply(lambda x: x.sum(), axis=1)
data_grouped = data_grouped.sort_values(by='总计', ascending=False)
data_grouped.loc['总计'] = data_grouped.apply(lambda x: x.sum())
# print(data_grouped)

data_grouped.to_csv(MONGO_TABLE + riqi + '.csv', encoding='utf-8')

client.close()  # 一定要关闭



