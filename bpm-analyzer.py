import json
import os
import warnings

import essentia.standard as es
import eyed3
import librosa
import plotly.graph_objects as go
from tqdm import tqdm

# uncomment to disable warnings
# warnings.filterwarnings('ignore')


class SetEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def get_metadata(song, i):
    try:
        metadata = eyed3.load(song)
        title = metadata.tag.title
        title = title.replace('/', '')
        authors = metadata.tag.artist
        authors = authors.split('/')
        track_num = metadata.tag.track_num[0]
        duration = metadata.info.time_secs
    except:
        title = song.split('/')[-1][:-4]
        authors = ['yt']
        track_num = i
        duration = 0
    return title, authors, track_num, duration


def preprocess_metadata():
    movies = []
    n_song = 0
    for folder in os.listdir('OST'):
        for song in os.listdir('OST/' + folder):
            if song != '.spotdl-cache':
                n_song += 1

    pbar = tqdm(total=n_song, unit='file',
                bar_format="Preprocessing metadata:\t{percentage:.0f}%|{bar:100}{r_bar}")
    for folder in sorted(os.listdir('OST')):
        songs = []
        for i, song in enumerate(sorted(os.listdir('OST/' + folder))):
            if song != '.spotdl-cache':
                song = 'OST/' + folder + '/' + song
                title, authors, track_num, duration = get_metadata(song, i)

                songs.append({
                    "title": title,
                    "authors": authors,
                    "duration": duration,
                    "track_num": track_num,
                })
                pbar.update(1)
        songs.sort(key=lambda x: x['track_num'], reverse=False)
        movie = folder.split('-', 1)
        movie = movie[1].replace('_', ' ').strip()
        movies.append({
            "title": movie,
            "songs_number": len(songs),
            "songs": songs
        })
    fname = 'songs.json'
    with open(fname, 'w') as outfile:
        json.dump(movies, outfile)
    return movies


def get_wav_path(song, movie, i):
    if i+1 < 10:
        movie_title = '0' + str(i+1)
    else:
        movie_title = str(i+1)
    movie_title += ' - ' + movie['title'].replace(' ', '_')

    if song['track_num'] < 10:
        track_num = '0' + str(song['track_num'])
    else:
        track_num = str(song['track_num'])

    return 'OST_wav/' + movie_title + '/' + track_num + '-' + song['title'] + '.wav'


def preprocess_bpm(movies_dict, tool):
    n_song = 0
    for movie in movies_dict:
        n_song += len(movie['songs'])
    pbar = tqdm(total=n_song, unit='files',
                bar_format="Preprocessing bpm:\t{percentage:.0f}%|{bar:100}{r_bar}")

    for i, movie in enumerate(movies_dict):
        for song in movie['songs']:
            wav_song = get_wav_path(song, movie, i)
            pbar.set_postfix({'song': song['title'][:20]})
            bpm, bpm_60 = extract(wav_song, tool)

            song['bpm'] = bpm
            song['bpm_60'] = bpm_60

            pbar.update(1)

    fname = 'songs_' + tool + '.json'
    with open(fname, 'w') as outfile:
        json.dump(movies_dict, outfile)

    return movies_dict


def extract(song, tool):
    # retrieve song BPM with essentia
    if tool == 'essentia':
        loader = es.MonoLoader(filename=song)
        audio = loader()
        rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
        bpm, beats, beats_confidence, _, beats_intervals = rhythm_extractor(
            audio)
        bpm_60, beats, beats_confidence, _, beats_intervals = rhythm_extractor(
            audio[:60 * 44100])

        return bpm, bpm_60
    # retrieve song BPM with librosa
    elif tool == 'librosa':
        y, sr = librosa.load(song, res_type='kaiser_fast')
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
        y, sr = librosa.load(song, res_type='kaiser_fast', duration=60)
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo_60 = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
        return tempo[0], tempo_60[0]


def plot_bpm(fname):
    f = open(fname)
    data = json.load(f)

    x = []
    y = []
    y_60 = []

    for movie in data:
        for song in movie['songs']:
            x.append(song['title'])
            y.append(song['bpm'])
            y_60.append(song['bpm_60'])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='full song'))
    fig.add_trace(
        go.Scatter(x=x,
                   y=y_60,
                   mode='lines+markers',
                   name='first 60 seconds'))

    fig.update_layout(title='Songs BPMs',
                      xaxis_title='song title',
                      yaxis_title='BPMs')

    fig.show()


def plot_average_bpm(fname):
    f = open()
    data = json.load(f)

    x = []
    y = []
    y_60 = []

    for movie in data:
        tmpy = []
        tmpy_60 = []
        for song in movie['songs']:
            tmpy.append(song['bpm'])
            tmpy_60.append(song['bpm_60'])
        x.append(movie['title'])
        y.append(sum(tmpy) / len(tmpy))
        y_60.append(sum(tmpy_60) / len(tmpy_60))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='full song'))
    fig.add_trace(
        go.Scatter(x=x, y=y_60, mode='lines+markers', name='first 60 seconds'))

    fig.update_layout(title='Movie average BPMs',
                      xaxis_title='song title',
                      yaxis_title='BPMs')

    fig.show()


def compare_movies_bpm(fname):
    f = open(fname)
    data = json.load(f)
    fig = go.Figure()
    fig.update_layout(title='Movie BPM comparison',
                      xaxis_title='song number',
                      yaxis_title='BPM')

    for movie in data:
        song_n = []
        song_bpm = []
        for i, song in enumerate(movie['songs']):
            song_n.append(i)
            song_bpm.append(song['bpm'])
        fig.add_trace(go.Scatter(x=song_n, y=song_bpm,
                      mode='lines', name=movie['title']))

    fig.show()


# tool = 'librosa'
# dataset = preprocess_metadata()
# preprocess_bpm(dataset, 'librosa')
fname = 'songs_librosa.json'
compare_movies_bpm(fname)
# plot_average_bpm(fname)
# plot_bpm(fname)
