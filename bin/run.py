# -*- coding: UTF-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))


import threading
# from threading import local
import time
from conf.settings import ROOM_ID_LIST
from src import douyu, chaxunliwu


def main():
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


if __name__ == '__main__':
    try:
        main()
    except Exception:
        time.sleep(5)
        os.execvp(sys.executable, [sys.executable, ] + sys.argv)  # os.execvp在python下不会重启，命令行没问题
    except KeyboardInterrupt:  # 没啥用，只是主线程退出，子线程还在运行
        print('KeyboardInterrupt')
        sys.exit(1)  # 不起作用，不会退出子线程
