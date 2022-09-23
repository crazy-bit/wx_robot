'''
reference https://github.com/smallevilbeast/ntchat
'''

# -*- coding: utf-8 -*-
import sys
import ntchat
import logging
import monitor
import config


# 启动微信robot
wechat = ntchat.WeChat()

'''
# 注册消息回调
@wechat.msg_register(ntchat.MT_RECV_TEXT_MSG)
def on_recv_text_msg(wechat_instance: ntchat.WeChat, message):
    data = message["data"]
    from_wxid = data["from_wxid"]
    self_wxid = wechat_instance.get_login_info()["wxid"]

    # 判断消息不是自己发的，并回复对方
    if data['room_wxid'] == "5121533646@chatroom":
        if from_wxid != self_wxid:
            wechat_instance.send_text(to_wxid=data["from_wxid"], content=f"I'm a robot: {data['msg']}")
'''


def load_config(file):
    f = open(file, 'r', encoding='utf-8')
    for line in f.readlines():
        if "#" in line:
            continue
        if 'monitor_dir' in line:
            monitor_dir = line.split('=')[1].strip()
            config.monitor_dir = monitor_dir
            continue
        if 'room_wx_id' in line:
            room_wx_id = line.split('=')[1].strip()
            config.room_wx_id = room_wx_id
        if 'continous_open' in line:
            continous_open = line.split('=')[1].strip()
            config.continous_open = continous_open
    print("load config:")
    print(config.monitor_dir)
    print(config.room_wx_id)
    print(config.continous_open)
    f.close()

if __name__ == "__main__":
    # 初始化日志
    logging.basicConfig(level=logging.INFO,
                format='%(asctime)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S')
    
    # 加载配置
    load_config("config.txt")

    # 监听文件
    monitor.monitor(config.monitor_dir)
    
    # 打开pc微信, smart: 是否管理已经登录的微信
    wechat.open(smart=True)
    # 等待登录
    wechat.wait_login()

    # 保存联系人
    f = open('contacts.txt', 'w', encoding='utf-8')
    contacts = wechat.get_contacts()
    for i, data in enumerate(contacts):
        f.write(str(data) + '\n')
    f.close()

    # 保存群
    f = open('rooms.txt', 'w', encoding='utf-8')
    rooms = wechat.get_rooms()
    for i, data in enumerate(rooms):
        f.write(str(data) + '\n')
    f.close()

    print("===============================================")
    print("robot start")
    print("===============================================")
    #wechat.send_text(to_wxid=config.room_wx_id, content="hello world test")

    try:
        while True:
            if config.send_content != "":
                content ="test"
                logging.info("send content %s to wx:%s", config.send_content, config.room_wx_id)
                wechat.send_text(to_wxid=config.room_wx_id, content=config.send_content)
                config.send_content = ""
            
            # 定时打开文件
            f = open(config.continous_open, 'r', encoding='gbk')
            f.close()
            pass
    except KeyboardInterrupt:
        ntchat.exit_()
        sys.exit()