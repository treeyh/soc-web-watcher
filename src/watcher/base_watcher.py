# -*- encoding: utf-8 -*-

import os
import time
import requests
from random import choice
import itchat
import traceback

from utils import log_utils, redis_utils, str_utils
import config


class BaseWatcher(object):
    _logger = None
    _check_interval = None
    _check_time = None
    _msg_map = None
    _send_wx_users = None
    _redis_utils = None
    _ding_headers = None


    def __init__(self):
        self._logger = log_utils.get_logger(os.path.join(config.APP_CONFIG['log_path'], 'run.log'))
        self._send_wx_users = config.APP_CONFIG['msg_send_users']
        self._check_time = time.time()
        self._check_interval = 48 * 60 * 60
        self._msg_map = {}
        self._redis_utils = redis_utils.get_redis_utils(**config.APP_CONFIG['redis_config'])
        self._ding_headers = {
            'Content-Type' : 'application/json',
        }


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
                   'Connection': 'close',
                   }
        session = requests.session()
        session.keep_alive = False
        try:
            result = requests.get(url=url, headers=headers, timeout=3)
            if 200 == result.status_code:
                return result.content
        except:
            self._logger.error('error:' + traceback.format_exc())
            return None
        return None

    def check_msg_send(self, id):
        """
        验证消息是否需要发送
        :param id:
        :return:
        """
        key = '%s:%s' % (config.APP_CONFIG['cache_pre_key'], id)
        if None is not self._redis_utils.get(key):
            if config.APP_CONFIG['is_print_detail']:
                self._logger.info('send msg exsit key:%s' % key)
            return False
        ti = str(int(time.time()))

        self._redis_utils.set(key=key, val=ti, time=self._check_interval)
        return True

    def send_wx_msg(self, id, msg):
        """
        发送微信消息
        :param id: 消息标识
        :param msg: 消息内容
        :return:
        """
        # self._logger.info('send msg: %s' % msg)
        if self.check_msg_send(id):
            for user in self._send_wx_users:
                result = itchat.send(msg, toUserName=user)
                if config.APP_CONFIG['is_print_detail']:
                    self._logger.info(result)
            self._logger.info('send msg over msgid:%s, users:%s, msg: %s' % (id, str_utils.json_encode(self._send_wx_users), msg))
            return True
        return False

    def send_ding_msg(self, id, msg):
        """
        发送微信消息
        :param id: 消息标识
        :param msg: 消息内容
        :return:
        """
        # self._logger.info('send msg: %s' % msg)
        if self.check_msg_send(id):
            result = requests.post(config.APP_CONFIG['dingding_send_url'], data=msg.encode('utf-8'), headers=self._ding_headers)
            if config.APP_CONFIG['is_print_detail']:
                self._logger.info('send ding msg over msgid:%s, state: %d, result:%s, msg: %s' % (id, result.status_code, result.text, msg))
            return True
        return False


