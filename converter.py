import os
from moviepy.editor import *
from tqdm import tqdm
from pathlib import Path
from pydub import AudioSegment
import eyed3


def check(source):
    n_song = 0
    n_wav_song = 0
    for folder in os.listdir(source):
        n_song += len(os.listdir(source + "/" + folder))

    for folder in os.listdir(source + "_wav"):
        n_wav_song += len(os.listdir(source + "_wav/" + folder))

    if n_wav_song != n_song - len(os.listdir(source)):
        print(">>>> WARNING: " + str(n_wav_song) + "is different from " + str(n_song))


def convert(source, usetrackn=True):
    # create the main folder
    ost = Path(source + "_wav")
    if not ost.exists():
        ost.mkdir()

    n_song = 0
    for folder in os.listdir(source):
        n_song += len(os.listdir(source + "/" + folder))
    pbar = tqdm(
        total=n_song,
        unit="files",
        bar_format="Coverting:\t{percentage:.0f}%|{bar:100}{r_bar}",
    )

    # iterate through the movies
    for folder in sorted(os.listdir(source)):
        # create the movie folder in the main folder
        if not Path(source + "_wav/" + folder).exists():
            Path(source + "_wav/" + folder).mkdir()

        # iterate through the songs
        for i, song in enumerate(sorted(os.listdir(source + "/" + folder))):
            if song != ".spotdl-cache":
                # convert mp4 song
                if song[-4:] == ".mp4":
                    video = AudioFileClip(os.path.join(source, folder, song))
                    video.write_audiofile(
                        os.path.join(source + "_wav", folder, (song[:-4] + ".wav"))
                    )
                # convert mp3 song
                if song[-4:] == ".mp3":
                    # extract metadata
                    metadata = eyed3.load(os.path.join(source, folder, song))
                    try:
                        title = metadata.tag.title
                        title = title.replace("/", "")
                        track_n = metadata.tag.track_num[0]
                    except:
                        title = song[:-4]
                    if not usetrackn:
                        track_n = i
                    # set all the track numbers in a NN format
                    if track_n < 10:
                        track_n = "0" + str(track_n)
                    else:
                        track_n = str(track_n)

                    # convert into wav
                    # pbar.set_postfix(f"| {title}")
                    sound = AudioSegment.from_mp3(os.path.join(source, folder, song))
                    sound.export(
                        os.path.join(
                            source + "_wav", folder, (track_n + "-" + title + ".wav")
                        ),
                        format="wav",
                    )

                    pbar.update(1)

    check(source)


# convert('Sanremo')
