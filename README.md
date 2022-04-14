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
