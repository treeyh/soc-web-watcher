# -*- encoding: utf-8 -*-

import os
import time
import random
import re
import json
import traceback

from soc_web_watcher import config
from soc_web_watcher.utils import log_utils, str_utils
from soc_web_watcher.watcher.base_watcher import BaseWatcher


class SmzdmWatcher(BaseWatcher):
  _logger = None

  _send_msg_status = None

  def __init__(self):
    BaseWatcher.__init__(self)
    self._logger = log_utils.get_logger(os.path.join(config.APP_CONFIG['log_path'], 'run.log'))
    self._send_msg_status = False
    pass

  def get_price(self, price):
    ss = re.findall(r'\d+[.\d]+', price)
    if len(ss) > 0:
      return float(ss[0])
    return None

  def get_item_by_json(self, item, type):

    cates = item.get('article_category', {})

    if isinstance(cates, str):
      category = cates
    elif isinstance(cates, list):
      if len(cates) > 0:
        category = str(cates[0])
      else:
        category = '无'
    else:
      category = cates.get('title', '无')

    info = {
        'id': item.get('article_id', ''),
        'title': '%s-%s' % (item['article_title'], item['article_price']),
        'category': category,
        'mall': item['article_mall'],
        'url': item['article_url'],
        'prices': item['article_price'],
        'worthy': int(item.get('article_worthy', '0')),
        'unworthy': int(item.get('article_unworthy', '0')),
        'comment': int(item.get('article_comment', '0')),
    }

    if 'service1' is type:
      info['top_category'] = ''
      info['pic_url'] = item.get('article_pic_url', '')
      info['timesort'] = item.get('article_timesort', 0)
    elif 'service2' is type:
      info['top_category'] = item.get('top_category', '')
      info['pic_url'] = item.get('article_pic', '')
      info['timesort'] = item.get('timesort', 0)
    else:
      return None

    info['price'] = self.get_price(info['prices'])

    if config.APP_CONFIG['is_print_detail']:
      self._logger.info('catch_item:' + str_utils.json_encode(info))
    return info

  def check_item(self, item):
    # 判断匹配词
    for word in config.APP_CONFIG['match_keywords']:
      key = word['keyword'].lower()
      if key not in item['title'].lower() and key not in item['category'] and key not in item['top_category']:
        continue
      if word['limit_price'] <= 0:
        return True, 0
      if None is not item.get('price', None) and word['limit_price'] >= item['price']:
        return True, 0

    # 判断价格是否正常获取
    if None is item.get('price', None) or config.APP_CONFIG['max_price'] <= item['price']:
      return False, 0

    # 过滤忽略词
    for word in config.APP_CONFIG['ignore_keywords']:
      if word in item['title'].lower() or word in item['category'].lower() or word in item['top_category'].lower():
        msg = u'keyword matching ignore keywords。名称：%s；分类：%s；匹配关键字：%s' % (
            item['title'], item['category'], word)
        if config.APP_CONFIG['is_print_detail']:
          self._logger.info(msg)
        return False, 0

    # 比较值不值比例
    count = item['worthy'] + item['unworthy']
    if count <= 0:
      return False, 0

    rate = item['worthy'] / count

    for rates in config.APP_CONFIG['assessment_rules']:
      # 判断值比例评论数
      if count >= rates['min_assessment_count'] and rate >= rates['worth_rate'] and \
              None is not item['comment'] and item['comment'] >= config.APP_CONFIG['min_comment']:
        return True, rate * 100

    return False, 0

  def watcher_service(self, url, type, page):
    content = self.get_web_content(url)
    if content is None:
      return
    try:
      infos = json.loads(content)
    except Exception as e:
      self._logger.error('json.loads_fail: '+ content + '; error:' + traceback.format_exc())
      return
    items = []
    if 'service1' is type:
      items = infos.get('article_list', [])
    else:
      items = infos
    if None is items or 0 >= len(items):
      return

    time_sort = 0
    for item in items:
      try:
        info = self.get_item_by_json(item, type)
        if None is info:
          continue
        time_sort = info['timesort']
        result, rate = self.check_item(info)

        if True is result:
          if config.APP_CONFIG['is_print_detail']:
            self._logger.info(' page:%d; url:%s; send_msg:%s;' %
                              (page, url, str_utils.json_encode(info)))
          info['title'] = info['title'] + " " + ('%.2f' % rate) + "%"
          self.send_msg(info)
      except Exception as e:
        self._logger.error(str_utils.json_encode(item) + '; error:' + traceback.format_exc())
    return time_sort

  def send_msg(self, item):
    msg = '''{
     "msgtype": "markdown",
     "markdown": {"title":"%s",
"text":"#### %s  \n > 值:%d，不值:%d，评论:%d \n > 商城:%s,分类:%s%s\n > [%s](%s)\n\n ![%s](%s)"
     },
    "at": {
        "atMobiles": [], 
        "isAtAll": false
    }
 }''' % (item['title'], item['title'], item['worthy'], item['unworthy'], item['comment'], item['mall'],
         '' if '' is item.get('top_category', '') else (
        '%s-' % item['top_category']),
        item['category'], item['url'], item['url'], item['title'], item['pic_url'])

    # msg = '【提醒】%s\n值:%d，不值:%d，评论:%d\n商城:%s,分类:%s%s\n%s' % (item['title'], item['worthy'],
    #                                                        item['unworthy'], item['comment'], item['mall'],
    #                                                        '' if '' is item.get('top_category', '') else (
    #                                                                '%s-' % item['top_category']),
    #                                                        item['category'], item['url'])
    # self.send_wx_msg(item['id'], msg)
    self.send_ding_msg(item['id'], msg)

  def watcher_services(self, url, num, interval, type):
    if None is not num and num < 1:
      raise Exception('num 配置不能小于1')
    if None is not interval and interval < 1:
      raise Exception('collect_interval 配置不能小于1')
    time_sort = 9999999999
    for i in range(1, num):
      u = url.replace('{{time}}', str(time_sort))
      self._logger.info('.......................watcher_run type:%s, page:%d, url:%s  ........................'
                        % (type, i, u))
      time_sort = self.watcher_service(u, type, i)
      time.sleep(interval + random.uniform(0, 2.1))

  def run(self):
    if None is not config.APP_CONFIG['task_interval'] and config.APP_CONFIG['task_interval'] < 10:
      msg = 'task_interval 配置不能小于10'
      self._logger.error(msg)
      raise Exception(msg)
    while True:
      self._send_msg_status = False
      for urls in config.APP_CONFIG['watcher_urls']:
        try:
          self.watcher_services(urls['url'], urls['num'],
                                config.APP_CONFIG['collect_interval'], urls['type'])
        except Exception as e:
          self._logger.error('error:' + traceback.format_exc())
          raise e
      # if self._send_msg_status:
      #     self.send_wx_msg(str(time.time()), '---------------')
      time.sleep(config.APP_CONFIG['task_interval'] + random.uniform(0, 3.1))


if __name__ == '__main__':
  smzdm = SmzdmWatcher()
  smzdm.run()
