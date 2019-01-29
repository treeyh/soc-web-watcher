# -*- encoding: utf-8 -*-

import os
import time
import random
import re
import requests
import json
from bs4 import BeautifulSoup
import itchat

from utils import log_utils
import config
from watcher.base_watcher import BaseWatcher


class SmzdmWatcher(BaseWatcher):
    _logger = None

    def __init__(self):
        self._logger = log_utils.get_logger(os.path.join(config.APP_CONFIG['log_path'], 'run.log'))
        pass

    def get_price(self, price):
        ss = re.findall(r'\d+[.\d]+', price)
        if len(ss) > 0:
            return float(ss[0])
        return None

    def get_item(self, item):
        info = {}
        info['title'] = item.find('h5').find('a').get_text()
        info['url'] = item.find('h5').find('a')['href']
        info['prices'] = item.find('h5').find('span', class_='z-highlight').get_text()
        zs = item.find('span', class_='feed-btn-group').find_all('span', class_='unvoted-wrap')
        info['zhi'] = int(zs[0].get_text().strip())
        info['buzhi'] = int(zs[1].get_text().strip())
        info['pl'] = item.find('div', class_='z-feed-foot-l').find('a', class_='z-group-data').get_text().strip()
        info['price'] = self.get_price(info['prices'])

        self._logger.info('catch_item:' + json.dumps(info))
        return info

    def get_item_by_json(self, item):
        info = {}
        info['title'] = '%s-%s' % (item['article_title'], item['article_price'])
        info['category'] = item.get('article_category', {}).get('title', '无')
        info['mall'] = item['article_mall']
        info['url'] = item['article_url']
        info['prices'] = item['article_price']
        info['zhi'] = int(item['article_worthy'])
        info['buzhi'] = int(item['article_unworthy'])
        info['pl'] = int(item['article_comment'])
        info['price'] = self.get_price(info['prices'])

        info['timesort'] = item['article_timesort']

        self._logger.info('catch_item:' + json.dumps(info))
        return info

    def check_item(self, item):
        # 判断价格是否正常获取
        if None is item['price']:
            return False

        # 过滤忽略词
        for word in config.APP_CONFIG['ignore_keywords']:
            if word.lower() in item['title'].lower() or word.lower() in item.get('category', ''):
                self._logger.info('名称匹配过滤规则。名称：' + item['title'])
                return False
        # 匹配词
        for word in config.APP_CONFIG['match_keywords']:
            if word['keyword'].lower() in item['title'].lower() and word['limit_price'] >= item['price']:
                return True

        # 比较值不值比例
        count = item['zhi'] + item['buzhi']
        if count <= 0:
            return False

        rate = item['zhi'] / count

        for rates in config.APP_CONFIG['assessment_rules']:
            if count >= rates['min_assessment_count'] and rate >= rates['worth_rate']:
                return True

        return False

    def watcher_page(self, url):
        content = self.get_web_content(url)
        if None is content:
            return
        soup = BeautifulSoup(content, 'html.parser')
        items = soup.find(id='feed-main-list').find_all('li', class_='feed-row-wide')

        for item in items:
            info = self.get_item(item)
            result = self.check_item(info)
            if True is result:
                self.send_msg(info)

    def watcher_service(self, url):
        content = self.get_web_content(url)
        items = json.loads(content)
        if None is items or 0 >= len(items['article_list']):
            return

        time_sort = 0
        for item in items['article_list']:
            info = self.get_item_by_json(item)
            time_sort = info['timesort']
            result = self.check_item(info)
            if True is result:
                self.send_msg(info)
        return time_sort

    def send_msg(self, item):
        msg = '商品提醒：%s，值：%d，不值：%d，分类：%s，商城：%s，链接：%s' % (item['title'], item.get('mall', '无'), item['zhi'], item['buzhi'], item.get('category', '无'), item['url'])
        print('send msg: %s' % msg)
        # self.send_wx(msg)



    def watcher_pages(self, url, num, interval):
        if None is not num and num < 1:
            raise Exception('num 配置不能小于1')
        if None is not interval and interval < 5:
            raise Exception('collect_interval 配置不能小于5')
        for i in range(1, num):
            u = url.replace('{{page}}', str(i))
            self.watcher_page(u)
            return
            time.sleep(interval + random.uniform(-1.0, 3.1))

    def watcher_services(self, url, num, interval):
        if None is not num and num < 1:
            raise Exception('num 配置不能小于1')
        if None is not interval and interval < 5:
            raise Exception('collect_interval 配置不能小于5')
        time_sort = 9999999999
        for i in range(1, num):
            u = url.replace('{{time}}', str(time_sort))
            time_sort = self.watcher_service(u)
            time.sleep(interval + random.uniform(-1.0, 3.1))

    def run(self):
        for urls in config.APP_CONFIG['watcher_urls']:
            try:
                if 'page' is urls['type']:
                    self.watcher_pages(urls['url'], urls['num'], config.APP_CONFIG['collect_interval'])
                else:
                    self.watcher_services(urls['url'], urls['num'], config.APP_CONFIG['collect_interval'])
            except Exception as e:
                print(str(e))
                raise e
        return
        time.sleep(config.APP_CONFIG['task_interval'])


if __name__ == '__main__':
    smzdm = SmzdmWatcher()
    smzdm.run()
