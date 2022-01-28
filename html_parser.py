import requests
import schedule
from bs4 import BeautifulSoup

from config import HEADERS


class Parser:
    def __init__(self, url):
        self.session = requests.Session()
        self.url = url
        self.response = self.get_page(self.url)
        self.stats = {}

    def get_page(self, url):
        return self.session.get(url=url, headers=HEADERS, timeout=5).text

    def parse_tt_views(self):
        bs = BeautifulSoup(self.response, "html.parser")
        views = bs.select(".video-count")
        videos = {}
        for i, v in enumerate(views):
            videos[f'{len(views) - i}'] = f'{v.text}'

        following = bs.find("strong", title="Following").text
        followers = bs.find("strong", title="Followers").text
        likes = bs.find("strong", title="Likes").text
        self.stats['videos'] = videos
        self.stats['following'] = following
        self.stats['followers'] = followers
        self.stats['likes'] = likes

