# -*- encoding: utf-8 -*-


import socket
import time
import datetime
# import re
# import json
from conf.settings import *
# import threading
# import db


class DouyuClient():
    # usr_txt = re.compile(b'type@=chatmsg.*/uid@=(.*?)/nn@=(.*?)/txt@=(.*?)/cid@=.*?/\x00')
    # usr_gift = re.compile(b'type@=dgb/rid@=(.*?)/.*?gfid@=(.*?)/.*?/uid@=(.*?)/.*?nn@=(.*?)/ic@=.*?/\x00')
    # usr_chouqin = re.compile(b'type@=bc_buy_deserve.*?/lev@=(\d)/.*?/sui@=id@A=(.*?)@Sname@A=@Snick@A=(.*?)@Sicon@A.*?/\x00')

    # gift = json.load(open(os.path.join(BASE_DIR, 'conf', 'gift.json'), 'r', encoding='utf-8'))  # 由下面的self.gift替换了

    def __init__(self, roomid, db, gift):
        self.dyclient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dyclient.connect((HOST, PORT))
        self.login(roomid)
        self.db = db
        self.gift = gift
        self.handledanmu = HandleDanmu(self.db, self.gift)

        print('login success!')

    def sendmsg(self, msgstr):
        msg = msgstr.encode('utf-8')
        data_length = len(msg) + 8
        code = 689
        jiami = 0
        baomi = 0
        msgHead = int.to_bytes(data_length, 4, 'little') \
                  + int.to_bytes(data_length, 4, 'little') + int.to_bytes(code, 2, 'little') \
                  + int.to_bytes(jiami, 1, 'little') + int.to_bytes(baomi, 1, 'little')
        self.dyclient.sendall(msgHead + msg)

    def login(self, roomid):
        login_data = 'type@=loginreq/roomid@={}/\0'.format(roomid)
        self.sendmsg(login_data)
        # 服务器返回登录消息
        recv_data = self.dyclient.recv(BUFSIZ)
        # print(recv_data)
        # 入组消息 -9999表示海量弹幕
        joingroup_data = 'type@=joingroup/rid@={}/gid@=-9999/\0'.format(roomid)
        self.sendmsg(joingroup_data)

        recv_data = self.dyclient.recv(BUFSIZ)
        # print(recv_data)

    def logout(self):
        logout_data = 'type@=logout/\0'
        self.sendmsg(logout_data)

    def recvall(self, length):
        ret = b''
        while len(ret) < length:
            tmp = self.dyclient.recv(length-len(ret))
            ret = ret + tmp
        return ret

    def run(self):
        data = b''
        while True:
            '''
            xiaoxitou = self.dyclient.recv(12)
            recv_data_lenth = int.from_bytes(xiaoxitou[:4], 'little')  # 有时候数据传递慢，还没有收到length那么多的数据
            if recv_data_lenth < 5000:  # 有时候这个数字好大，明显错了。按理说，不应该会有这种错误的
                recv_data = xiaoxitou + self.recvall(recv_data_lenth - 8)   # 自己定义函数的解决上面说的问题
            else:
                recv_data = xiaoxitou + self.dyclient.recv(BUFSIZ)
            data = data + recv_data
            '''
            # 觉得上面这一段还不如  data = data + self.dyclient.recv(BUFSIZ) 写这一句
            data = data + self.dyclient.recv(BUFSIZ)
            # print(data)
            if b'/\x00' in data:  # 有一个（两个...）完整的记录
                danmu_list = data.split(b'/\x00')
                danmu, data = danmu_list[:-1], danmu_list[-1]
                # print(danmu)
                for i in danmu:
                    self.handle(i[12:])
                    # pass

    def handle(self, recv_data):

        # print(recv_data)
        try:
            recv_data = recv_data.decode('utf-8')
        except UnicodeDecodeError as e:
            return
        recv_data = recv_data.replace('@=', '=')
        # recv_data = recv_data.replace('@S', '/')
        recv_data = recv_data.replace('@A', '@')
        recv_data = recv_data.split('/')
        # print('------>', recv_data)
        data = {}
        for key_value in recv_data:
            if '=' in key_value:
                key_value = key_value.split('=', 1)
                key = key_value[0]
                value = key_value[1]
                data[key] = value
        if data.get('type', None):
            # print(data)   data是字典{}
            if hasattr(self.handledanmu, data.get('type')):
                getattr(self.handledanmu, data.get('type'))(data)
            # if data['type'] == 'chatmsg':
            #     result = [data['uid'], data['nn'], data['txt']]
            #     # result = [data['uid'], data['nn'], data['txt'].replace('丿', '/')]  # 弹幕不允许出现/符号，加了这个转换，原本是丿的也会转换成/
            #     # current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            #     current_time = datetime.datetime.now()
            #     result.append(current_time)
            #     print(result[1] + ': ' + result[2] + '\t' + str(result[-1]))
            #     self.db.save(result, self.db.danmu_table)
            # elif data['type'] == 'dgb':
            #     result = [data['rid'], data['gfid'], data['uid'], data['nn']]
            #     # current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            #     current_time = datetime.datetime.now()
            #     result.append(current_time)
            #     if result[1] in self.gift.keys():
            #         print(result[3] + '\t' + '送出了' + '\t' + self.gift[result[1]][0] + '\t' + str(result[-1]))
            #         self.db.save(result, self.db.gift_table)
            # else:
            #     pass

    def keeplive(self):
        while True:
            # unixtime = int(time.time())
            # msg = 'type@=keeplive/tick@=%d\0' % unixtime
            msg = 'type@=mrkl/\0'
            self.sendmsg(msg)
            time.sleep(15)


class HandleDanmu():
    def __init__(self, db, gift):
        self.db = db
        self.gift = gift

    def chatmsg(self, data):
        result = [data['uid'], data['nn'], data['txt']]
        # result = [data['uid'], data['nn'], data['txt'].replace('丿', '/')]  # 弹幕不允许出现/符号，加了这个转换，原本是丿的也会转换成/
        # current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        current_time = datetime.datetime.now()
        result.append(current_time)
        print(result[1] + ': ' + result[2] + '\t' + str(result[-1]))
        self.db.save(result, self.db.danmu_table)

    def dgb(self, data):
        result = [data['rid'], data['gfid'], data['uid'], data['nn']]
        # current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        current_time = datetime.datetime.now()
        result.append(current_time)
        if result[1] in self.gift.keys():
            print(result[3] + '\t' + '送出了' + '\t' + self.gift[result[1]][0] + '\t' + str(result[-1]))
            self.db.save(result, self.db.gift_table)


if __name__ == '__main__':
    roomid = input('请输入房间号：')
    savedb = db.SaveDb(roomid)
    dyclient = DouyuClient(roomid, savedb)
    run = threading.Thread(target=dyclient.run)
    keeplive = threading.Thread(target=dyclient.keeplive)
    run.start()
    keeplive.start()
