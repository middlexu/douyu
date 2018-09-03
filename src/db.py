from conf.settings import *
import pymongo
# import json


# gift = json.load(open(os.path.join(BASE_DIR, 'conf', 'gift.json'), 'r', encoding='utf-8'))


class SaveDb():
    def __init__(self, room_nickname):
        self.client = pymongo.MongoClient(MONGO_URI)
        self.client.douyu.authenticate(DB_USER, DB_PWD, mechanism='SCRAM-SHA-1')
        self.db = self.client[MONGO_DB]
        self.danmu_table = room_nickname + '_danmu'
        self.gift_table = room_nickname + '_gift'
        self.noble_table = room_nickname + '_noble'

    def save_to_mongodb(self, table, **result):
        try:
            self.db[table].insert(result)
            # print("存储到MONGODB成功", result)
        except Exception as e:
            print("存储到MONGODB失败", result)
            pass
