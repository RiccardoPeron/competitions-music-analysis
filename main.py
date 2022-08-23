from sklearn.inspection import plot_partial_dependence
from Functions import downloader, converter, songs_preprocesser, evaluator, plot
import json

# EDIT HERE TO CHANGE FOLDERS AND TOOLS
tool = "essentia"
competition = "ESC"
# -------------------------------------

source = "Music/" + competition
# dataset = json.load(open('JSON/Sanremosongs.json'))
fname = "Results/" + competition + "songs_" + tool + ".json"
dataset = json.load(open(fname))
tracknum = False

if __name__ == "__main__":
    print("-" * 10)
    print("Folder:\t" + source)
    print("Tool:\t" + tool)
    print("-" * 10)

    print("Downloading...")
    downloader.download_all(source + ".json", source)

    print("Converting...")
    converter.convert(source, usetrackn=tracknum)

    print("Processing metadata...")
    dataset = songs_preprocesser.preprocess_metadata(source, usetrackn=tracknum)

    print("Processing features...")
    dataset, fname = songs_preprocesser.preprocess_es_features(
        dataset, fname, source, ["time", "tempo", "tonal"]
    )

    dataset, fname = songs_preprocesser.tmp(dataset, fname, source)

    print(evaluator.make_latex_table(fname))

    for opt in ["years", "index", "mean"]:
        print(plot.plot_all(fname, source, opt))

    plot.plot_keys(fname)
    plot.plot_keys_pie(fname)

    # EXPERIMENTAL SHOULD WORK BUT NOT TESTED

    # print("processing gpu features...")
    # dataset, fname = songs_preprocesser.preprocess_es_features(
    #     dataset, fname, source, ["high_level"]
    # )
