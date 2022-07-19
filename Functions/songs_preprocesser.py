import json
import os
import warnings
from typing import Counter

import essentia.standard as es
import eyed3
import librosa
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from tqdm import tqdm

from Functions import extractor
from Functions import tensorflow_extractor as tfextractor

# uncomment to disable warnings
warnings.filterwarnings("ignore")
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def get_metadata(song, i, usetrackn):
    try:
        metadata = eyed3.load(song)
        title = metadata.tag.title
        title = title.replace("/", "")
        authors = metadata.tag.artist
        authors = authors.split("/")
        track_num = metadata.tag.track_num[0]
        duration = metadata.info.time_secs
    except:
        title = song.split("/")[-1][:-4]
        authors = ["yt"]
        duration = 0
    if not usetrackn:
        track_num = i
    return title, authors, track_num, duration


def get_wav_path(song, album, i, source):
    if i + 1 < 10:
        album_title = "0" + str(i + 1)
    else:
        album_title = str(i + 1)
    album_title += " - " + album["title"].replace(" ", "_")

    if song["track_num"] < 10:
        track_num = "0" + str(song["track_num"])
    else:
        track_num = str(song["track_num"])

    return (
        source + "_wav/" + album_title + "/" + track_num + "-" + song["title"] + ".wav"
    )


def preprocess_metadata(source, usetrackn=True):
    albums = []
    n_song = 0
    if source == "Music/Sanremo":
        base_year = 1951
    elif source == "Music/ESC":
        base_year = 1956
    elif source == "Music/OST":
        base_year = 1937

    for folder in os.listdir(source):
        for song in os.listdir(source + "/" + folder):
            if song != ".spotdl-cache":
                n_song += 1

    pbar = tqdm(
        total=n_song,
        unit="file",
        bar_format="Preprocessing metadata:\t{percentage:.0f}%|{bar:100}{r_bar}",
    )
    for j, folder in enumerate(sorted(os.listdir(source))):
        songs = []
        for i, song in enumerate(sorted(os.listdir(source + "/" + folder))):
            if song != ".spotdl-cache":
                song = source + "/" + folder + "/" + song
                title, authors, track_num, duration = get_metadata(song, i, usetrackn)

                songs.append(
                    {
                        "title": title,
                        "authors": authors,
                        "duration": duration,
                        "track_num": track_num,
                    }
                )
                pbar.update(1)

        songs.sort(key=lambda x: x["track_num"], reverse=False)
        try:
            album = folder.split("-", 1)
            album = album[1].replace("_", " ").strip()
        except:
            album = folder.strip()
        albums.append(
            {
                "title": album,
                "songs_number": len(songs),
                "year": j + base_year,
                "songs": songs,
            }
        )
    fname = "Results/" + source.split("/")[1] + "_songs.json"
    with open(fname, "w") as outfile:
        json.dump(albums, outfile)
    return albums


def preprocess_es_features(albums_dict, fname, source, features):
    n_song = 0

    for album in albums_dict:
        n_song += len(album["songs"])
    pbar = tqdm(
        total=n_song,
        unit="files",
        bar_format="Preprocessing features:\t{percentage:.0f}%|{bar:100}{r_bar}",
    )
    for i, album in enumerate(albums_dict):
        for song in album["songs"]:
            pbar.set_postfix({"song": song["title"][:20]})

            wav_song = get_wav_path(song, album, i, source)
            audio = es.MonoLoader(filename=wav_song)()
            if "time" in features:
                song["time"] = extractor.compute_time(audio)
            if "tempo" in features:
                song["tempo"] = extractor.compute_tempo(audio)
            if "tonal" in features:
                song["tonal"] = extractor.compute_tonal(wav_song)
            if "high_level" in features:
                song["high_level"] = tfextractor.get_multiple_models_results(
                    wav_song, tfextractor.all_models()
                )

            pbar.update(1)

    with open(fname, "w") as outfile:
        json.dump(albums_dict, outfile)

    return albums_dict, fname


def extract(song, tool):
    # retrieve song BPM with essentia
    if tool == "essentia":
        # es_song = es.MonoLoader(filename=song)()
        # global_bpm, local_bpm, local_probs = es.TempoCNN(
        #     graphFilename='utilities/deeptemp-k16-3.pb')(es_song)

        loader = es.MonoLoader(filename=song)
        audio = loader()
        rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
        bpm, beats, beats_confidence, _, beats_intervals = rhythm_extractor(audio)
        bpm_60, beats, beats_confidence, _, beats_intervals = rhythm_extractor(
            audio[: 60 * 44100]
        )

        return int(bpm), int(bpm_60)
    # retrieve song BPM with librosa
    elif tool == "librosa":
        y, sr = librosa.load(song, res_type="kaiser_fast")
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
        y, sr = librosa.load(song, res_type="kaiser_fast", duration=60)
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo_60 = librosa.beat.tempo(onset_envelope=onset_env, sr=sr)
        return int(tempo[0]), int(tempo_60[0])


def plot_bpm(fname):
    f = open(fname)
    data = json.load(f)

    x = []
    y = []
    y_60 = []

    for album in data:
        for song in album["songs"]:
            if song["title"] not in x:
                x.append(song["title"])
            else:
                x.append(
                    song["title"]
                    + "_"
                    + str(
                        x.count(song["title"])
                        + sum(
                            [
                                x.count(song["title"] + "_" + str(y))
                                for y in [1, 2, 3, 4, 5, 6, 7, 8, 9]
                            ]
                        )
                    )
                )
            y.append(song["bpm"])
            y_60.append(song["bpm_60"])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", name="full song"))
    fig.add_trace(
        go.Scatter(x=x, y=y_60, mode="lines+markers", name="first 60 seconds")
    )

    fig.update_layout(title="Songs BPMs", xaxis_title="song title", yaxis_title="BPMs")
    print(len(x), len(set(x)))
    fig.show()


def plot_average_bpm(fname):
    f = open(fname)
    data = json.load(f)

    x = []
    y = []
    y_60 = []

    for album in data:
        tmpy = []
        tmpy_60 = []
        for song in album["songs"]:
            tmpy.append(song["bpm"])
            tmpy_60.append(song["bpm_60"])
        x.append(album["title"])
        y.append(sum(tmpy) / len(tmpy))
        y_60.append(sum(tmpy_60) / len(tmpy_60))

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines+markers", name="full song"))
    fig.add_trace(
        go.Scatter(x=x, y=y_60, mode="lines+markers", name="first 60 seconds")
    )

    fig.update_layout(
        title="album average BPMs", xaxis_title="song title", yaxis_title="BPMs"
    )

    fig.show()


def compare_albums_bpm(fname, field):
    f = open(fname)
    data = json.load(f)
    fig = go.Figure()
    fig.update_layout(
        title="album " + field + " comparison",
        xaxis_title="song number",
        yaxis_title="BPM",
    )

    for album in data:
        song_n = []
        song_bpm = []
        for i, song in enumerate(album["songs"]):
            song_n.append(i)
            song_bpm.append(song[field])

        k = 100 // len(song_n)
        song_n = [i * k for i in range(len(song_n))]

        fig.add_trace(
            go.Scatter(x=song_n, y=song_bpm, mode="lines", name=album["title"])
        )

    fig.show()


def plot_keys(fname):
    f = open(fname)
    data = json.load(f)

    k = []
    maj_min = []

    for album in data:
        for song in album["songs"]:
            k.append(song["key"])
            if "major" in song["key"]:
                maj_min.append("major")
            else:
                maj_min.append("minor")

    k = Counter(k)
    maj_min = Counter(maj_min)

    fig = make_subplots(
        rows=1, cols=2, specs=[[{"type": "domain"}, {"type": "domain"}]]
    )
    fig.add_trace(go.Pie(labels=list(k.keys()), values=list(k.values())), 1, 1)
    fig.add_trace(
        go.Pie(labels=list(maj_min.keys()), values=list(maj_min.values())), 1, 2
    )

    fig.update_traces(hole=0.4, hoverinfo="label+percent+name")
    fig.update_layout(
        title_text="Songs keys",
        # Add annotations in the center of the donut pies.
        annotations=[
            dict(text="Key distribucion", x=0.18, y=0.5, font_size=20, showarrow=False),
            dict(text="Major/Minor", x=0.82, y=0.5, font_size=20, showarrow=False),
        ],
    )

    fig.show()


# tool = 'librosa'
# source = "Music/ESC"
# fname = "Results/ESC_essentia.json"
# dataset = json.load(open("Results/ESC_essentia.json"))
# dataset = preprocess_metadata(source, usetrackn=False)
# dataset, fname = preprocess_bpm(dataset, 'librosa', source)
# dataset = preprocess_key(dataset, fname)
# dataset = preprocess_es_features(dataset, fname, source, features=["high_level"])

# compare_albums_bpm(fname, 'bpm')
# plot_average_bpm(fname)
# plot_bpm(fname)
# plot_keys(fname)
