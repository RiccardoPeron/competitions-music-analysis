import json
import numpy as np

metrics = [
    "duration",
    "effective_duration",
    "dynamicComplexity",
    "loudness",
    "intensity",
    "\hline",
    "bpm",
    "bpm_loudness",
    "danceability",
    "\hline",
    "key",
    "chordsChangesRate",
    "inharmonicity",
    "dissonance",
    "chordsNumber",
]


def fill_schema(fname, y):  # index, years, mean
    f = open(fname)
    data = json.load(f)

    years = []
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
            "chordsNumber": [],
        },
    }
    i = 0

    for category in ["time", "tempo", "tonal"]:
        for element in schema[category]:
            for album in data:
                tmp_arr = []
                for song in album["songs"]:
                    val = song[category][element]
                    if y == "mean":
                        tmp_arr.append(val)
                    else:
                        schema[category][element].append(val)

                if y == "mean" and tmp_arr != []:
                    if type(tmp_arr[0]) == type(0) or type(tmp_arr[0]) == type(0.1):
                        mean = float("{:.2f}".format(np.mean(tmp_arr)))
                        schema[category][element].append(mean)

    for album in data:
        for song in album["songs"]:
            if y == "years" or y == "mean":
                years.append(album["year"])
            if y == "index":
                years.append(i)
                i += 1
    if y == "mean":
        years = list(set(years))

    return schema, years
