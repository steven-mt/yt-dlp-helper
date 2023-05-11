# Make sure to have ffmpeg.exe in the same directory as the yt-dlp.exe file,
# as it is required to download separate audio and video files and combine them together.
# This is important for downloading high quality videos from YouTube, as anything better than 720p
# is generally stored as separate audio and video files.

$path_to_ytdlp = "D:\yt-dlp\yt-dlp.exe"

$REENCODE_FORMATS = @"
Currently supported formats: avi, flv,
gif, mkv, mov, mp4, webm, aac, aiff, alac,
flac, m4a, mka, mp3, ogg, opus, vorbis, wav`n
"@
$REENCODE_SYNTAX = @"
You can specify multiple rules; e.g.
"aac>m4a/mov>mp4/mkv" will remux aac to m4a,
mov to mp4 and anything else to mkv
"@
$MERGE_FORMATS = @"
Merging formats:
Containers that may be used when merging
formats, separated by "/", e.g. "mp4/mkv".
Ignored if no merge is required. (currently
supported: avi, flv, mkv, mov, mp4, webm)
"@

$restart = "y"

do {
    $url = Read-Host -Prompt "`nInput URL"

    $Option = Read-Host -Prompt "`nChoose an option:
    - [va] Video (Choose Best Quality Automatically)
    - [vc] Video (Choose Custom Video And Audio Files)
    - [1] Video Or Audio Only (Choose One File)
    "
    while ("vc", "va", "1" -notcontains $Option) {
        $Option = Read-Host -Prompt "Invalid option. Try again"
    }

    $DirectoryChoice = Read-Host -Prompt "`nSave the file(s) in:
    - [1] current directory
    - [2] yt-dlp directory
    "
    while ("1", "2" -notcontains $DirectoryChoice) {
        $DirectoryChoice = Read-Host -Prompt "Invalid option. Try again"
    }

    switch ($DirectoryChoice) {
        "1" {
            $Directory = Get-Location
        }
        "2" {
            $Directory = Split-Path -Path $path_to_ytdlp
            Set-Location -Path $Directory
        }
    }

    Write-Host ""
    if ($Option -eq "va") {
        & $path_to_ytdlp $url
    } 
    elseif ($Option -eq "vc" -OR $Option -eq "1") {
        
        & $path_to_ytdlp -F $url
        Write-Host ""
        
        if ($Option -eq "vc") {
            $videoformat = Read-Host -Prompt "Choose a video format"
            $audioformat = Read-Host -Prompt "Choose an audio format"
            
            Write-Host "`nMerge into output format or re-encode into other formats? (proper syntax required)"
            do {
                $formatchoice = Read-Host -Prompt `
                "[M] Merge   [R] Re-encode   [N] No   [?] Supported Formats And Syntax "
                if ($formatchoice -eq "?") {
                    Write-Host "`n$REENCODE_FORMATS`n`n$REENCODE_SYNTAX`n`n$MERGE_FORMATS`n"
                }
            } while (
                "m", "r", "n" -notcontains $formatchoice
            )

            Write-Host ""
            switch ($formatchoice) {
                "m" {
                    $merge_format = Read-Host -Prompt "Enter merge formats"
                    Write-Host ""
                    & $path_to_ytdlp -f $format $videoformat+$audioformat `
                    --merge-output-format $merge_format $url
                }
                "r" {
                    $recode_format_complete = Read-Host -Prompt "Enter complete re-encoding rules"
                    Write-Host ""
                    & $path_to_ytdlp -f $format $videoformat+$audioformat `
                    --recode-video $recode_format_complete $url
                }
                "n" {
                    & $path_to_ytdlp -f $videoformat+$audioformat $url
                }
            }
        }
        elseif ($Option -eq "1") {
            $format = Read-Host -Prompt "Choose a format"
            
            Write-Host "Do you want to re-encode into another format?"
            do {
                $formatchoice = Read-Host -Prompt "[Y] Yes   [N] No   [?] Supported Formats "
                if ($formatchoice -eq "?") {
                    Write-Host $REENCODE_FORMATS
                }
            } while (
                "y", "n" -notcontains $formatchoice
            )

            switch ($formatchoice) {
                "y" {
                    Write-Host
                    $initial_format = Read-Host -Prompt "Specify original format"
                    $recode_format = Read-Host -Prompt "Specify format to re-encode to"
                    Write-Host
                    & $path_to_ytdlp -f $format --recode-video $initial_format>$recode_format $url
                }
                "n" {
                    & $path_to_ytdlp -f $format $url
                }
            }
        }
    }

    Write-Host "`nThe file(s) are in $Directory."

    Write-Host "`nContinue to use yt-dlp?"
    do {
        $restart = Read-Host "[Y] Yes   [N] No "
    } until (
        "y", "n" -contains $restart
    )
} until ($restart -eq "n")

Write-Host -NoNewLine "`nPress any key to continue..."
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')

# Alternatives:
# cmd /c pause
# timeout /t <number of seconds>