import re

from bs4 import BeautifulSoup, Tag
from cachetools.func import ttl_cache

from curby.core import (
    request,
    REFRESH_TTL
)

BILLBOARD_HEADER = {
    "User-Agent": "Chrome/120.0.0.0"
}

def _extract_title(element: Tag):
    return ' '.join(re.findall(r'\w+', element.text)).lower()

def _extract_author(element: Tag):
    return ' '.join(re.findall(r'\w+', element.find_next_sibling('span').text)).lower()


def _extract_titles(soup: BeautifulSoup, max_songs: int):
    elements = soup.find_all(id="title-of-a-story")
    elements = elements[6:403:4][:max_songs] #sometimes 5 or 6
    return list(map(lambda element : _extract_title(element), elements))

def _extract_authors(soup: BeautifulSoup, max_songs: int):
    elements = soup.find_all(id="title-of-a-story")
    elements = elements[6:403:4][:max_songs] #sometimes 5 or 6
    return list(map(lambda element : _extract_author(element), elements))


@ttl_cache(ttl=REFRESH_TTL)
def get_songs_titles(max_songs: int) -> list[str]:
    response = request("https://www.billboard.com/charts/hot-100/", header=BILLBOARD_HEADER)
    return _extract_titles(BeautifulSoup(response.text, 'html.parser'), max_songs)

@ttl_cache(ttl=REFRESH_TTL)
def get_songs_authors(max_songs: int) -> list[str]:
    response = request("https://www.billboard.com/charts/hot-100/", header=BILLBOARD_HEADER)
    return _extract_authors(BeautifulSoup(response.text, 'html.parser'), max_songs)