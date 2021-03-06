# -*- coding: UTF-8 -*-
import socket
import os

MONGO_URI = "localhost"
MONGO_DB = "douyu"

DB_USER = "douyu"
DB_PWD = "password"


HOST = socket.gethostbyname('openbarrage.douyutv.com')


PORT = 8601
BUFSIZ = 1024

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



from collections import namedtuple

# F4, 339, 9438, 正直博, 401
Room = namedtuple('Room', 'roomid nickname')
ROOM_ID_LIST = [
                # Room('318624', 'f4'), 
                # Room('485503', '339'), 
                # Room('430489', '9438'), 
                # Room('533813', '正直博'), 
                # Room('229346', '401'),
                # Room('288016', '英雄联盟官方赛事'),
                # Room('25233', '小深深儿'),
                Room('4632993', '小深深儿'),
                ]



Noble = namedtuple('Noble', ['name', 'price'])  # 这个price表示可以收到多少钱
# Noble = namedtuple('Noble', 'name price')  # 这么写也是可以的

NOBLE_DICT = {
    '1': Noble('骑士', 200),
    '2': Noble('子爵', 500),
    '3': Noble('伯爵', 2000),
    '4': Noble('公爵', 5000),
    '5': Noble('国王', 10000),
    '6': Noble('皇帝', 20000),
    '7': Noble('游侠', 26),
}
