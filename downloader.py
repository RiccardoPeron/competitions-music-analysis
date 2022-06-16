from spotdl import __main__ as spotdl
import json
import os
import subprocess
import sys
from pathlib import Path

print('import spotdl...')


def download(title, link, out_folder, i):
    print("downloading ", title, " OTS")
    os.chdir('./' + out_folder)
    fname = ''
    if i < 10:
        fname = '0' + str(i) + ' - ' + title
    else:
        fname = str(i) + ' - ' + title
    os.mkdir(fname)
    os.chdir('./' + fname)
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

    for i, movie in enumerate(movies):
        link = movie["link"].replace(" ", "_")
        title = movie["title"].replace(" ", "_")
        download(title, link, out_folder, i+1)

    print('--- DONE ---')


# download_all('sanremo.json', 'Sanremo')
