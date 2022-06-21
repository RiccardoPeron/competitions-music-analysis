from spotdl import __main__ as spotdl
import json
import os
import subprocess
import sys
from pathlib import Path
import youtube_dl

print("import spotdl...")

ydl_opts_download = {
    "format": "bestaudio/best",
    "cachedir": False,
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
}


def download_single_yt(url_list):
    skipped = []
    for i in range(len(url_list)):
        try:
            with youtube_dl.YoutubeDL(ydl_opts_download) as ydl:
                ydl.download([url_list[i]])
        except:
            skipped.append(url_list[i])
    if skipped == []:
        return 0
    else:
        download_single_yt(skipped)


def ytdownload(link):
    with youtube_dl.YoutubeDL(
        {
            "outtmpl": "%(id)s%(ext)s",
            "quiet": True,
        }
    ) as ydl:
        result = ydl.extract_info(link, download=False)
        if "entries" in result:
            # Can be a playlist or a list of videos
            video = result["entries"]
        playlist_urls = [
            result["entries"][i]["webpage_url"] for i, item in enumerate(video)
        ]

    download_single_yt(playlist_urls)
    print("-" * 15)


def download(title, link, out_folder, i):
    print("downloading ", title, " OTS")
    os.chdir("./" + out_folder)
    fname = ""
    if i < 10:
        fname = "0" + str(i) + " - " + title
    else:
        fname = str(i) + " - " + title
    os.mkdir(fname)
    os.chdir("./" + fname)
    # subprocess.check_call(["spotdl", link, "--output-format wav"])
    ytdownload(link)
    os.chdir("..")
    os.chdir("..")


def download_all(json_source, out_folder):
    print("open file...")
    file = open(json_source)
    movies = json.load(file)

    print("creating main folder...")
    ost = Path(out_folder)
    if not ost.exists():
        ost.mkdir()

    for i, movie in enumerate(movies):
        link = movie["link"].replace(" ", "_")
        title = movie["title"].replace(" ", "_")
        download(title, link, out_folder, i + 1)

    print("--- DONE ---")


# download_all("ESC.json", "ESC")
