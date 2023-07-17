# SBRemote for YouTube on Apple TV (Docker)

Use SponsorBlock with YouTube on Apple TV (Docker)

## Introduction

This is a program by `https://github.com/bsharper/sbremote` optimized by me for Docker. After pairing with an Apple TV, it will ask the Apple TV what is being played on YouTube. If the video being played has an entry in the SponsorBlock database, it will attempt to skip those sections. 

## Requirements

You should just need a local home server (standalone instance or linux-base router) with Docker and Python 3 installed. The support libraries are listed in `requirements.txt`

## Usage

1. Clone this repository `git clone https://github.com/bsharper/sbremote`
2. Run `cd sbremote`
2. Run `docker volume create sbremote_data`. This will create a volume for config file.
3. Run `docker build -t sbremote .`. This will build sbremote image.
4. Run `docker run --rm -it --network=host -v sbremote_data:/data sbremote --setup`. This will start setup container. Follow all the steps. If everything is successful, the configuration file will be saved to the sbremote_data. Setup container will remove automatically. 
5. Run `sudo docker run -d --name SBRemote --restart=unless-stopped --network=host -v sbremote_data:/data sbremote --run`. This will start Sponsorblock service with your config in sbremote_data volume.
6. That's all! After sometime service will be alive. You can watch logs by `docker logs SBRemote` and report issues for some bugs. 

## Limitations

Currently, one device for one service instance is supported.

## Plans

Provide support for multiple devices with a single instance of the service.

### What gets skipped?

There are a few categories SponsorBlock tracks. They are filler, interaction, intro, music_offtopic, outro, poi_highlight, preview, selfpromo and sponsor. This program by default will skip:

`skip_types = ["sponsor", "selfpromo", "intro", "outro"]`

This is defined in the `sb_remote.py` file. If you edit the line where `skip_types` is defined, you can add or remove types of skips.

Please note that the process of identifying a video and getting the list of skips from the SponsorBlock API can take a few seconds, so the intro doesn't always get skipped. The reason it takes a few seconds is that the YouTube app on the Apple TV only provides the channel name and video title, meaning we have to search for the video ID. So there are 2 lookups whenever a new video is discovered:

1. Find the video ID from YouTube [using youtube-search-python](https://github.com/alexmercerind/youtube-search-python)
2. Get the list of skips from SponsorBlock API [using sponsorblock.py](https://github.com/wasi-master/sponsorblock.py)

Entries are added to a cache. The SponsorBlock data is considered "fresh" for 12 hours, meaning after 12 hours we will request a new update from SponsorBlock. This helps when a new video comes out and doesn't have an entry yet. However, the first lookup (to find the video ID) isn't performed if the channel name and video title haven't changed.
