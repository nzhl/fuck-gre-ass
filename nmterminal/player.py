from os.path import isdir, isfile, join
from os import mkdir
from urllib.parse import unquote
from threading import Thread
from subprocess import Popen
from bs4 import BeautifulSoup

from .logger import get_logger
from .config import *

logger = get_logger(__name__)

class Player(Thread):
    def __init__(self, song_id, xiami):
        super().__init__()
        self.song_id = song_id
        self.xiami = xiami
        self.path = join(SONG_DIR, song_id) + ".mp3"
        

    def run(self):
        if not isfile(self.path):
            self.cache_song()
        Popen("afplay " + self.path, shell=True)

    def cache_song(self):
        if not isdir(SONG_DIR):
            mkdir(SONG_DIR)
        response = self.xiami.get(XML_URL + self.song_id)
        raw = BeautifulSoup(response.content, "lxml").location.get_text()
        url = self.raw2url(raw)
        with open(self.path, "wb") as file:
            response = self.xiami.get(url)
            file.write(response.content)

    def raw2url(self, raw):
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

