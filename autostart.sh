#!/bin/bash
# chkconfig: 345 90 90
# description: autostart......
cd /root/v2ray_client
nohup ./v2ray run -config=config.json &
cd /root
nohup python /root/test.py &
