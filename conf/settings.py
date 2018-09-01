import socket
import os

MONGO_URI = "localhost"
MONGO_DB = "douyu"

DB_USER = "douyu"
DB_PWD = "password"

HOST = socket.gethostbyname('openbarrage.douyutv.com')
print(HOST)
HOST = "124.95.155.50"
PORT = 8601
BUFSIZ = 1024

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# F4, 339, 9438, 正直博
# ROOM_ID_LIST = ['318624', '485503', '430489', '533813', ]
ROOM_ID_LIST = ['229346', ]

from collections import namedtuple

Noble = namedtuple('Noble', ['name', 'price'])  # 这个price表示可以收到多少钱

NOBLE_DICT = {
    '1': Noble('骑士', 200),
    '2': Noble('子爵', 500),
    '3': Noble('伯爵', 2000),
    '4': Noble('公爵', 5000),
    '5': Noble('国王', 10000),
    '6': Noble('皇帝', 20000),
    '7': Noble('游侠', 26),
}
