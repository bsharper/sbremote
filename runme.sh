#!/bin/bash

if [[ ! -d env ]]; then
	echo "Run \"./setup.sh\" first"
	exit 
fi

source env/bin/activate
python sb_remote.py
