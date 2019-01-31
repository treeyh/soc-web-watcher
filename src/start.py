# -*- encoding: utf-8 -*-

import sys
import io
import os
import platform

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


def load_ignore_keywords():
    keywords = read_all_lines_file(os.path.join(os.getcwd(), 'ignore_keywords.txt'))
    keys = []
    for key in keywords:
        k = key.strip().lower()
        if None is k or '' is k or '#' is k[0]:
            continue
        keys.append(k)
    config.APP_CONFIG['ignore_keywords'] = keys


def run():
    config.APP_CONFIG['log_path'] = os.path.join(os.getcwd(), '..', 'logs')

    load_ignore_keywords()
    itchat.auto_login(True)
    smz = smzdm_watcher.SmzdmWatcher()
    smz.run()


if __name__ == '__main__':
    system = platform.system()
    if system is 'Windows':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='gb18030')
    run()
