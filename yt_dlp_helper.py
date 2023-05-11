import yt_dlp
import yt_dlp.utils
import subprocess
import pathlib
import os
import textwrap

YTDLP_LOCATION = "D:/yt-dlp/yt-dlp.exe"
FFMPEG_LOCATION = "D:/yt-dlp/ffmpeg.exe"

REENCODE_FORMATS = (
    "avi",
    "flv",
    "gif",
    "mkv",
    "mov",
    "mp4",
    "webm",
    "aac",
    "aiff",
    "alac",
    "flac",
    "m4a",
    "mka",
    "mp3",
    "ogg",
    "opus",
    "vorbis",
    "wav",
)

MERGE_FORMATS = ("avi", "flv", "mkv", "mov", "mp4", "webm")

REENCODE_FORMAT_DESC = f"Re-encoding supported formats: {', '.join(REENCODE_FORMATS)}"

REENCODE_SYNTAX_DESC = """Re-encoding syntax:
You can specify multiple rules; e.g.
"aac>m4a/mov>mp4/mkv" will remux aac to m4a,
mov to mp4 and anything else to mkv"""

REENCODE_WARNING = """Warning: 
if the target format is not compatible with the
video/audio codec, re-encoding will fail and
the files will be downloaded without re-encoding."""

MERGE_FORMAT_DESC = f"""Merging formats:
Containers that may be used when merging
formats, separated by "/", e.g. "mp4/mkv".
Ignored if no merge is required. (currently
supported: {", ".join(MERGE_FORMATS)})"""

ydl_opts = {"ffmpeg_location": FFMPEG_LOCATION}

url = "https://www.youtube.com/watch?v=BaW_jenozKc"

do_restart = True
while do_restart:
    # url = input("Input URL: ")

    # valid_url = False
    # while not valid_url:
    #     try:

    #         # check if URL is valid without downloading
    #         with yt_dlp.YoutubeDL(dict(ydl_opts, skip_download=True)) as ydl:
    #             ydl.download(url)
    #         valid_url = True

    #     except Exception as e:

    #         if not isinstance(e, yt_dlp.utils.DownloadError):
    #             print(e)

    #         print("Try again.")

    #         url = input("Input URL: ")

    directory_choice = input(textwrap.dedent("""
    Save file(s) in:
     - [1] current directory
     - [2] yt-dlp directory
     : """))
    while directory_choice not in ("1", "2"):
        directory_choice = input("Invalid option. Try again: ")

    if directory_choice == "2":
        directory = pathlib.Path(YTDLP_LOCATION).resolve().parent
        os.chdir(directory)

    option = input(textwrap.dedent("""
    Choose an option:
     - [va] Video (Choose Best Quality Automatically)
     - [vc] Video (Choose Custom Video And Audio Files)
     - [1] Video Or Audio Only (Choose One File)
     : """))
    while option not in ("vc", "va", "1"):
        option = input("Invalid option. Try again: ")

    print()
    
    if option == "va":
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(url)

    else:
        with yt_dlp.YoutubeDL(dict(ydl_opts, listformats=True)) as ydl:
            ydl.download(url)
        print()

        if option == "vc":

            valid_formats = False
            while not valid_formats:
                try:
                    
                    video_format = input("Choose a video format: ")
                    audio_format = input("Choose an audio format: ")

                    format_select = f"{video_format}+{audio_format}"

                    if video_format == audio_format:
                        raise Exception("Both formats are the same, try again.")

                    with yt_dlp.YoutubeDL(
                        dict(ydl_opts, format=format_select, skip_download=True)
                    ) as ydl:
                        ydl.download(url)
                    valid_formats = True

                except Exception as e:
                    if isinstance(e, yt_dlp.utils.DownloadError):
                        print("Try again.")
                    else:
                        print(e)

            print(
                "\nMerge into output format or re-encode into other formats? (proper syntax required)"
            )
            while True:
                output_choice = input("[M] Merge   [R] Re-encode   [N] No   "
                    "[?] Supported Formats And Syntax : "
                )
                if output_choice == "?":
                    print(
                        f"\n{REENCODE_FORMAT_DESC}\n\n{REENCODE_SYNTAX_DESC}\n\n{REENCODE_WARNING}\n"
                        f"\n{MERGE_FORMAT_DESC}\n"
                    )
                elif output_choice in ("m", "r", "n"):
                    break

            if output_choice.lower() == "m":
                merge_format = input("Enter merge formats: ")

                valid_merge = False
                while not valid_merge:
                    try:
                        # skip download first in case merge format is invalid
                        with yt_dlp.YoutubeDL(
                            dict(
                                ydl_opts,
                                format=format_select,
                                merge_output_format=merge_format,
                                skip_download=True,
                            )
                        ) as ydl:
                            ydl.download(url)
                        valid_merge = True

                    except Exception as e:
                        if isinstance(e, yt_dlp.utils.DownloadError):
                            print("Try again.")
                        else:
                            print(e)

                        merge_format = input("Enter merge formats: ")

                with yt_dlp.YoutubeDL(
                    dict(ydl_opts, format=format_select, merge_output_format=merge_format)
                ) as ydl:
                    ydl.download(url)

            elif output_choice.lower() == "r":

                valid_reencode_format = False
                while not valid_reencode_format:
                    
                    reencode_format_complete = input("Enter complete re-encoding rules: ")
                    
                    if [reencode_format_complete] == reencode_format_complete.split("/"):
                        # only one rule specified, e.g. "aac>m4a"
                        if [reencode_format_complete] == reencode_format_complete.split(">"):
                            if reencode_format_complete in REENCODE_FORMATS:
                                valid_reencode_format = True
                            else:
                                print("Unavailable format.")
                        else:
                            reencode_formats = reencode_format_complete.split(">")
                            valid_reencode_format = True
                            for format in reencode_formats:
                                if format not in REENCODE_FORMATS:
                                    valid_reencode_format = False
                                    print("At least one of the formats is unavailable.")
                                    break
                    else:
                        # multiple rules specified, e.g. "aac>m4a/mov>mp4/mkv"
                        reencode_rules = reencode_format_complete.split("/")
                        valid_reencode_format = True
                        for rule in reencode_rules:
                            if valid_reencode_format:
                                rule_formats = rule.split(">")
                                for format in rule_formats:
                                    if format not in REENCODE_FORMATS:
                                        valid_reencode_format = False
                                        print("At least one of the formats is unavailable.")
                                        break
                            else:
                                break

                subprocess.run(
                    f"{YTDLP_LOCATION} -f {format_select} "
                    f"--recode-video {reencode_format_complete} {url}"
                )

            elif output_choice.lower() == "n":
                with yt_dlp.YoutubeDL(dict(ydl_opts, format=format_select)) as ydl:
                    ydl.download(url)

        elif option == "1":
            format_choice = input("Choose a format: ")

            success = False
            while not success:
                try:
                    # check if format is valid without downloading
                    with yt_dlp.YoutubeDL(
                        dict(ydl_opts, format=format_choice, skip_download=True)
                    ) as ydl:
                        ydl.download(url)
                    success = True

                except Exception as e:
                    if not isinstance(e, yt_dlp.utils.DownloadError):
                        print(e)

                    print("Try again.")

                    format_choice = input("Choose a format: ")

            print("\nDo you want to re-encode into another format?")
            while True:
                encode_choice = input("[Y] Yes   [N] No   [?] Supported Formats : ")

                if encode_choice == "?":
                    print(f"\n{REENCODE_FORMAT_DESC}\n\n{REENCODE_WARNING}\n")
                elif encode_choice in ("y", "n"):
                    break

            if encode_choice == "n":
                
                with yt_dlp.YoutubeDL(dict(ydl_opts, format=format_choice)) as ydl:
                    ydl.download(url)

            elif encode_choice == "y":
                
                while True:
                    initial_format = input("Specify original format: ")
                    if initial_format in REENCODE_FORMATS:
                        break
                    else:
                        print("Unavailable format.")
                
                while True:
                    recode_format = input("Specify format to re-encode to: ")
                    if recode_format in REENCODE_FORMATS:
                        break
                    else:
                        print("Unavailable format.")
                
                subprocess.run(
                    f"{YTDLP_LOCATION} -f {format_choice} "
                    f"--recode-video {initial_format}>{recode_format} {url}")

    print()
    while True:    
        restart_choice = input("Continue using yt-dlp? [Y/N] : ")
        if restart_choice.lower() == "y":
            do_restart = True
            break
        elif restart_choice.lower() == "n":
            do_restart = False
            break

    if not do_restart:
        break

input("\nPress enter to close: ")
