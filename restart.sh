#!/bin/bash
if [[ ${#1} == 0 ]]; then
    bn=$(basename $0)
    echo "Usage: $bn PID"
    exit
fi
kill $1 &>/dev/null
sleep 0.5
kill -9 $1 &>/dev/null
python sb_remote.py
