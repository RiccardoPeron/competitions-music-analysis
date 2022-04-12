import json
import os

import essentia
import essentia.standard as es
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from tqdm import tqdm


class SetEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def get_authors_and_title(song):
    authors_title = song.split('-')
    title = ' '.join(authors_title[1:])
    title = title[:-4].strip()
    authors = authors_title[0].split(',')
    authors = [author.strip() for author in authors]
    return authors, title


def preprocess():
    movies = []
    songs_set = []
    for folder in tqdm(sorted(os.listdir('OST')), ncols=100):
        songs = []
        for song in sorted(os.listdir('OST/' + folder)):
            if song != '.spotdl-cache':
                try:
                    authors, title = get_authors_and_title(song)
                except:
                    authors = 'yt'
                    title = song
                song = 'OST/' + folder + '/' + song
                bpm, bpm_60 = extract(song)
                songs_set.append(title)
                if title in songs_set and songs_set.count(title) > 1:
                    title = title + str(songs_set.count(title) - 1)
                songs.append({
                    "title": title,
                    "authors": authors,
                    "bpm": int(bpm),
                    "bpm_60": int(bpm_60)
                })
        movie = folder.split('-')
        movie = movie[1].replace('_', ' ').strip()
        movies.append({
            "title": movie,
            "songs_number": len(songs),
            "songs": songs
        })
    with open('songs.json', 'w') as outfile:
        json.dump(movies, outfile)
    return movies


def extract(song):
    loader = es.MonoLoader(filename=song)
    audio = loader()
    rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
    bpm, beats, beats_confidence, _, beats_intervals = rhythm_extractor(audio)
    bpm_60, beats, beats_confidence, _, beats_intervals = rhythm_extractor(
        audio[:60 * 44100])

    return bpm, bpm_60


def extract_():
    songs = []
    bpms = []
    bpms_60 = []
    movies = []
    bpm_average = []
    bpm_average_60 = []

    for folder in sorted(os.listdir('OST')):
        tmp = []
        tmp_60 = []
        for song in sorted(os.listdir('OST/' + folder)):
            if song != '.spotdl-cache':
                song = 'OST/' + folder + '/' + song
                loader = es.MonoLoader(filename=song)
                audio = loader()
                rhythm_extractor = es.RhythmExtractor2013(
                    method="multifeature")
                bpm = rhythm_extractor(audio)
                bpm_60 = rhythm_extractor(audio[:60 * 44100])

                bpms.append(bpm)
                tmp.append(bpm)
                bpms_60.append(bpm_60)
                tmp.append(bpm_60)
                songs.append(song[:-4])

        movies.append(folder[5:])
        bpm_average.append(sum(tmp) // len(tmp))
        bpm_average_60.append(sum(tmp_60) // len(tmp_60))


def plot_bpm():
    f = open('songs.json')
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
        go.Scatter(x=x[:100],
                   y=y_60[:100],
                   mode='lines+markers',
                   name='first 60 seconds'))

    fig.update_layout(title='Songs BPMs',
                      xaxis_title='song title',
                      yaxis_title='BPMs')

    fig.show()


def plot_average_bpm():
    f = open('songs.json')
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


#preprocess()

plot_average_bpm()
plot_bpm()
