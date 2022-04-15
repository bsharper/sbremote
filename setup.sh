#!/bin/bash

if [[ -d env ]]; then
	source env/bin/activate
fi

echo "Checking python version..."
PYEXE="python"
PV=$($PYEXE -c "import sys; sys.stdout.write(str(sys.version_info.major));")
if [[ "$PV" != "3" ]]; then
	echo 'Calling "python" does not run version 3, testing "python3"'
	PYEXE="python3"
	echo "Testing python3..."
	$PYEXE -c "import sys"
	rv=$?
	if [[ $rv != 0 ]]; then
		echo "Error: could not run $PYEXE. Please install Python 3 to continue"
		exit 1
	fi
fi

echo "Checking dependencies..."
$PYEXE -c "import pyatv, yaspin, inquirer, sponsorblock, youtubesearchpython; print ('Import test successful')"
rv=$?

if [[ $rv == 0 ]]; then
	echo "Everything looks ok, try running \"./runme.sh\""
	exit
fi

echo "Import test failed, attempting to install dependencies"
if [[ ! -d env ]]; then
	$PYEXE -m venv env
	source env/bin/activate
fi

# Switching from $PYEXE to python because venv should be active now
python -m pip install -r requirements.txt
echo "============================================================"
echo "Try running this script again. If you don't see any errors, try \"./runme.sh\""
echo "============================================================"


