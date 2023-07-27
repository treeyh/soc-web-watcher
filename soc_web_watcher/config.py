# -*- encoding: utf-8 -*-

import os

# 系统版本号
VERSION = "1.0.0"

# 应用名称
APP_NAME = "soc-web-watcher"

APP_CONFIG = {
    # 任务循环间隔 秒, 不能小于10秒
    "task_interval": 60,
    # 采集间隔 秒, 不能小于1秒
    "collect_interval": 1,
    # 日志路径
    "log_path": os.path.join("/data/logs", APP_NAME),
    # 是否打印详细日志
    "is_print_detail": True,
    # redis 配置
    "redis_config": {
        "host": "127.0.0.1",
        "port": 6379,
        "db": 0,
        "password": "",
    },
    # 缓存key前缀
    "cache_pre_key": "soc-web-watcher",
    # 通知类型，dingding或feishu
    "notification_type": "dingding",
    # 钉钉通知地址
    "dingding_send_url": "",
    "feishu_send_url": "",
    # 微信消息发送用户名列表, 启动后会补充用户昵称列表内用户
    "msg_send_users": [
        "filehelper",
    ],
    # 微信消息发送用户昵称列表
    "msg_send_nick_names": [
        "测试用户",
    ],
    # 采集url列表
    "watcher_urls": [
        {
            # 类型 服务 精选好价
            "type": "service1",
            # 采集url
            "url": "https://www.smzdm.com/jingxuan/json_more?timesort={{time}}&filter=s0f0t0b0d0r0p0",
            # 采集几页
            "num": 36,
        },
        {
            # 类型 服务 全部好价
            "type": "service2",
            # 采集url
            "url": "https://www.smzdm.com/json_more?type=a&timesort={{time}}",
            # 采集几页
            "num": 72,
        },
    ],
    # 采集user_agents
    "user_agents": [
        # Edge
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78",
        # windows chrome
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        # Ubuntu Chrome
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        # mac Chrome
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        # Ubuntu Firefox
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
        # mac Firefox
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:109.0) Gecko/20100101 Firefox/109.0",
    ],
    # 最大价格，超过该价格不通知
    "max_price": 9999,
    # 最小评论数，防止刷票，在匹配值百分比后判断
    "min_comment": 3,
    # 匹配评价百分比规则列表
    "assessment_rules": [
        {
            # 评价数量
            "min_assessment_count": 13,
            # 值所占比例
            "worth_rate": 0.8,
        },
        {
            "min_assessment_count": 30,
            "worth_rate": 0.76,
        },
    ],
    # 匹配关键词, 匹配到低于价位直接发提醒
    "match_keywords": [
        # {
        #     # 关键词
        #     'keyword': 'airpods',
        #     # 价格限制，低于该价格会通知
        #     'limit_price': 900,
        # },
        {
            # 关键词
            "keyword": "美浓烧",
            # 价格限制，低于该价格会通知，为负数则不做价格判断
            "limit_price": -1,
        },
        {
            # 关键词
            "keyword": "张一元",
            # 价格限制，低于该价格会通知，为负数则不做价格判断
            "limit_price": -1,
        },
        {
            # 关键词
            "keyword": "Selsun Gold",
            # 价格限制，低于该价格会通知，为负数则不做价格判断
            "limit_price": -1,
        },
        {
            # 关键词
            "keyword": "限免",
            # 价格限制，低于该价格会通知，为负数则不做价格判断
            "limit_price": -1,
        },
    ],
    # 忽略关键词 同时忽略标题和分类，启动时会从ignore_keywords.txt文件中读取
    "ignore_keywords": [],
}
