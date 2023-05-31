# yt-dlp helper

A simple Python script that helps with using [yt-dlp](https://github.com/yt-dlp/yt-dlp "yt-dlp GitHub").

- [Requirements](#requirements)
- [Download](#download)
  - [Virtual Environment](#virtual-environment)
  - [Installing dependencies using `requirements.txt`](#installing-dependencies-using-requirementstxt)
- [Usage](#usage)
  - [Configuration File](#configuration-file)
  - [Download Options](#download-options)
  - [File Save Locaitons](#file-save-locations)

## Requirements

- Python 3.7+ (following yt-dlp)  
- yt_dlp Python package (you can simply use the [requirements.txt](requirements.txt) file as shown in [this section](#installing-dependencies-using-requirementstxt))
- yt-dlp.exe[^1] (the standalone binary, which you can find [here](https://github.com/yt-dlp/yt-dlp#release-files))
- ffmpeg.exe (you can find the links to some of the builds on the [ffmpeg website](https://www.ffmpeg.org/download.html), or you can get the custom builds for yt-dlp [here](https://github.com/yt-dlp/FFmpeg-Builds))

[^1]: Since the --recode-video option does not seem to be available in the yt_dlp package, the script runs the yt-dlp.exe file instead only when downloading with this specific option as a workaround, which is why the binary is required despite already using the Python package.

## Download

The only files you need to download from this repository are:

- the Python file [yt_dlp_helper.py](yt_dlp_helper.py)
- the pip requirements file [requirements.txt](requirements.txt)

If you would like to run the file directly, you can skip to [this section](#installing-dependencies-using-requirementstxt "Installing Dependencies Using requirements.txt"), but if you would like to edit and/or run the code in a virtual environment, you can go to the [next section](#virtual-environment "Virtual Environment").

### Virtual Environment

To isolate package installations from other projects, you may want to set up a Python virtual environment at your chosen directory by using the following command:

```shell
python -m venv /path/to/new/virtual/environment
```

For example, if you want to the folder to be named "venv": `python -m venv venv`

To run the virtual environment, you can use

```shell
<path to virtual environment>/Scripts/activate
```

e.g. `./venv/Scripts/activate`

Note: On Microsoft Windows, it may be required to enable the Activate.ps1 script by setting the execution policy for the user. You can do this by issuing the following PowerShell command:  

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Installing Dependencies Using `requirements.txt`

You can enter this command in the terminal to install the required packages:

```shell
pip install -r requirements.txt
```

You should then be able to run the `yt_dlp_helper.py` file.

## Usage

### Configuration File

When first starting, the program will ask for the paths to the yt-dlp.exe and ffmpeg.exe files (you must include the file names and extensions when giving the path, e.g. `C:\folder\yt-dlp.exe`).

A configuration file `config.ini` will be created at the same directory as the `yt_dlp_helper.py` file. This file contains the paths for yt-dlp.exe and ffmpeg.exe as mentioned above as well as the custom save directory if one has been set (see [File Save Locations](#file-save-locations)). You can edit this manually if you want to change these locations as long as the correct syntax is followed.

### Download Options

Note that although yt-dlp supports multiple websites, this script is only meant for and has only been tested on YouTube.

After inputting the URL, there are three download options available:

- Best video: This uses the default format selection that yt-dlp uses to download the best available quality which you can see [here](https://github.com/yt-dlp/yt-dlp#format-selection)

- Custom video: Lists all avaiable formats and allows you to choose the video and audio file that you want to download.

  There are two further options avaiable once you have chosen your files:

  - Merge: This is the --merge-output-format option from yt-dlp as seen [here](https://github.com/yt-dlp/yt-dlp#video-format-options:~:text=%2D%2Dmerge%2Doutput%2Dformat) which can also be found in their [YoutubeDL module](https://github.com/yt-dlp/yt-dlp/blob/master/yt_dlp/YoutubeDL.py), in the yt_dlp Python package
  
  - Re-encode: This is the [--recode-video option](https://github.com/yt-dlp/yt-dlp#video-format-options:~:text=else%20to%20mkv-,%2D%2Drecode%2Dvideo,-FORMAT%20%20%20%20%20%20%20%20%20%20%20Re%2Dencode) which does not seem to exist in the yt_dlp Python package[^1] (at least at the time of writing). This option is also available for the next download option, "Video or audio only"

- Video or audio only: Similar to the "Custom Video" option, but allows you to only choose one file. This would mostly be used for downloading audio-only files from Youtube, but can also be used to download a single video file that may or may not contain audio depending on the format.

### File Save Locations

You can choose to save the file in different locations:

- Current working directory: This saves the file where the script is being run

- yt-dlp.exe directory: This uses the same directory that was given for the yt-dlp.exe binary

- New directory: This is allows you to choose a directory that you may only want to use once. You can also use this option to set a new custom directory, which will overwrite the previous custom directory if it exists.

- Saved directory: If there has not been any custom directory saved yet, you will be asked to set a new one and save at that location. If a custom directory has been set, you can use this option to keep saving files to that custom directory.

## Background

I made this to help with using yt-dlp without commands as I found myself using it from the command line ocassionally to download videos or audio from YouTube. Since I would often forget the commands, I had to take note of them somewhere and refer to them whenever I wanted to use yt-dlp. There *are* other third-party GUIs that are quite good and such as [this](https://github.com/kannagi0303/yt-dlp-gui "yt-dlp-gui by kannagi0303") or [this](https://github.com/oleksis/youtube-dl-gui "youtube-dl-gui by oleksis") that you can find after a quick Google search, but I wanted to try making a simple script that was just enough for what I wanted to do (and also possibly make it for learning/fun). I decided to create a simple PowerShell script at first to help with this, but then added more options as I thought of more use cases. I eventually switched to using Python to handle exceptions as yt-dlp is also written in Python and I am more familiar with it than PowerShell. Still, I decided to keep the PowerShell script in this repository just in case I want to do something with it in the future.
