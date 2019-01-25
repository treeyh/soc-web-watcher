# -*- encoding: utf-8 -*-

import os
from watcher import smzdm_watcher
import itchat
import config


if __name__ == '__main__':
    config.APP_CONFIG['log_path'] = os.path.join(os.getcwd(), '..', 'logs')
    itchat.auto_login(True)

    smz = smzdm_watcher.SmzdmWatcher()
    smz.run()