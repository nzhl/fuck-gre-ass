from bs4 import BeautifulSoup

from .ui import UI
from .logger import get_logger
from .player import Player
from .io import Browser
from .config import *


logger = get_logger(__name__)

class Client(object):

    def __init__(self):
        self.ui = UI()
        self.moodle = Browser('moodle')
        self.xiami = Browser('xiami')
        self.data = {}

    
    def login(self):
        response = self.moodle.get(INDEX_URL)
        if response.url == INDEX_URL:
            self.parse_modules(response.content)
            return 

        while True:
            should_alert = False
            username, password = self.ui.get_login_info(should_alert)
            response = self.moodle.post(url=LOGIN_URL, form={
                'username': username,
                'password': password,
            })
            if response.url == INDEX_URL:
                break
            else:
                should_alert = True
        self.parse_modules(response.content)
     
    
    def loop(self):
        self.login()
        while True:
            self.ui.show_list(self.data)
            command = self.ui.get_command()
            self.dispatcher(command)

    def dispatcher(self, command):
        if command in ('j', 'KEY_DOWN'):
            self.down()
        elif command in ('k', 'KEY_UP'):
            self.up()
        elif command in ('l', 'KEY_LEFT'):
            self.front()
        elif command in ('h', 'KEY_RIGHT'):
            self.back()
        elif command in ('m'):
            self.bgm()
        else:
            pass
            
    def up(self):
        total_rows = len(self.data['list'])
        position = self.data['position']
        self.data['position'] = (position - 1 + total_rows) % total_rows

    def down(self):
        total_rows = len(self.data['list'])
        position = self.data['position']
        self.data['position'] = (position + 1) % total_rows

    def front(self):
        type = self.data['type']
        list = self.data['list']
        position = self.data['position']
        if type == "modules":
            response = self.modules.get(list[position][1])
            parse_module(response.content)
        elif type == "module":
            pass
        elif type == "songs":
            song_id = list[position][1]
            self.player = Player(song_id, self.xiami)
            self.player.start()

    def back(self):
        pass

    def bgm(self):
        keyword = str(self.ui.get_song_name(), 'utf-8')
        response = self.xiami.get(SEARCH_URL + keyword)
        self.parse_songs(response.content)
    

    def parse_modules(self, content):
        modules = []
        soup = BeautifulSoup(content, 'lxml')
        for row_tag in soup.find(class_="nottingham-tabcontent").find_all("h2"):
            a_tag = row_tag.find("a")
            modules.append((a_tag.string, a_tag['href']))

        self.data['name'] = soup.find(class_="profile").contents[0]
        self.data['type'] = "modules"
        self.data['list'] = modules
        self.data['position'] = 0

    def parse_module(self, content):
        pass

    def parse_songs(self, content):
        songs = []
        soup = BeautifulSoup(content, "lxml")
        rows = soup.find_all(attrs={'data-playstatus':"1"})
        for i in range(10):
            row_tag = rows[i]
            if row_tag.select(".song_name"):
                name = row_tag.select(".song_name")[0].get_text(strip=True)
                artist = row_tag.select(".song_artist")[0].get_text(strip=True)
                song_id = row_tag.input['value']
                songs.append((name + ' // ' + artist, song_id,))
            else:
                break
        self.data['name'] = soup.select("#search_text")[0]['value']
        self.data['type'] = "songs"
        self.data['list'] = songs
        self.data['position'] = 0
