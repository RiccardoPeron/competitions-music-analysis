import os
from moviepy.editor import *
from tqdm import tqdm

for folder in tqdm(sorted(os.listdir('OST')), ncols=100):
    for song in sorted(os.listdir('OST/' + folder)):
        if song != '.spotdl-cache':
            if song[-4:] == '.mp4':
                video = AudioFileClip(os.path.join('OST', folder, song))
                video.write_audiofile(
                    os.path.join('OST', folder, (song[:-4] + '.mp3')))
