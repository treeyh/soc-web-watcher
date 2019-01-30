# -*- encoding: utf-8 -*-

import os
import time
import requests
from random import choice
import itchat

from utils import log_utils
import config


class BaseWatcher(object):
    _logger = None
    _check_interval = None
    _check_time = None
    _msg_map = None

    def __init__(self):
        self._logger = log_utils.get_logger(os.path.join(config.APP_CONFIG['log_path'], 'run.log'))
        self._check_time = time.time()
        self._check_interval = 48 * 60 * 60
        self._msg_map = {}

    def get_user_agent(self):
        """
        获取ua信息
        :return: ua
        """
        return choice(config.APP_CONFIG['user_agents'])

    def get_web_content(self, url):
        """
        http方法
        :param url:
        :return:
        """
        headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                   "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                   "User-Agent": self.get_user_agent(),
                   }

        result = requests.get(url=url, headers=headers)
        if 200 == result.status_code:
            return result.content
        return None

    def check_msg_send(self, identity):
        """
        验证消息是否需要发送
        :param identity:
        :return:
        """
        print(self._msg_map)
        print(self._check_interval)
        print(self._check_time)
        if None is not self._msg_map.get(identity, None):
            return False
        ti = time.time()
        if ti > self._check_time + self._check_interval:
            self.clear_msg()
        self._msg_map[identity] = time.time()
        return True

    def clear_msg(self):
        """
        清理过期消息
        :return:
        """
        for k, v in self._msg_map.items():
            if v < self._check_time:
                del self._msg_map[k]
        self._check_time = time

    def send_wx_msg(self, identity, msg):
        """
        发送微信消息
        :param identity: 消息标识
        :param msg: 消息内容
        :return:
        """
        self._logger.info('send msg: %s' % msg)
        if self.check_msg_send(identity):
            itchat.send(msg, toUserName=config.APP_CONFIG['msg_send_user'])
            self._logger.info('send over msg: %s' % msg)
