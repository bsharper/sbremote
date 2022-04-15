# SBRemote for YouTube on Apple TV

Use SponsorBlock with YouTube on Apple TV 

## Introduction

This is a program that runs in the background on a computer. After pairing with an Apple TV, it will ask the Apple TV what is being played on YouTube. If the video being played has an entry in the SponsorBlock database, it will attempt to skip those sections. 

## Requirements

You should just need a computer with Python 3 installed. The support libraries are listed in `requirements.txt`

## Usage

1. Clone this repository `git clone https://github.com/bsharper/sbremote`
2. Run `./setup.sh`. This will create a venv environment in the current directory and install required libraries.
3. Run `./runme.sh`. This will start the program and allow you to pair with an Apple TV. Leave this program running in the background.

## Troubleshooting

### A literal bug

I found this bug on Raspbian 10. If you get an error that looks like this:

`ImportError: cannot import name 'Literal' from 'typing' (/usr/lib/python3.7/typing.py)`

It means you are running an older version of Python 3 (older than 3.8). You can update Python to 3.8 or higher, or make the following change to fix the issue. Edit the `env/lib/python3.7/site-packages/sponsorblock/utils.py` file using `vi` or `nano` or `emacs` or `ed` or a [whatever editor you use](https://imgs.xkcd.com/comics/real_programmers.png).

`nano env/lib/python3.7/site-packages/sponsorblock/utils.py`

Then look for the line at the top that looks like:

````
from typing import Dict, Literal
````

And change that to 2 lines:

````
from typing import Dict
from typing_extensions import Literal
````

Then retry setup. 