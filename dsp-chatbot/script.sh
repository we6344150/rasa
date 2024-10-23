#!/bin/bash

rasa run --enable-api --cors "*" --debug &

rasa run actions --debug &

# 保持容器运行
exec tail -f /dev/null
# rasa run --port 5005 --enable-api --cors '*' --debug

# rasa run actions --port 5055 --debug
