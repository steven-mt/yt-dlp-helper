from pathlib import Path
from configparser import ConfigParser
import subprocess
import textwrap
import yt_dlp
from yt_dlp.utils import DownloadError


class YtDlpHelper:
    _CFG_FILENAME = "config.ini"

    _BIN_PATH_SECTION = "paths"
    _YTDLP_PATH_KEY = "ytdlp_path"
    _FFMPEG_PATH_KEY = "ffmpeg_path"

    _SAVE_DIR_SECTION = "saved_directory"
    _SAVE_DIR_KEY = "save_dir"

    _REENCODE_FORMATS = {
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
    }

    _MERGE_FORMATS = {"avi", "flv", "mkv", "mov", "mp4", "webm"}

    _REENCODE_FORMAT_DESC = (
        f"Re-encoding supported formats: {', '.join(_REENCODE_FORMATS)}"
    )

    _REENCODE_SYNTAX_DESC = textwrap.dedent(
        """Re-encoding syntax:
        You can specify multiple rules; e.g.
        "aac>m4a/mov>mp4/mkv" will remux aac to m4a,
        mov to mp4 and anything else to mkv"""
    )

    _REENCODE_WARNING = textwrap.dedent(
        """Warning:
        if the target format is not compatible with the
        video/audio codec, re-encoding will fail and
        the files will be downloaded without re-encoding."""
    )

    _MERGE_FORMAT_DESC = textwrap.dedent(
        f"""Merging formats:
        Containers that may be used when merging
        formats, separated by "/", e.g. "mp4/mkv".
        Ignored if no merge is required. (currently
        supported: {", ".join(_MERGE_FORMATS)})"""
    )

    def __init__(self) -> None:
        self.cfg_parser = ConfigParser()
        self.cfg_parser.read(self._CFG_FILENAME)

        self.ytdlp_path = ""
        self.ffmpeg_path = ""

        self.ydl_opts = {}

        self.url = ""

    def get_bin_paths(self):
        try:
            path_cfg = self.cfg_parser[self._BIN_PATH_SECTION]
            self.ytdlp_path = path_cfg[self._YTDLP_PATH_KEY]
            self.ffmpeg_path = path_cfg[self._FFMPEG_PATH_KEY]

        except KeyError:
            print("Path information not found, input paths: ")

            ytdlp_path_input = input("Enter path to yt-dlp.exe: ")
            while not (
                Path(ytdlp_path_input).is_file()
                and Path(ytdlp_path_input).stem == "yt-dlp"
            ):
                ytdlp_path_input = input("Invalid input, try again: ")

            ffmpeg_path_input = input("Enter path to ffmpeg.exe: ")
            while not (
                Path(ffmpeg_path_input).is_file()
                and Path(ffmpeg_path_input).stem == "ffmpeg"
            ):
                ffmpeg_path_input = input("Invalid input, try again: ")

            self.cfg_parser[self._BIN_PATH_SECTION] = {
                self._YTDLP_PATH_KEY: ytdlp_path_input,
                self._FFMPEG_PATH_KEY: ffmpeg_path_input,
            }

            with open(self._CFG_FILENAME, "w") as cfg_file:
                self.cfg_parser.write(cfg_file)

            self.ytdlp_path = ytdlp_path_input
            self.ffmpeg_path = ffmpeg_path_input

        finally:
            self.ydl_opts["ffmpeg_location"] = self.ffmpeg_path

    def get_url(self):
        valid_url = False
        while not valid_url:
            try:
                url = input("Input URL: ")

                # check if URL is valid without downloading
                with yt_dlp.YoutubeDL(dict(self.ydl_opts, skip_download=True)) as ydl:
                    ydl.download(url)

                valid_url = True
                return url

            except DownloadError:
                print("Try again.")

    def get_dir_choice(self):
        dir_choice = input(
            textwrap.dedent(
                """
        Save file(s) in:
        - [1] current working directory
        - [2] yt-dlp.exe directory
        - [3] new directory (choose between one time only or save the directory)
        - [4] saved directory
        : """
            )
        )
        while dir_choice not in {"1", "2", "3", "4"}:
            dir_choice = input("Invalid option. Try again: ")

        if dir_choice == "1":
            save_dir = str(Path.cwd())

        elif dir_choice == "2":
            save_dir = str(Path(self.ytdlp_path).resolve().parent)

        elif dir_choice == "3":
            save_dir = input("Enter custom directory: ")
            while not Path(save_dir).is_dir():
                save_dir = input("Invalid directory. Try again: ")

            save_choice = input(
                "Would you like to save the directory? "
                "\nAny existing saved directory will be overwritten. [Y/N] : "
            )
            while save_choice.lower() not in {"y", "n"}:
                save_choice = input("[Y/N] : ")

            if save_choice.lower() == "y":
                self.save_dir_to_cfg(save_dir)

        elif dir_choice == "4":
            try:
                save_dir = self.cfg_parser[self._SAVE_DIR_SECTION][self._SAVE_DIR_KEY]
            except KeyError:
                save_dir = input("No saved directory found. Enter new directory: ")
                while not Path(save_dir).is_dir():
                    save_dir = input("Invalid directory. Try again: ")

                self.save_dir_to_cfg(save_dir)

        self.ydl_opts[self._BIN_PATH_SECTION] = {"home": save_dir}
        print(f"Saving at: {save_dir}")

    def save_dir_to_cfg(self, save_dir):
        self.cfg_parser[self._SAVE_DIR_SECTION] = {self._SAVE_DIR_KEY: save_dir}

        with open(self._CFG_FILENAME, "w") as cfg_file:
            self.cfg_parser.write(cfg_file)

    def get_download_option(self):
        download_option = input(
            textwrap.dedent(
                """
        Choose an option:
        - [va] Best Video (Choose Best Quality Automatically)
        - [vc] Custom Video (Choose Custom Video And Audio Files)
        - [1] Video Or Audio Only (Choose One File)
        : """
            )
        )
        while download_option not in {"vc", "va", "1"}:
            download_option = input("Invalid option. Try again: ")

        print(end="\n")

        return download_option

    def download_best(self):
        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download(self.url)

    def show_formats(self):
        with yt_dlp.YoutubeDL(dict(self.ydl_opts, listformats=True)) as ydl:
            ydl.download(self.url)

        print(end="\n")

    def get_two_formats(self):
        valid_formats = False
        while not valid_formats:
            try:
                video_format = input("Choose a video format: ")
                audio_format = input("Choose an audio format: ")

                format_select = f"{video_format}+{audio_format}"

                if video_format == audio_format:
                    raise ValueError("Both formats are the same, try again.")

                with yt_dlp.YoutubeDL(
                    dict(self.ydl_opts, format=format_select, skip_download=True)
                ) as ydl:
                    ydl.download(self.url)

                valid_formats = True
                return format_select

            except ValueError as e:
                print(e)
            except DownloadError:
                print("Try again.")

    def get_merge_recode_choice(self):
        print(
            "\nMerge into output format or re-encode into other formats? "
            "(proper syntax required)"
        )
        while True:
            output_choice = input(
                "[M] Merge   [R] Re-encode   [N] No   "
                "[?] Supported Formats And Syntax : "
            )
            if output_choice == "?":
                print(
                    f"\n{self._REENCODE_FORMAT_DESC}\n\n{self._REENCODE_SYNTAX_DESC}\n"
                    f"\n{self._REENCODE_WARNING}\n\n{self._MERGE_FORMAT_DESC}\n"
                )
            elif output_choice.lower() in {"m", "r", "n"}:
                return output_choice

    def get_merge_format(self, format_select):
        valid_merge = False
        while not valid_merge:
            try:
                merge_format = input("Enter merge formats: ")

                # skip download first in case merge format is invalid
                with yt_dlp.YoutubeDL(
                    dict(
                        self.ydl_opts,
                        format=format_select,
                        merge_output_format=merge_format,
                        skip_download=True,
                    )
                ) as ydl:
                    ydl.download(self.url)

                valid_merge = True
                return merge_format

            except DownloadError:
                print("Try again.")

    def download_two_merge(self, format_select, merge_format):
        with yt_dlp.YoutubeDL(
            dict(self.ydl_opts, format=format_select, merge_output_format=merge_format)
        ) as ydl:
            ydl.download(self.url)

    def get_reencode_format(self):
        valid_reencode_format = False
        while not valid_reencode_format:
            reencode_format_complete = input("Enter complete re-encoding rules: ")

            if [reencode_format_complete] == reencode_format_complete.split("/"):
                # only one rule specified, e.g. "aac>m4a"

                if [reencode_format_complete] == reencode_format_complete.split(">"):
                    # single format given without ">" separator, e.g. "m4a"
                    if reencode_format_complete in self._REENCODE_FORMATS:
                        valid_reencode_format = True
                    else:
                        print("Unavailable format.")
                else:
                    reencode_formats = reencode_format_complete.split(">")
                    valid_reencode_format = True
                    for reencode_format in reencode_formats:
                        if reencode_format not in self._REENCODE_FORMATS:
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
                        for rule_format in rule_formats:
                            if rule_format not in self._REENCODE_FORMATS:
                                valid_reencode_format = False
                                print("At least one of the formats is unavailable.")
                                break
                    else:
                        break

        return reencode_format_complete

    def download_format_reencode(self, format_select, reencode_format):
        subprocess.run(
            f"{self.ytdlp_path} -f {format_select} "
            f"--recode-video {reencode_format} {self.url}"
        )

    def download_format_default(self, format_select):
        with yt_dlp.YoutubeDL(dict(self.ydl_opts, format=format_select)) as ydl:
            ydl.download(self.url)

    def get_one_format(self):
        success = False
        while not success:
            try:
                format_choice = input("Choose a format: ")

                # check if format is valid without downloading
                with yt_dlp.YoutubeDL(
                    dict(self.ydl_opts, format=format_choice, skip_download=True)
                ) as ydl:
                    ydl.download(self.url)
                success = True

            except DownloadError:
                print("Try again.")

        return format_choice

    def get_reencode_choice(self):
        print("\nDo you want to re-encode into another format?")
        while True:
            reencode_choice = input("[Y] Yes   [N] No   [?] Supported Formats : ")

            if reencode_choice == "?":
                print(f"\n{self._REENCODE_FORMAT_DESC}\n\n{self._REENCODE_WARNING}\n")
            elif reencode_choice.lower() == "y":
                return True
            elif reencode_choice.lower() == "n":
                return False


def main(helper: YtDlpHelper):
    helper.get_bin_paths()

    helper.url = helper.get_url()

    helper.get_dir_choice()

    download_option = helper.get_download_option()

    if download_option == "va":
        helper.download_best()

    else:
        helper.show_formats()

        if download_option == "vc":
            format_select = helper.get_two_formats()
            output_choice = helper.get_merge_recode_choice()

            if output_choice.lower() == "m":
                merge_format = helper.get_merge_format(format_select)
                helper.download_two_merge(format_select, merge_format)

            elif output_choice.lower() == "r":
                reencode_format = helper.get_reencode_format(format_select)
                helper.download_format_reencode(format_select, reencode_format)

            elif output_choice.lower() == "n":
                helper.download_format_default(format_select)

        elif download_option == "1":
            format_choice = helper.get_one_format()
            do_reencode = helper.get_reencode_choice()

            if do_reencode:
                reencode_format = helper.get_reencode_format()
                helper.download_format_reencode(format_choice, reencode_format)

            else:
                helper.download_format_default(format_choice)


if __name__ == "__main__":
    ytdlphelper = YtDlpHelper()

    do_restart = True
    while do_restart:
        main(ytdlphelper)

        print(end="\n")

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
