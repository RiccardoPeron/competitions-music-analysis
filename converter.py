import os
from moviepy.editor import *
from tqdm import tqdm
from pathlib import Path
from pydub import AudioSegment
import eyed3

# create the main folder
ost = Path('OST_wav')
if not ost.exists():
    ost.mkdir()

# iterate through the movies
pbar = tqdm(sorted(os.listdir('OST')), desc='converting: ', ncols=100)
for folder in pbar:
    # create the movie folder in the main folder
    if not Path('OST_wav/' + folder).exists():
        Path('OST_wav/' + folder).mkdir()

    # iterate through the songs
    for i, song in enumerate(sorted(os.listdir('OST/' + folder))):
        if song != '.spotdl-cache':
            # convert mp4 song
            if song[-4:] == '.mp4':
                video = AudioFileClip(os.path.join('OST', folder, song))
                video.write_audiofile(
                    os.path.join('OST_wav', folder, (song[:-4] + '.wav')))
            # convert mp3 song
            if song[-4:] == '.mp3':
                # extract metadata
                metadata = eyed3.load(os.path.join('OST', folder, song))
                try:
                    title = metadata.tag.title
                    title = title.replace('/', '')
                    track_n = metadata.tag.track_num[0]
                except:
                    title = song[:-4]
                    track_n = i
                # set all the track numbers in a NN format
                if track_n < 10:
                    track_n = '0'+str(track_n)
                else:
                    track_n = str(track_n)

                # convert into wav
                pbar.set_postfix(f"| {title}")
                sound = AudioSegment.from_mp3(
                    os.path.join('OST', folder, song))
                sound.export(os.path.join(
                    'OST_wav', folder, (track_n + '-' + title + '.wav')), format='wav')
