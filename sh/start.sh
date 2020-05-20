#export WORK_PATH=/arcstore/ns-home/newspaper/work/newswork/image-wires-agent
export WORK_PATH=/Users/hakgyun/repository_chosunbiz/inbound-script-py
export ENV_PATH=$WORK_PATH/env.ini
export PYTHON_VENV=/venv/bin/python

$WORK_PATH$PYTHON_VENV $WORK_PATH/wires -m & echo $$ > $WORK_PATH/sh/pid.txt