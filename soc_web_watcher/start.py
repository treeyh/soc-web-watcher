# -*- encoding: utf-8 -*-

import sys
import io
import os
import platform

#import itchat

from soc_web_watcher.utils import log_utils
from soc_web_watcher.watcher import smzdm_watcher
from soc_web_watcher import config

_logger = None


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


def walk2(path):
  '''
      列举path下的所有文件、文件夹
  '''
  fpaths = []
  for pt, fl, fi in os.walk(path):
    for f in fi:
      fpaths.append((pt, f))
  return fpaths


def get_file_suffix(path):
  '''
      获取文件后缀
      path：文件路径，可使用__file__
  '''
  return os.path.splitext(path)[1][1:]


def load_ignore_keywords_info(filePath, keys):
  filep = os.path.join(filePath[0], filePath[1])

  if 'txt' != get_file_suffix(filep):
    return keys

  keywords = read_all_lines_file(filep)
  for key in keywords:
    k = key.strip().lower()
    if None is k or '' is k or '#' is k[0]:
      continue
    keys.append(k)
  return keys


def load_ignore_keywords(self_path):

  ik_paths = walk2(os.path.join(self_path, 'ignore_keyword'))

  keys = []
  for p in ik_paths:
    keys = load_ignore_keywords_info(p, keys)
  config.APP_CONFIG['ignore_keywords'] = keys


#def init_send_wx_users():
#  '''
#  初始化微信发送用户名
#  :return:
#  '''
#
#  for nick_name in config.APP_CONFIG['msg_send_nick_names']:
#    users = itchat.search_friends(nickName=nick_name)
#    if None is users or len(users) <= 0:
#      continue
#    _logger.info('send wx nickname:%s; username:%s' % (nick_name, users[0].UserName))
#    config.APP_CONFIG['msg_send_users'].append(users[0].UserName)
#  _logger.info('send wx users:%s' % (config.APP_CONFIG['msg_send_users']))


def check_wx_login():
  login_result = itchat.check_login()
  if '200' is not login_result:
    _logger.error('wx login fail')
    sys.exit(-2)
  return True


def run():

  self_path = os.path.split(os.path.realpath(__file__))[0]
  # config.APP_CONFIG['log_path'] = os.path.join(self_path, '..', 'logs')
  _logger = log_utils.get_logger(os.path.join(config.APP_CONFIG['log_path'], 'run.log'))

  system = platform.system()
  if system is 'Windows':
    _logger.error('soc-web-watcher can not run windows.')
    sys.exit(-1)

  load_ignore_keywords(self_path)

  # itchat.auto_login(enableCmdQR=2, hotReload=True)
  # check_wx_login()

  # init_send_wx_users()
  smz = smzdm_watcher.SmzdmWatcher()
  smz.run()


if __name__ == '__main__':
  run()
