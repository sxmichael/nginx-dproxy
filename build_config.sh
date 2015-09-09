#!/bin/bash
cwd=$(dirname $0)
tmp_conf=$(mktemp)
nginx_conf=/etc/nginx/conf.d/default.conf
while true; do
  python $cwd/build_config.py > $tmp_conf
  if diff $tmp_conf $nginx_conf >/dev/null ; then
    rm $tmp_conf
  else
    echo Reloading configuration
    mv $tmp_conf $nginx_conf && nginx -s reload
  fi
  sleep 60
done
