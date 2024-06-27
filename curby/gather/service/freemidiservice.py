import re

from bs4 import BeautifulSoup, Tag
from requests import Response
from cachetools.func import ttl_cache

from curby.core import request, REFRESH_TTL

FREEMIDI_HEADER = {
    "User-Agent": "Chrome/121.0.0.0"
}

def _extract_name(element: Tag):
    return element.text.lower()

def _extract_route(element: Tag):
    return element.next_element.get("href")

def _extract_song_title(element: Tag):
    return " ".join(re.findall(r'\w+', list(element.children)[1].text)).lower()

def _extract_song_route(element: Tag):
    return list(list(element.children)[1].children)[1].get("href")


def _extract_download_route(soup: BeautifulSoup):
    return soup.find('a', id='downloadmidi')['href']
    
def _extract_cookie(response: Response):
    return response.headers.get("Set-Cookie")

def _extract_names(soup: BeautifulSoup):
    return list(map(lambda element : _extract_name(element), soup.select(".genre-link-text")))

def _extract_routes(soup: BeautifulSoup):
    return list(map(lambda element : _extract_route(element), soup.select(".genre-link-text")))

def _extract_song_titles(soup: BeautifulSoup):
    return list(map(lambda element : _extract_song_title(element), soup.select(".artist-song-cell")))

def _extract_song_routes(soup: BeautifulSoup):
    return list(map(lambda element : _extract_song_route(element), soup.select(".artist-song-cell")))


@ttl_cache(ttl=REFRESH_TTL)
def get_names(letter: str):
    response = request(f"https://freemidi.org/artists-{letter.lower()}", header=FREEMIDI_HEADER)
    return _extract_names(BeautifulSoup(response.text, 'html.parser'))

@ttl_cache(ttl=REFRESH_TTL)
def get_routes(letter: str):
    response = request(f"https://freemidi.org/artists-{letter.lower()}", header=FREEMIDI_HEADER)
    return _extract_routes(BeautifulSoup(response.text, 'html.parser'))

@ttl_cache(ttl=REFRESH_TTL)
def get_download_route(song_route: str):
    response = request(f"https://freemidi.org/{song_route}", header=FREEMIDI_HEADER)
    return _extract_download_route(BeautifulSoup(response.text, 'html.parser'))

@ttl_cache(ttl=REFRESH_TTL)
def get_cookie(song_route: str):
    response = request(f"https://freemidi.org/{song_route}", header=FREEMIDI_HEADER)
    return _extract_cookie(response)

@ttl_cache(ttl=REFRESH_TTL)
def get_song_titles(artist_route: str):
    response = request(f"https://freemidi.org/{artist_route}", header=FREEMIDI_HEADER)
    return _extract_song_titles(BeautifulSoup(response.text, 'html.parser'))

@ttl_cache(ttl=REFRESH_TTL)
def get_song_routes(artist_route: str):
    response = request(f"https://freemidi.org/{artist_route}", header=FREEMIDI_HEADER)
    return _extract_song_routes(BeautifulSoup(response.text, 'html.parser'))       