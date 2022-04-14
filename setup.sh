#!/bin/bash

if [[ -d env ]]; then
	source env/bin/activate
fi

echo "Checking dependencies..."
python -c "import pyatv, yaspin, inquirer, sponsorblock, youtubesearchpython; print ('Import test successful')"
rv=$?

if [[ $rv == 0 ]]; then
	echo "Everything looks ok, try running \"./runme.sh\""
	exit
fi

echo "Import test failed, attempting to install dependencies"
if [[ ! -d env ]]; then
	python -m venv env
	source env/bin/activate
fi

pip install -r requirements.txt

echo "Try running this script again. If you don't see any errors, try \"./runme.sh\""



