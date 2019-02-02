# -*- encoding: utf-8 -*-

import itchat


def run():
    itchat.auto_login(enableCmdQR=True, hotReload=True)
    print(itchat.search_friends(nickName='test'))


if __name__ == '__main__':
    run()
