from os.path import isdir, join, isfile
from os import mkdir
from pickle import load, dump

from requests.utils import dict_from_cookiejar, add_dict_to_cookiejar
from requests.exceptions import TooManyRedirects
from requests import get, Session

from .config import *
from .logger import get_logger

logger = get_logger(__name__)

class Browser(object):
    def __init__(self, name):
        self.session = Session()
        self.session.max_redirects = 5
        self.path = join(COOKIE_DIR, '%s.cookie' % name)
        self.load_cookies()
        

    def load_cookies(self):
        if not isfile(self.path):
            return
        with open(self.path, "rb") as file:
            add_dict_to_cookiejar(self.session.cookies, load(file))


    def save_cookies(self):
        if not isdir(COOKIE_DIR):
            mkdir(COOKIE_DIR)
        with open(self.path, "wb") as file:
            cookies_dict = dict_from_cookiejar(self.session.cookies)
            dump(cookies_dict, file)


    def clear_cookies(self):
        self.session.cookies.clear_session_cookies()


    def get(self, url):
        try:
            response = self.session.get(url, headers=HEADERS)
        except TooManyRedirects:
            response = None
        return response


    def post(self, url, form):
        response =  self.session.post(url=url, data=form, headers=HEADERS)
        return response

