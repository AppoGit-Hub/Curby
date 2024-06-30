import re

from bs4 import BeautifulSoup, Tag
from requests import Response
from cachetools.func import ttl_cache

from curby.core import (
    request, 
    REFRESH_TTL,
    generic_search
)
from curby.error import (
    FreeMidiError
)

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
def _get_names(letter: str) -> list[str]:
    """
    Scrap freemidi.org to get list the all artists' names that begins by the letter <letter>

    Parameter
    ---------
    letter : str
        the begining letter of the artist

    Return
    ------
    a list the all artists' names that begins by the letter <letter>
    
    Example
    -------
    >>> get_names("a")
    >>> ['a dub', 'a f i', 'a flock of seagulls', 'a perfect circle', 'a taste of honey', ... ]

    Note
    ----
    This function is cached
    """
    response = request(f"https://freemidi.org/artists-{letter.lower()}", header=FREEMIDI_HEADER)
    return _extract_names(BeautifulSoup(response.text, 'html.parser'))

@ttl_cache(ttl=REFRESH_TTL)
def _get_routes(letter: str) -> list[str]:
    """
    Scrap the all routes of the artirts that beginings with the letter <letter>

    Parameter
    ---------
    letter : str
        the first letter of the artist

    Return
    ------
    a list of all the letter <letter> of artists'routes
    
    Example
    -------
    >>> get_routes("a")
    >>> ['artist-1191-a-dub', 'artist-140-a-f-i', 'artist-1886-a-flock-of-seagulls', ... ]
    
    Note
    ----
    This function is cached
    """
    response = request(f"https://freemidi.org/artists-{letter.lower()}", header=FREEMIDI_HEADER)
    return _extract_routes(BeautifulSoup(response.text, 'html.parser'))

@ttl_cache(ttl=REFRESH_TTL)
def _get_download_route(song_route: str) -> list[str]:
    """
    Scrap freemidi.org to get the download route from the song route

    Parameter
    ---------
    song_route : str
        the song route to start from (gotten from .get_routes(...))

    Return
    ------
    a list of downlaod routes

    Example
    -------
    >>> get_download_route("artist-1886-a-flock-of-seagulls")
    >>> ['download3-18484-i-ran-so-far-away-a-flock-of-seagulls', 'download3-18483-the-more-you-live-more-you-love-a-flock-of-seagulls']
    
    Note
    ----
    This function is cached
    """
    response = request(f"https://freemidi.org/{song_route}", header=FREEMIDI_HEADER)
    return _extract_download_route(BeautifulSoup(response.text, 'html.parser'))

@ttl_cache(ttl=REFRESH_TTL)
def _get_cookie(song_route: str) -> str:
    """
    Scrap freemidi.org to get the cookie from the song route 
    
    Parameter
    ---------
    song_route : str
        the song route to start from (gotten from .get_routes(...))
    
    Return
    ------
    the cookie 

    Example
    -------
    >>> get_cookie('artist-1886-a-flock-of-seagulls')
    >>> PHPSESSID=a87rdmj2h87lf4qth51rqlc0e0; path=/

    Note
    ----
    This function is cached
    """
    response = request(f"https://freemidi.org/{song_route}", header=FREEMIDI_HEADER)
    return _extract_cookie(response)

@ttl_cache(ttl=REFRESH_TTL)
def _get_song_titles(artist_route: str) -> list[str]:
    """
    Scrap freemidi.org to get a the songs list from the artist_route

    Parameter
    ---------
    artist_route : str
        the artirst route (gotten from .get_routes(...))

    Return
    ------

    Example
    -------
    >>> get_song_titles('artist-1191-a-dub')
    >>> ['who i be']

    Note
    ----
    This function is cached
    """
    response = request(f"https://freemidi.org/{artist_route}", header=FREEMIDI_HEADER)
    return _extract_song_titles(BeautifulSoup(response.text, 'html.parser'))

@ttl_cache(ttl=REFRESH_TTL)
def _get_song_routes(artist_route: str) -> list[str]:
    """
    Scrap a list songs routes from the artist route

    Parameter
    ---------
    artist_route : str
        the artist route

    Return
    ------
    list of songs routes

    Example
    -------
    >>> get_song_routes('artist-1886-a-flock-of-seagulls')
    >>> ['download3-18484-i-ran-so-far-away-a-flock-of-seagulls', 'download3-18483-the-more-you-live-more-you-love-a-flock-of-seagulls']

    Note
    ----
    This function is cached
    """
    response = request(f"https://freemidi.org/{artist_route}", header=FREEMIDI_HEADER)
    return _extract_song_routes(BeautifulSoup(response.text, 'html.parser'))


@ttl_cache(ttl=REFRESH_TTL)
def get_artist_route(artist_name: str) -> str:
    """
    From the artist name get the artist route

    Parameter
    ---------
    artist_name : str
        the artist name

    Return
    ------
    artists_route : str
        the artist route 

    Example
    -------
    >>> get_artist_route("ariana grande")
    >>> "artist-1751-ariana-grande"

    Note
    ----
    This function is cached
    """
    try:
        artists_names: list[str] = _get_names(artist_name[0])
        artists_routes: list[str] = _get_routes(artist_name[0])
        artists: list[tuple[str, str]] = list(zip(artists_names, artists_routes))
        find_index: int = generic_search(artists, lambda element: element[0] == artist_name)
        artists_name, artists_route = artists[find_index]
        return artists_route
    except Exception as error:
        print(error)
        raise FreeMidiError()

@ttl_cache(ttl=REFRESH_TTL)
def get_song_route(artist_name: str, song_title: str) -> str:
    """
    From the artist name and the song title get the song route

    Parameter
    ---------
    artist_name : str
        the artist name
    song_title : str
        the song title
    
    Return
    ------
    the song route

    Example
    -------
    >>> get_song_route("ariana grande", "pov")
    >>> download3-26867-pov-ariana-grande

    Note
    ----
    This function is cached
    """
    try:
        artist_route: str = get_artist_route(artist_name)
        songs_titles: list[str] = _get_song_titles(artist_route)
        songs_routes: list[str] = _get_song_routes(artist_route)
        songs: list[tuple[str, str]] = list(zip(songs_titles, songs_routes))
        find_index: int = generic_search(songs, lambda element: element[0] == song_title)
        title, song_route = songs[find_index]
        return song_route
    except Exception as error:
        print(error)
        raise FreeMidiError()

@ttl_cache(ttl=REFRESH_TTL)
def get_download_route(artist_name: str, song_title: str) -> str:
    """
    From the artist name and the song title get the download route

    Parameter
    ---------
    artist_name : str
        the artist name
    song_title : str
        the song title

    Return
    ------
    the download route

    Example
    -------
    >>> get_download_route("ariana grande", "pov")
    >>> getter-26867

    Note
    ----
    This function is cached
    """
    try:
        song_route: str = get_song_route(artist_name, song_title)
        download_route: str = _get_download_route(song_route)
        return download_route
    except Exception as error:
        print(error)
        raise FreeMidiError()

@ttl_cache(ttl=REFRESH_TTL)
def get_cookie(artist_name: str, song_title: str) -> str:
    """
    From the artist name and the song title get the cookie

    Parameter
    ---------
    artist_name : str
        the artist name
    song_title : str
        the song title

    Return
    ------
    the cookie

    Example
    -------
    >>> get_cookie("ariana grande", "pov")
    >>> PHPSESSID=gmcrphc99ms4jvhoplvst0pem6; path=/
    
    Note
    ----
    This function is cached
    """
    try:
        song_route: str = get_song_route(artist_name, song_title)
        return _get_cookie(song_route)
    except Exception as error:
        print(error)
        raise FreeMidiError()