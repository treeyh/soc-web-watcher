# -*- encoding: utf-8 -*-

import os
from watcher import smzdm_watcher
import itchat
import config


def read_all_lines_file(file_path, method='r'):
    """
    读取所有文件，一次性读取所有内容， 文件不存在返回 None
    :param file_path: 文件路径
    :param method: 读取方式，'r'读取，'rb' 二进制方式读取
    :return:
    """
    if not os.path.exists(file_path):
        return None
    fh = open(file_path, method, encoding='UTF-8')
    try:
        c = fh.readlines()
        return c
    finally:
        fh.close()

def run():
    config.APP_CONFIG['log_path'] = os.path.join(os.getcwd(), '..', 'logs')
    itchat.auto_login(True)

    keywords = read_all_lines_file(os.path.join(os.getcwd(), 'ignore_keywords.txt'))

    keys = []
    for key in keywords:
        k = key.strip().lower()
        if '' is k:
            continue
        keys.append(k)
    config.APP_CONFIG['ignore_keywords'] = keys

    smz = smzdm_watcher.SmzdmWatcher()
    smz.run()

if __name__ == '__main__':
    run()
