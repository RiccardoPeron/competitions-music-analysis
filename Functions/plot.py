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
            y.append(temp_keys.count(key) * 100 / years_dict[year])
            index += years_dict[year] + 1
        data.append(go.Bar(name=key, x=x, y=y))

    scat_x = []
    scat_y = []

    for year in years_dict:
        scat_x.append(years_dict)
        for key in keys_set:
            temp_keys = set(keys[index : index + years_dict[year]])
            scat_y.append(len(temp_keys))

    scat.add_trace(go.Scatter(name=key, x=scat_x, y=scat_y, mode="lines+markers"))

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
