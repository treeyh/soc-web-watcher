# -*- encoding: utf-8 -*-

import os

# 系统版本号
VERSION = '1.0.0'

# 应用名称
APP_NAME = 'soc-web-watcher'

APP_CONFIG = {

    # 任务循环间隔 秒, 不能小于5秒
    'task_interval': 30,

    # 采集间隔 秒, 不能小于5秒
    'collect_interval': 7,

    # 日志路径
    'log_path': os.path.join('/data/logs', APP_NAME),

    # 微信消息发送用户名
    'msg_send_user': 'filehelper',

    # 采集url列表
    'watcher_urls': [
        {
            #类型 服务 精选好价
            'type': 'service1',
            # 采集url
            'url': 'https://www.smzdm.com/jingxuan/json_more?timesort={{time}}&filter=s0f0t0b0d0r0p0',
            # 采集几页
            'num': 12,
        },
        {
            #类型 服务 全部好价
            'type': 'service2',
            # 采集url
            'url': 'https://www.smzdm.com/json_more?type=a&timesort={{time}}',
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

    # 最大价格，超过该价格不通知
    'max_price': 9999,

    # 最小评论数，防止刷票
    'min_comment': 3,

    # 匹配评价百分比规则列表
    'assessment_rules': [
        {
            # 评价数量
            'min_assessment_count': 13,
            # 值所占比例
            'worth_rate': 0.8,
        },
        {
            'min_assessment_count': 30,
            'worth_rate': 0.76,
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

    # 忽略关键词 同时忽略标题和分类，启动时会从ignore_keywords.txt文件中读取
    'ignore_keywords': []

}
