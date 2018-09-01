import sys
import os
import threading
from threading import local
import time
from conf.settings import ROOM_ID_LIST
from src import douyu, db, chaxunliwu

sys.path.append(os.path.dirname(os.path.dirname(__file__)))


# args = sys.argv[:]
# args.insert(0, sys.executable)
# roomid = args[2]

threads = []
for roomid in ROOM_ID_LIST:
    gift = chaxunliwu.Gift(roomid)
    gift.handle()
    # print(gift.data_handled)
    savedb = db.SaveDb(roomid, gift.data_handled)
    # handledanmu = douyu.HandleDanmu()
    dyclient = douyu.DouyuClient(roomid, savedb, gift.data_handled, )
    run = threading.Thread(target=dyclient.run)
    keeplive = threading.Thread(target=dyclient.keeplive)
    # 好像没有线程同步的问题
    # 因为没有用到全局变量，传进去的dyclient不一样
    threads.append(run)
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


