import sys
import os
import threading

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from src import douyu, db, chaxunliwu

roomid = input('请输入房间号：')
gift = chaxunliwu.Gift(roomid)
gift.handle()
# print(gift.data_handled)
savedb = db.SaveDb(roomid, gift.data_handled)
# handledanmu = douyu.HandleDanmu()
dyclient = douyu.DouyuClient(roomid, savedb, gift.data_handled, )
run = threading.Thread(target=dyclient.run)
keeplive = threading.Thread(target=dyclient.keeplive)
run.start()
keeplive.start()


# ConnectionResetError

