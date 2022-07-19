import json

import numpy as np
import pandas as pd
from tqdm import tqdm

import json_to_lists as jlist


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


def get_all_coeff(schema, years):
    coeff_list = []
    for category in ["time", "tempo", "tonal"]:
        for element in schema[category]:
            try:
                metric = schema[category][element]
                coeff = np.corrcoef(metric, years)
                coeff = float("{:.2f}".format(coeff[0][1]))
                coeff_list.append(coeff)
                # print(f"| {element}\t\t\t\t|\t{coeff} |")
            except:
                # print(f"| {element}\t\t\t\t|\tTOFIX |")
                coeff_list.append("TOFIX")
                len(metric) == len(years)
    return coeff_list


def make_latex_table(fname):
    options = ["years", "index", "mean"]
    coeffs = []

    for opt in options:
        schema, years = jlist.fill_schema(
            fname,
            y=opt,
        )
        coeffs.append(get_all_coeff(schema, years))

    table = (
        "\\begin{table}[!ht]\n"
        + "\centering\n"
        + "\\begin{tabular}{@{}lrrr@{}}\n"
        + "\\toprule\n"
        + "{\color[HTML]{333333} \\textbf{Feature}} & {\color[HTML]{333333} \\textbf{Year PRC}} & {\color[HTML]{333333} \\textbf{Song index PRC}} & {\color[HTML]{333333} \\textbf{Year mean PRC}} \\\\ \midrule\n"
    )
    i = 0
    for metric in jlist.metrics:
        if metric == "\hline":
            table += metric + "\n"
        else:
            table += (
                metric
                + "&"
                + str(coeffs[0][i])
                + "&"
                + str(coeffs[1][i])
                + "&"
                + str(coeffs[2][i])
                + "\\\\\n"
            )
            i += 1

    table += (
        "\end{tabular}\n"
        + "\caption{Pearson Relation Coefficent relativo ad ogni metrica}\n"
        + "\label{table:}\n"
        + "\end{table}"
    )

    return table


# schema, years = jlist.fill_schema(
#     "/home/riccardo/Tesi/disney-ost-analysis/Results/Sanremosongs_essentia.json",
#     y="mean",
# )
# get_all_coeff(schema, years)

# get_all_coeff("Results/ESC_essentia.json")
# get_csv_coefficent("JSON/ESCsongs.json", "OST_results/results.csv")

print(
    make_latex_table(
        "/home/riccardo/Tesi/disney-ost-analysis/Results/ESC_essentia.json"
    )
)
