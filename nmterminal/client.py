from os.path import isdir, join
from os import mkdir
from pickle import dump, load
from requests.utils import dict_from_cookiejar, cookiejar_from_dict
from requests import get, Session
from bs4 import BeautifulSoup
from threading import Thread

from .ui import UI
from .config import *
from .logger import get_logger
from .player import Player
from .io import raw2url, cache_song

logger = get_logger(__name__)

class Client(object):

    def __init__(self):
        self.username = ""
        self.password = ""
        self.session = Session()
        self.ui = UI()
        self.player = Player()
        self.data = {}
        logger.warning("init")

    
    def save_cookies(self):
        logger.debug("save cookie")
        cookies_dict = dict_from_cookiejar(self.session.cookies)
        for k, v in cookies_dict.items():
            logger.debug(1)
            logger.debug(k)
            logger.debug(v)
        if not isdir(COOKIE_PATH):
            mkdir(COOKIE_PATH)
        with open(join(COOKIE_PATH, 'login.cookie'), "wb") as file:
            dump(cookies_dict, file)
            

    def load_cookie(self):
        cookies = None
        cookie_file_path = join(COOKIE_PATH, 'login.cookie')
        try:
            with open(cookie_file_path, "rb") as file:
                    cookies = cookiejar_from_dict(load(file))
        except FileNotFoundError:
            logger.debug("login cookie : %s not found" % cookie_file_path)
        return cookies

    def cookie_login(self):
        cookies = self.load_cookie()
        if cookies:
            response = self.session.get(INDEX_URL, cookies=cookies)
            if response.url == INDEX_URL:
                self.parse_modules(response.content)
                return True
        return False
            

    def login(self):
            while True:
                should_alert = False
                self.username, self.password = self.ui.get_login_info(should_alert)
                response = self.session.post(url=LOGIN_URL, data={
                    'username': self.username,
                    'password': self.password,
                })
                if response.url == INDEX_URL:
                    break
                else:
                    should_alert = True
            self.save_cookies()
            self.parse_modules(response.content)
     
    
    def loop(self):
        if not self.cookie_login():
            self.login()
        self.data['type'] = "modules"
        self.data['position'] = 0
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
        list = self.data['list']
        position = self.data['position']
        url = list[position][1]
        type = self.data['type']
        if type == "modules":
            self.data['type'] = "module"
            parse_module(get(url).content)
        elif type == "module":
            pass
        elif type == "songs":
            response = get(XML_URL + url, headers=HEADERS)
            raw = BeautifulSoup(response.content, "lxml").location.get_text()
            url = raw2url(raw)
            self.cache_thread = Thread(target=cache_song,
                                       args=(url, list[position][0]))
            self.cache_thread.start()

    def back(self):
        pass

    def bgm(self):
        keyword = str(self.ui.get_song_name(), 'utf-8')
        response = get(SEARCH_URL + keyword, headers=HEADERS)
        self.parse_songs(response.content)
        self.data['name'] = keyword
        self.data['position'] = 0
        self.data['type'] = 'songs'
        
    

    def parse_modules(self, content):
        modules = []
        soup = BeautifulSoup(content, 'lxml')
        for row_tag in soup.find(class_="nottingham-tabcontent").find_all("h2"):
            a_tag = row_tag.find("a")
            modules.append((a_tag.string, a_tag['href']))
        self.data['list'] = modules
        self.data['name'] = soup.find(class_="profile").contents[0]

    def parse_module(self, content):
        pass

    def parse_songs(self, content):
        songs = []
        soup = BeautifulSoup(content, "lxml").find_all(attrs={'data-playstatus':"1"})
        for i in range(10):
            row_tag = soup[i]
            if row_tag.select(".song_name"):
                name = row_tag.select(".song_name")[0].get_text(strip=True)
                artist = row_tag.select(".song_artist")[0].get_text(strip=True)
                song_id = row_tag.input['value']
                songs.append((name + ' // ' + artist, song_id,))
            else:
                break
        self.data['list'] = songs
