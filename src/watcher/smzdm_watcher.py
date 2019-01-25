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

    def check_item(self, item):
        # 判断价格是否正常获取
        if None is item['price']:
            return False

        # 过滤忽略词
        for word in config.APP_CONFIG['ignore_keywords']:
            if word.lower() in item['title'].lower():
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
        html = self.get_html(url)
        if None is html:
            return
        soup = BeautifulSoup(html, 'html.parser')
        items = soup.find(id='feed-main-list').find_all('li', class_='feed-row-wide')

        for item in items:
            info = self.get_item(item)
            result = self.check_item(info)
            if True is result:
                msg = '商品提醒：%s，值：%d，不值：%d，链接：%s' % (info['title'], info['zhi'], info['buzhi'], info['url'])
                print('send msg: %s' % msg)
                self.send_wx(msg)

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

    def run(self):
        for urls in config.APP_CONFIG['watcher_urls']:
            try:
                self.watcher_pages(urls['url'], urls['num'], config.APP_CONFIG['collect_interval'])
            except Exception as e:
                print(str(e))
                raise e
        return
        time.sleep(config.APP_CONFIG['task_interval'])


if __name__ == '__main__':
    smzdm = SmzdmWatcher()
    smzdm.run()
