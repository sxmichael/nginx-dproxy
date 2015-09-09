#!/bin/bash
cwd=$(dirname $0)
$cwd/build_config.sh &
sleep 3
echo Starting nginx with new configuration:
cat /etc/nginx/conf.d/default.conf
nginx -g 'daemon off;'
