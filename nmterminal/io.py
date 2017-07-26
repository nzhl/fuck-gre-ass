from os.path import isdir, join
from os import mkdir
from shlex import quote
from urllib.parse import unquote
from subprocess import Popen
from requests import get


from .config import *


def raw2url(raw):
    matrix_height = int(raw[:raw.find('h')])
    raw = raw[raw.find('h'):]
    matrix_width = len(raw) // matrix_height
    remainer = len(raw) % matrix_height

    url = []
    for y in range(matrix_width):
        for x in range(matrix_height):
            index = x * matrix_width + y + min(x, remainer)
            url.append(raw[index])
    for i in range(remainer):
        url.append(raw[(i+1) * (matrix_width + 1) - 1])
    return unquote("".join(url)).replace("^", "0")

def cache_song(url, name):
    if not isdir(SONG_PATH):
        mkdir(SONG_PATH)

    song_path = join(SONG_PATH, str(hash(name))) + ".mp3"
    with open(song_path, "wb") as file:
        response = get(url, headers=HEADERS)
        file.write(response.content)
    Popen("afplay " + song_path, shell=True)
