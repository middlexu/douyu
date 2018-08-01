import socket
import os

MONGO_URI = "localhost"
MONGO_DB = "douyu"

DB_USER = "douyu"
DB_PWD = "XXXXXXX"


HOST = socket.gethostbyname('openbarrage.douyutv.com')
print(HOST)
HOST = "124.95.155.50"
PORT = 8601
BUFSIZ = 1024

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))