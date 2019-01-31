#!/bin/bash

#取当前目录
BASE_PATH=`cd "$(dirname "$0")"; pwd`

source $BASE_PATH/venv/bin/activate

pip install -r $BASE_PATH/requirements.txt

nohup $BASE_PATH/ >/data/logs/ssserver/account.log 2>&1 &