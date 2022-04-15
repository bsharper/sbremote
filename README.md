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

## Configuration

### What gets skipped?

There are a few categories SponsorBlock tracks. They are filler, interaction, intro, music_offtopic, outro, poi_highlight, preview, selfpromo and sponsor. This program by default will skip:

`skip_types = ["sponsor", "selfpromo", "intro", "outro"]`

This is defined in the `sb_remote.py` file. If you edit the line where `skip_types` is defined, you can add or remove types of skips.

Please note that the process of identifying a video and getting the list of skips from the SponsorBlock API can take a few seconds, so the intro doesn't always get skipped. The reason it takes a few seconds is that the YouTube app on the Apple TV only provides the channel name and video title, meaning we have to search for the video ID. So there are 2 lookups whenever a new video is discovered:

1. Find the video ID from YouTube [using youtube-search-python](https://github.com/alexmercerind/youtube-search-python)
2. Get the list of skips from SponsorBlock API [using sponsorblock.py](https://github.com/wasi-master/sponsorblock.py)

Entries are added to a cache. The SponsorBlock data is considered "fresh" for 12 hours, meaning after 12 hours we will request a new update from SponsorBlock. This helps when a new video comes out and doesn't have an entry yet. However, the first lookup (to find the video ID) isn't performed if the channel name and video title haven't changed.

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