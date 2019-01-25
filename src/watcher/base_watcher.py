# -*- encoding: utf-8 -*-

import os

import requests
from random import choice
import itchat

import config


class BaseWatcher(object):

    def __init__(self):
        super()
        pass

    def get_user_agent(self):
        return choice(config.APP_CONFIG['user_agents'])


    def get_html(self, url):
        headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                   "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                   "User-Agent": self.get_user_agent(),
                   }

        result = requests.get(url=url, headers=headers)
        if 200 == result.status_code:
            return result.content
        return None

    def send_wx(self, msg):
        itchat.send(msg, toUserName='filehelper')

