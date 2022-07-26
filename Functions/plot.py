import json
from nis import cat
from optparse import TitledHelpFormatter
from os import sched_get_priority_max
from typing import Counter

import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from Functions import json_to_lists as jlist
from collections import Counter


def plot(schema, years, category, title=""):

    fig = go.Figure()
    fig.update_layout(
        title=category + " " + title, xaxis_title="years", yaxis_title="features"
    )

    for element in schema[category]:
        y = schema[category][element]
        fig.add_trace(go.Scatter(x=years, y=y, mode="lines+markers", name=element))

    fig.show()
    return 0


def plot_all(fname, source, opt="mean"):
    schema, years = jlist.fill_schema(
        fname,
        y=opt,
    )
    title = "[" + source + ", " + opt + "]"
    plot(schema, years, "time", title)
    plot(schema, years, "tempo", title)
    plot(schema, years, "tonal", title)


def plot_keys(fname):
    schema, years = jlist.fill_schema(
        fname,
        y="years",
    )

    keys = schema["tonal"]["key"]
    keys_set = list(set(keys))
    years_dict = Counter(years)

    scat = go.Figure()
    data = []
    for key in keys_set:
        index = 0
        x = []
        y = []
        for year in years_dict:
            x.append(year)
            temp_keys = keys[index : index + years_dict[year]]
            y.append(temp_keys.count(key))
            index += years_dict[year] + 1
        scat.add_trace(go.Scatter(name=key, x=x, y=y, mode="lines+markers"))
        data.append(go.Bar(name=key, x=x, y=y))

    fig = go.Figure(data)
    fig.update_layout(title="key statsistics")
    fig.update_layout(barmode="stack")
    fig.show()
    fig.update_layout(barmode="group")
    fig.show()
    scat.show()

    return 0


def plot_keys_pie(fname):
    schema, years = jlist.fill_schema(
        fname,
        y="years",
    )
    keys = schema["tonal"]["key"]
    maj_min = []

    for key in keys:
        if "major" in key:
            maj_min.append("major")
        else:
            maj_min.append("minor")

    k = Counter(keys)
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


def plot_one_feature(schema, years, feature, title=""):
    fig = go.Figure()
    fig.update_layout(
        title=feature + " " + title, xaxis_title="years", yaxis_title="features"
    )

    for category in schema:
        for element in schema[category]:
            if element == feature:
                y = schema[category][element]
                fig.add_trace(
                    go.Scatter(x=years, y=y, mode="lines+markers", name=element)
                )

    fig.show()
    return 0


# EXPERIMENTAL


def plot_multi(feature, opt):

    fig = go.Figure()
    fig.update_layout(
        title=feature + " " + opt, xaxis_title="years", yaxis_title="features"
    )

    for competition in ["ESC", "Sanremo"]:
        fname = "Results/" + competition + "songs_essentia.json"
        schema, years = jlist.fill_schema(fname, opt)
        for category in schema:
            for element in schema[category]:
                if element == feature:
                    y = schema[category][element]
                    fig.add_trace(
                        go.Scatter(x=years, y=y, mode="lines+markers", name=competition)
                    )

    fig.show()


# OLD BELOW


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
