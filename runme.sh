#!/bin/bash

if [[ ! -d appletv.json ]]; then
	echo "Run docker -it first to setup config!!!"
	exit 
fi

source env/bin/activate
python sb_remote.py
