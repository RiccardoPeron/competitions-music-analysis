from statistics import mean
import numpy as np
import json
import pandas as pd
from tqdm import tqdm

schema = {
    "time": {
        "duration": [],
        "effective_duration": [],
        "dynamicComplexity": [],
        "loudness": [],
        "intensity": [],
    },
    "tempo": {"bpm": [], "bpm_loudness": [], "danceability": []},
    "tonal": {
        "key": [],
        "chordsChangesRate": [],
        "inharmonicity": [],
        "dissonance": [],
    },
}

years = []


def get_coefficent(fname, metric):
    f = open(fname)
    data = json.load(f)

    x = []
    y = []

    for album in data:
        # m = []
        for song in album["songs"]:
            y.append(song[metric])
        # x.append(mean(m))
        x.append(album["year"])

    coeff = np.corrcoef(x, y)
    return coeff[0][1]


def get_csv_coefficent(fname, csv):
    f = open(fname)
    data = json.load(f)

    df = pd.read_csv(csv, header=0)
    index = list(df.columns)
    tracks = index[0]

    years = []
    titles_split = []

    for track in df[tracks]:
        t = track.split("-")[2:]
        t[len(t) - 1] = t[len(t) - 1][:-12]
        t = "-".join(t)
        titles_split.append(t)

    for album in data:
        for song in album["songs"]:
            s = song["title"]
            n = titles_split.count(s)
            if n > 3:
                print("n: ", n)
            for i in range(n):
                years.append(album["year"])

    if len(df[tracks]) != len(years):
        print("emmosoncazzi", len(years), len(df[tracks]))

    for id in tqdm(index):
        if id != tracks and "stdev" not in id:
            x = [track for track in df[id]]
            if not all(v == 0 for v in x):
                print(id, "\t|\t", np.corrcoef(x, years)[0][1])


def fill_schema(fname):
    f = open(fname)
    data = json.load(f)

    for album in data:
        for song in album["songs"]:
            years.append(album["year"])
            for category in ["time", "tempo", "tonal"]:
                for element in song[category]:
                    val = song[category][element]
                    schema[category][element].append(val)

    return schema


def get_all_coeff(fname):
    song_schema = fill_schema(fname)
    for category in ["time", "tempo", "tonal"]:
        for element in schema[category]:
            try:
                metric = schema[category][element]
                coeff = np.corrcoef(metric, years)
                print(f"| {element}\t\t|\t{coeff[0][1]} |")
            except:
                print(f"| {element}\t\t|\tTOFIX |")
    return 0


get_all_coeff("Results/ESC_essentia.json")
# get_csv_coefficent("JSON/ESCsongs.json", "OST_results/results.csv")
