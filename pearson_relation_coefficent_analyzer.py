import numpy as np
import json


def get_coefficent(fname, metric):
    f = open(fname)
    data = json.load(f)

    x = []
    y = []

    for album in data:
        for song in album["songs"]:
            x.append(song[metric])
            y.append(album["year"])

    coeff = np.corrcoef(x, y)
    return coeff
