from bs4 import BeautifulSoup, Tag
from cachetools.func import ttl_cache

from curby.core import request, REFRESH_TTL

def _extract_title(element: Tag):
    return list(element.children)[1].text.lower()

def _extract_song_route(element: Tag):
    if element.find("a") is not None:
        return element.find("a").get("href")
    else:
        return "None"

def _extract_route(soup: BeautifulSoup):
    artists_lines = soup.find_all(attrs={"data-score": True})
    if len(artists_lines) > 0:
        chossen_artist : Tag = artists_lines[0]
        return chossen_artist.contents[0].contents[0].get("href")

def _extract_artist_genres(soup: BeautifulSoup):
    genre_root = soup.select(".genre-list")
    genres_tag = list(list(genre_root[0].children)[0])[::2]
    return [tag.text for tag in genres_tag if tag.text != '(none)']

def _extract_titles(soup: BeautifulSoup):
    titles: list[str] = map(lambda element : _extract_title(element), soup.select("tr"))
    return list(filter(lambda element : element != "title", titles))

def _extract_song_genres(soup: BeautifulSoup):
    genre_root = soup.select(".genre-list")
    genres_tag = list(list(genre_root[0].children)[0])[::2]
    return [tag.text for tag in genres_tag if tag.text != '(none)']

def _extract_songs_routes(soup: BeautifulSoup) -> list[str]:
    return list(map(lambda element : _extract_song_route(element), soup.select("tr")))

@ttl_cache(ttl=REFRESH_TTL)
def get_route(artist_name: str):
    response = request(f"https://musicbrainz.org/taglookup/index?tag-lookup.artist={artist_name}")
    return _extract_route(BeautifulSoup(response.text, "html.parser"))

@ttl_cache(ttl=REFRESH_TTL)
def get_artist_genres(artist_route: str):
    response = request(f"https://musicbrainz.org/{artist_route}")
    return _extract_artist_genres(BeautifulSoup(response.text, "html.parser"))

@ttl_cache(ttl=REFRESH_TTL)
def get_songs_titles(artist_route: str):
    response = request(f"https://musicbrainz.org/{artist_route}")
    return _extract_titles(BeautifulSoup(response.text, "html.parser"))

@ttl_cache(ttl=REFRESH_TTL)
def get_songs_routes(artist_route: str):
    response = request(f"https://musicbrainz.org/{artist_route}")
    return _extract_songs_routes(BeautifulSoup(response.text, "html.parser"))

@ttl_cache(ttl=REFRESH_TTL)
def get_song_genres(song_route: str):
    response = request(f"https://musicbrainz.org/{song_route}")
    return _extract_song_genres(BeautifulSoup(response.text, "html.parser"))