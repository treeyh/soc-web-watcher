# -*- encoding: utf-8 -*-

import os

APP_CONFIG = {

    # 系统版本号
    'version': '0.0.1',

    # 任务循环间隔 秒, 不能小于5秒
    'task_interval': 30,

    # 采集间隔 秒, 不能小于5秒
    'collect_interval': 7,

    # 日志路径
    'log_path': '~/work/99_tree/03_github/soc-web-watcher/logs',

    # 采集url列表
    'watcher_urls': [
        {
            # 采集url
            'url': 'https://www.smzdm.com/jingxuan/p{{page}}/',
            # 采集几页
            'num': 12,
        }
    ],

    # 采集user_agents
    'user_agents': [
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36',
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:64.0) Gecko/20100101 Firefox/64.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:63.0) Gecko/20100101 Firefox/63.0',
    ],

    # 匹配评价百分比规则列表
    'assessment_rules': [
        {
            # 评价数量
            'min_assessment_count': 10,
            # 值所占比例
            'worth_rate': 0.8,
        },
        {
            'min_assessment_count': 25,
            'worth_rate': 0.7,
        },
    ],

    # 匹配关键词, 匹配到低于价位直接发提醒
    'match_keywords': [
        {
            # 关键词
            'keyword': '测试',
            # 价格限制，低于该价格会通知
            'limit_price': 12.1,
        }
    ],

    # 忽略关键词
    'ignore_keywords': [
        '测试',
    ]

}