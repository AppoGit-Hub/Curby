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
def get_artist_route(artist_name: str) -> str:
    """
    Scrap from the artist name get the artist route
    
    Parameter
    ---------
    artist_name : str
        the artist name

    Return
    ------
    the artist route

    Example
    -------
    >>> get_artist_route("ariana grande")
    >>> "/artist/f4fdbb4c-e4b7-47a0-b83b-d91bbfcfa387"

    Note
    ----
    This function is cached
    """
    response = request(f"https://musicbrainz.org/taglookup/index?tag-lookup.artist={artist_name}")
    return _extract_route(BeautifulSoup(response.text, "html.parser"))

@ttl_cache(ttl=REFRESH_TTL)
def get_artist_genres(artist_route: str) -> list[str]:
    """
    Scrap from the artist route the artist genres

    Parameter
    ---------
    artist_route : str
        the artist route (gotten from .get_artist_route(...))

    Return
    ------
    the artist route

    Example
    -------
    >>> get_artist_genres("/artist/f4fdbb4c-e4b7-47a0-b83b-d91bbfcfa387")
    >>> ['pop', 'r&b', 'trap soul', 'dance-pop', 'trap']

    Note
    ----
    This function is cached
    """
    response = request(f"https://musicbrainz.org/{artist_route}")
    return _extract_artist_genres(BeautifulSoup(response.text, "html.parser"))

@ttl_cache(ttl=REFRESH_TTL)
def get_songs_titles(artist_route: str) -> list[str]:
    """
    Scrap the artist songs titles from the artist route

    Parameter
    ---------
    artist_route : str
        the artist route (gotten from .get_artist_route(...))
    
    Return
    ------
    the list of songs titles

    Example
    -------
    >>> get_songs_titles("/artist/f4fdbb4c-e4b7-47a0-b83b-d91bbfcfa387")
    >>> ['yours truly', 'my everything', 'dangerous woman', 'sweetener', ... ]

    Note
    ----
    This function is cached
    """
    response = request(f"https://musicbrainz.org/{artist_route}")
    return _extract_titles(BeautifulSoup(response.text, "html.parser"))

@ttl_cache(ttl=REFRESH_TTL)
def get_songs_routes(artist_route: str) -> list[str]:
    """
    Scrap from the artist route, the songs routes 

    Paramter
    --------
    artist_route : str
        the artist route (gotten from .get_artist_route(...))
    
    Return
    ------
    a list of all the songs routes

    Example
    -------
    >>> get_songs_routes("/artist/f4fdbb4c-e4b7-47a0-b83b-d91bbfcfa387")
    >>> ['/release-group/1237b040-fb8f-4f23-8000-fb6909486c83', '/release-group/17fd3576-b584-4f32-8ff0-12206d4cb66c', ... ]
    
    Note
    ----
    This function is cached
    """
    response = request(f"https://musicbrainz.org/{artist_route}")
    return _extract_songs_routes(BeautifulSoup(response.text, "html.parser"))

@ttl_cache(ttl=REFRESH_TTL)
def get_song_genres(song_route: str) -> list[str]:
    """
    Scrap the list of songs genres from the song route

    Parameter
    ---------
    song_route : str
        the song route (gotten from .get_songs_routes(...))
    
    Return
    ------
    the list of songs genres

    Example
    -------
    >>> get_song_genres("/release-group/1237b040-fb8f-4f23-8000-fb6909486c83")
    >>> ['pop', 'contemporary r&b', 'dance-pop', 'ballad', 'hip hop']

    Note
    ----
    This function is cached
    """
    response = request(f"https://musicbrainz.org/{song_route}")
    return _extract_song_genres(BeautifulSoup(response.text, "html.parser"))