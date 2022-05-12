from spotdl import __main__ as spotdl
import json
import os
import subprocess
import sys
from pathlib import Path

print('import spotdl...')


def download(title, link, out_folder):
    print("downloading ", title, " OTS")
    os.chdir('./' + out_folder)
    os.mkdir(title)
    os.chdir('./' + title)
    # subprocess.check_call(['touch', 'a.txt'])
    # subprocess.check_call([sys.executable, spotdl.__file__, link])
    subprocess.check_call(['spotdl', link, '--output-format wav'])
    os.chdir('..')
    os.chdir('..')


def download_all(json_source, out_folder):
    print('open file...')
    file = open(json_source)
    movies = json.load(file)

    print("creating main folder...")
    ost = Path(out_folder)
    if not ost.exists():
        ost.mkdir()

    for movie in movies:
        link = movie["link"].replace(" ", "_")
        title = movie["title"].replace(" ", "_")
        download(title, link, out_folder)

    print('--- DONE ---')


download_all('sanremo.json', 'Sanremo')
