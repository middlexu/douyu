# !usr/bin/env python
# -*- encoding: utf-8 -*-
# author: middle
# time: 2018/4/16

# -*- encoding: utf-8 -*-

from pymongo import MongoClient
import pandas as pd
from functools import cmp_to_key
import datetime
# from urllib.parse import quote_plus

MONGO_TABLE = '318624gift'

host = '47.104.21.73'
client = MongoClient(host)
client.douyu.authenticate("douyu", "Xu731583158", mechanism='SCRAM-SHA-1')
db = client["douyu"]
collection = db[MONGO_TABLE]


# 取某一日期数据，以后更改这个就行
nian = 2018
yue = 8
ri = 1

riqi = '%s-%s-%s'%(nian, yue, ri)
time_start = datetime.datetime(nian, yue, ri, 0, 0)
time_end = time_start + datetime.timedelta(days=30)
# time_end = datetime.datetime(2018, 8, 1, 0, 0)

# data = pd.DataFrame(list(collection.find({'time':{'$regex': riqi}} ,{'_id': 0})))
data = pd.DataFrame(list(collection.find({'time':{'$gte':time_start, '$lte':time_end}},{'_id': 0})))

# print(data.head(10))
giftname_price = data[['giftname', 'price']]
giftname_price = giftname_price.groupby(by='giftname')['price'].mean()
giftname_price = giftname_price.to_dict()

giftname_jiangxu = []
# cmp(x[1], y[1]) cmp改成这个了 (a > b) - (a < b)
giftname_price = sorted(giftname_price.items(), key=cmp_to_key(lambda x, y: (x[1]>y[1])-(x[1]<y[1])), reverse=True)
for i in giftname_price:
    giftname_jiangxu.append(i[0])

data_grouped = data.groupby(by=['usrname', 'giftname'])['price'].sum()
data_grouped = data_grouped.to_frame()

data_grouped = data_grouped.unstack()
print(data_grouped)
data_grouped.columns = data_grouped.columns.droplevel()

# data_grouped = data_grouped[['火箭', '飞机', '金锄头', '帐篷', '好人卡']]  # 有的没有火箭
data_grouped = data_grouped[giftname_jiangxu]
data_grouped['总计'] = data_grouped.apply(lambda x: x.sum(), axis=1)
data_grouped = data_grouped.sort_values(by='总计', ascending=False)
data_grouped.loc['总计'] = data_grouped.apply(lambda x: x.sum())
print(data_grouped)

data_grouped.to_csv(MONGO_TABLE + riqi + '.csv', encoding='gbk')
