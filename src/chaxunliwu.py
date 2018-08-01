# -*- encoding: utf-8 -*-
# 房间礼物名称查询

import json
import requests


# result = requests.get('http://open.douyucdn.cn/api/RoomApi/room/318624')
#
# result = json.loads(result.content)
# print(result['data']['gift'])
# for i in result['data']['gift']:
#     print(i)


class Gift():
    def __init__(self, roomid):
        self.roomid = roomid
        self.data = json.loads(requests.get('http://open.douyucdn.cn/api/RoomApi/room/'+self.roomid).content)['data']['gift']

    def handle(self):
        self.data_handled = {}
        # 处理完后是下面的数据
        # {
        #     "1005": ["超级火箭", 2000],
        #     "196": ["火箭", 500],
        #     "195": ["飞机", 100],
        #     "750": ["办卡", 6],
        # }
        for liwu in self.data:
            if '鱼丸' not in liwu['name'] and '超大丸星' not in liwu['name']:
                self.data_handled[liwu['id']] = [
                    liwu['name'],
                    liwu['pc']
                ]


# gift = Gift('318624')
# gift.handle()
# print(gift.data_handled)