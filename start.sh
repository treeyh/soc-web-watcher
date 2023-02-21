#!/bin/bash

#取当前目录
BASE_PATH=`cd "$(dirname "$0")"; pwd`

cd $BASE_PATH

if [ ! -f "BASE_PATH/venv/bin/activate" ]; then
    mkdir -p $BASE_PATH/venv
    /opt/soft/python311/bin/python3 -m venv venv/.
fi

source $BASE_PATH/venv/bin/activate

pip install -r $BASE_PATH/requirements.txt

echo "nohup python $BASE_PATH/src/start.py >/dev/null 2>&1 &"

nohup python $BASE_PATH/src/start.py >/dev/null 2>&1 &