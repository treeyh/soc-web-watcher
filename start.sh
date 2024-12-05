#!/bin/bash

#取当前目录
BASE_PATH=`cd "$(dirname "$0")"; pwd`

cd $BASE_PATH

#if [ ! -f "BASE_PATH/.venv/bin/activate" ]; then
#    echo 'create venv'
#    uv venv 
#fi

source $BASE_PATH/.venv/bin/activate

uv pip install -r $BASE_PATH/requirements.txt

echo "nohup python -m soc_web_watcher >/dev/null 2>&1 &"

nohup python -m soc_web_watcher >/dev/null 2>&1 &
