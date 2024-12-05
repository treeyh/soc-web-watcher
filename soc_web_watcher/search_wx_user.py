# -*- encoding: utf-8 -*-

import itchat


def run():
    itchat.auto_login(enableCmdQR=2, hotReload=True)
    print(itchat.search_friends(nickName="测试用户"))


if __name__ == "__main__":
    run()
