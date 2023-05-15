# yt-dlp helper

A simple Python script that helps with using [yt-dlp](https://github.com/yt-dlp/yt-dlp "yt-dlp GitHub").

## Requirements

- Python 3.7+ (following yt-dlp)  
- yt_dlp Python package
- yt-dlp.exe (the standalone binary, which you can find [here](https://github.com/yt-dlp/yt-dlp#release-files))
- ffmpeg.exe

## Usage

### Configuration File

When first starting, the program will ask for the paths to the yt-dlp.exe and ffmpeg.exe files (you must include the file names and extension when giving the path, e.g. `C:\folder\yt-dlp.exe`).

A configuration file `config.ini` will be created at the same directory as the `yt_dlp_helper.py` file. This file contains the paths for yt-dlp.exe and ffmpeg.exe as mentioned above as well as the custom save directory if one has been set (see [File Save Locations](#file-save-locations)). You can edit this manually if you want to change these locations as long as the correct syntax is followed.

### Download Options

Note that although yt-dlp supports multiple websites, this script is only meant for and has only been tested on YouTube.

After inputting the URL, there are three download options available:

- Best Video: This uses the default format selection that yt-dlp uses to download the best available quality which you can see [here](https://github.com/yt-dlp/yt-dlp#format-selection)

- Custom Video: Lists all avaiable formats and allows you to choose the video and audio file that you want to download.

  There are two further options avaiable once you have chosen your files:

  - Merge: This is the --merge-output-format option from yt-dlp as seen [here](https://github.com/yt-dlp/yt-dlp#video-format-options:~:text=%2D%2Dmerge%2Doutput%2Dformat) which can also be found in their [YoutubeDL.py file](https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/YoutubeDL.py), which is in the yt_dlp Python package
  
  - Re-encode: This is the [--recode-video option](https://github.com/yt-dlp/yt-dlp#video-format-options:~:text=else%20to%20mkv-,%2D%2Drecode%2Dvideo,-FORMAT%20%20%20%20%20%20%20%20%20%20%20Re%2Dencode) which does not seem to exist in the yt_dlp Python package (at least at the time of writing). This option is also available for the next download option "Video Or Audio Only"

- Video Or Audio Only: Similar to the "Custom Video" option, but allows you to only choose one file. This would mostly be used for downloading audio-only files from Youtube, but can also be used to download a single video file that may or may not contain audio depending on the format.

### File Save Locations

You can choose to save the file in different locations:

- Current working directory: This saves the file where the script is being run

- yt-dlp.exe directory: This uses the same directory that was given for the yt-dlp.exe binary

- New directory: This is allows you to choose a directory that you may only want to use once. You can also use this option to set a new custom directory, which will overwrite the previous custom directory if it exists.

- Saved directory: If there has not been any custom directory saved yet, you will be asked to set a new one and save at that location. If a custom directory has been set, you can use this option to keep saving files to that custom directory.

## Background

I made this to help with using yt-dlp without commands as I found myself using it from the command line ocassionally to download videos or audio from YouTube. Since I would often forget the commands, I had to take note of them somewhere and refer to them whenever I wanted to use yt-dlp. There *are* other third-party GUIs that are quite good and such as [this](https://github.com/kannagi0303/yt-dlp-gui "yt-dlp-gui by kannagi0303") or [this](https://github.com/oleksis/youtube-dl-gui "youtube-dl-gui by oleksis") that you can find after a quick Google search, but I wanted to try making a simple script that was just enough for what I wanted to do (and also possibly make it for learning/fun). I decided to create a simple PowerShell script at first to help with this, but then added more options as I thought of more use cases. I eventually switched to using Python to handle exceptions as yt-dlp is also written in Python and I am more familiar with it than PowerShell. Still, I decided to keep the PowerShell script in this repository just in case I want to do something with it in the future.
