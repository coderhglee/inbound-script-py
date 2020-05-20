#!/bin/sh

#path=/arcstore/ns-home/newspaper/work/newswork/image-wires-agent/sh/pid.txt
#log=/arcstore/ns-home/newspaper/work/newswork/image-wires-agent/logs/wires.log

path=/Users/hakgyun/repository_chosunbiz/inbound-script-py/sh/pid.txt
log=/Users/hakgyun/repository_chosunbiz/inbound-script-py/logs/wires.log

if [ -f $path ]
        then  read pid<$path
              kill -15 -- -$pid
                  rm $path
                  echo "[DEBUG] ********************************* WIRES AGENT IS DISCONNECTED ***********************************">>$log
else echo "pid.txt is not found"
fi