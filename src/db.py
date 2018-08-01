from conf.settings import *
import pymongo
# import json


# gift = json.load(open(os.path.join(BASE_DIR, 'conf', 'gift.json'), 'r', encoding='utf-8'))


class SaveDb():
    def __init__(self, roomid, gift):
        self.client = pymongo.MongoClient(MONGO_URI)
        self.client.douyu.authenticate(DB_USER, DB_PWD, mechanism='SCRAM-SHA-1')
        self.db = self.client[MONGO_DB]
        self.danmu_table = roomid
        self.gift_table = roomid + 'gift'
        self.gift = gift

    def save(self, result, table):
        if table == self.danmu_table:
            usrname_txt = {
                'uid': result[0],
                'usrname': result[1],
                'txt': result[2],
                'time': result[-1]
            }
            self.save_to_mongodb(self.danmu_table, **usrname_txt)
        else:
            usrname_gift = {
                'uid': result[2],
                'usrname': result[3],
                'giftid': result[1],
                'giftname': self.gift[result[1]][0],
                'price': self.gift[result[1]][1],
                'time': result[-1]
            }
            self.save_to_mongodb(self.gift_table, **usrname_gift)

    def save_to_mongodb(self, table, **result):
        try:
            self.db[table].insert(result)
            # print("存储到MONGODB成功", result)
        except Exception as e:
            # print("存储到MONGODB失败", result)
            pass