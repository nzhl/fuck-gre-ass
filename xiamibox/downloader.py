from urllib.parse import unquote
from scrapy.crawler import CrawlerProcess
from scrapy import Request, Spider

from re import compile, findall


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


class SongSpider(Spider):
    name = "song"


    def start_requests(self):
        xml_url = 'http://www.xiami.com/song/playlist/id/%s' % self.song_id
        yield Request(url=xml_url, callback=self.parse_xml)
    
    
    def parse_xml(self, response):
        xml = str(response.body)
        raw = compile('<location>(.*)</location>').findall(xml)[0]
        yield Request(url=raw2url(raw), callback=self.save_song)


    def save_song(self, response):
        with open("%s.mp3" % self.song_id, "wb") as f:
            f.write(response.body)


def download_song(song_id):
    process = CrawlerProcess()
    process.crawl(SongSpider, song_id=song_id)
    process.start()

if __name__ == '__main__':
    download_song('382560')
