import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


import threading
# from threading import local
# import time
from conf.settings import ROOM_ID_LIST
from src import douyu, chaxunliwu


# args = sys.argv[:]
# args.insert(0, sys.executable)
# roomid = args[2]

threads = []
for room in ROOM_ID_LIST:
    gift = chaxunliwu.Gift(room.roomid)
    gift.handle()
    dyclient = douyu.DouyuClient(room, gift.data_handled)
    run = threading.Thread(target=dyclient.run, name=room.roomid)
    
    # 好像没有线程同步的问题
    # 因为没有用到全局变量，传进去的dyclient不一样
    threads.append(run)

    keeplive = threading.Thread(target=dyclient.keeplive)
    threads.append(keeplive)


for i in threads:
    i.start()

# ConnectionResetError
# BrokenPipeError

for i in threads:
    i.join()
# print('---------------------------')
# if not keeplive.is_alive():
#     executable = sys.executable  # python（安装）路径
#     time.sleep(5)
#     os.execvp(executable, args)


