from Functions import downloader, converter, songs_preprocesser
import json

tool = "librosa"
source = "ESC"
# dataset = json.load(open('JSON/Sanremosongs.json'))
fname = "JSON/ESCsongs_" + tool + ".json"
# dataset = json.load(open(fname))
tracknum = False

if __name__ == "__main__":
    print("-" * 10)
    print("Folder:\t" + source)
    print("Tool:\t" + tool)
    print("-" * 10)

    # print('Downloading...')
    # downloader.download_all(source+'.json', source)

    print("Converting...")
    converter.convert(source, usetrackn=tracknum)

    print("Processing metadata...")
    dataset = songs_preprocesser.preprocess_metadata(source, usetrackn=tracknum)

    print("Processing bpm...")
    dataset, fname = songs_preprocesser.preprocess_bpm(dataset, tool, source)

    print("Processing key...")
    dataset = songs_preprocesser.preprocess_key(dataset, fname, source)

    songs_preprocesser.compare_movies_bpm(fname, "bpm")
    print("> created")
    songs_preprocesser.plot_average_bpm(fname)
    print("> created")
    songs_preprocesser.plot_bpm(fname)
    print("> created")
    songs_preprocesser.plot_keys(fname)
    print("> created")
