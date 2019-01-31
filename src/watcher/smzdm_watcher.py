# -*- encoding: utf-8 -*-

import os
import time
import random
import re
import json
import traceback

import config
from utils import log_utils, str_utils
from watcher.base_watcher import BaseWatcher


class SmzdmWatcher(BaseWatcher):
    _logger = None

    def __init__(self):
        BaseWatcher.__init__(self)
        self._logger = log_utils.get_logger(os.path.join(config.APP_CONFIG['log_path'], 'run.log'))
        pass

    def get_price(self, price):
        ss = re.findall(r'\d+[.\d]+', price)
        if len(ss) > 0:
            return float(ss[0])
        return None

    def get_item_by_json(self, item):
        info = {
            'title': '%s-%s' % (item['article_title'], item['article_price']),
            'category': item.get('article_category', {}).get('title', '无'),
            'mall': item['article_mall'],
            'url': item['article_url'],
            'prices': item['article_price'],
            'zhi': int(item.get('article_worthy', '0')),
            'buzhi': int(item.get('article_unworthy', '0')),
            'pl': int(item.get('article_comment', '0')),
            'timesort': item['article_timesort'],
        }

        info['price'] = self.get_price(info['prices'])

        self._logger.info('catch_item:' + str_utils.json_encode(info))
        return info

    def check_item(self, item):
        # 判断价格是否正常获取
        if None is item['price']:
            return False

        # 匹配词
        for word in config.APP_CONFIG['match_keywords']:
            if word['keyword'].lower() in item['title'].lower() and word['limit_price'] >= item['price']:
                return True

        # 过滤忽略词
        for word in config.APP_CONFIG['ignore_keywords']:
            if word in item['title'].lower() or word.lower() in item.get('category', ''):
                msg = '名称匹配过滤规则。名称：%s；分类：%s；匹配关键字：%s' % (item['title'], item.get('category', ''), word)
                self._logger.info(msg)
                return False

        # 比较值不值比例
        count = item['zhi'] + item['buzhi']
        if count <= 0:
            return False

        rate = item['zhi'] / count

        for rates in config.APP_CONFIG['assessment_rules']:
            if count >= rates['min_assessment_count'] and rate >= rates['worth_rate']:
                return True

        return False

    def watcher_service(self, url, type):
        content = self.get_web_content(url)
        infos = json.loads(content)
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
                info = self.get_item_by_json(item)
                time_sort = info['timesort']
                result = self.check_item(info)
                if True is result:
                    self.send_msg(info)
            except Exception as e:
                self._logger.error(str_utils.json_encode(item) + '; error:' + traceback.format_exc())
        return time_sort

    def send_msg(self, item):
        msg = '商品提醒：%s，值：%d，不值：%d，分类：%s，商城：%s，链接：%s' % (item['title'], item['zhi'], item['buzhi'],
                                                        item.get('category', '无'), item.get('mall', '无'), item['url'])

        self.send_wx_msg(item['url'], msg)

    def watcher_services(self, url, num, interval, type):
        if None is not num and num < 1:
            raise Exception('num 配置不能小于1')
        if None is not interval and interval < 5:
            raise Exception('collect_interval 配置不能小于5')
        time_sort = 9999999999
        for i in range(1, num):
            u = url.replace('{{time}}', str(time_sort))
            time_sort = self.watcher_service(u, type)
            time.sleep(interval + random.uniform(-1.0, 3.1))

    def run(self):
        for urls in config.APP_CONFIG['watcher_urls']:
            try:
                self.watcher_services(urls['url'], urls['num'], config.APP_CONFIG['collect_interval'], urls['type'])
            except Exception as e:
                print(str(e))
                raise e
        return
        time.sleep(config.APP_CONFIG['task_interval'])


if __name__ == '__main__':
    smzdm = SmzdmWatcher()
    smzdm.run()
