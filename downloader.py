import json
import os
import subprocess
import sys
from pathlib import Path

print('import spotdl...')
from spotdl import __main__ as spotdl


def download(title, link):
    print("downloading ", title, " OTS")
    os.chdir('./OST')
    os.mkdir(title)
    os.chdir('./' + title)
    # subprocess.check_call(['touch', 'a.txt'])
    # subprocess.check_call([sys.executable, spotdl.__file__, link])
    subprocess.check_call(['spotdl', link])
    os.chdir('..')
    os.chdir('..')


print('open file...')
file = open("movies.json")
movies = json.load(file)

print("creating main folder...")
ost = Path('OST')
if not ost.exists():
    ost.mkdir()

for movie in movies:
    link = movie["link"].replace(" ", "_")
    if movie["original_title"] == '':
        title = movie["title"].replace(" ", "_")
    else:
        title = movie["original_title"].replace(" ", "_")
    download(title, link)
