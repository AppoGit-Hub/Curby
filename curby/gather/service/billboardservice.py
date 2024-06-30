import re

from bs4 import BeautifulSoup, Tag
from cachetools.func import ttl_cache

from curby.core import (
    request,
    REFRESH_TTL
)
from curby.error import (
    BillboardError
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
def _get_songs_titles(max_titles: int) -> list[str]:
    """
    Scrap the song titles of the first <max_titles> on the billboard of billboard.com

    Parameter
    ---------
    max_titles : int
        song titles number to return
    
    Return
    ------
    a list of lenght <max_titles> of the songs' titles

    Example
    -------
    >>> get_songs_authors(3)
    >>> ['please please please', 'i had some help', 'a bar song tipsy']

    Note
    ----
    This function is cached
    """    
    response = request("https://www.billboard.com/charts/hot-100/", header=BILLBOARD_HEADER)
    return _extract_titles(BeautifulSoup(response.text, 'html.parser'), max_titles)

@ttl_cache(ttl=REFRESH_TTL)
def _get_songs_authors(max_authors: int) -> list[str]:
    """
    Scrap the song authors of the first <max_authors> on the billboard of billboard.com

    Parameter
    ---------
    max_authors : int
        song authors number to return
    
    Return
    ------
    a list of length <max_authors> of the song authors

    Example
    -------
    >>> get_songs_authors(3)
    >>> ['sabrina carpenter', 'post malone featuring morgan wallen', 'shaboozey']

    Note
    ----
    This function is cached
    """ 
    response = request("https://www.billboard.com/charts/hot-100/", header=BILLBOARD_HEADER)
    return _extract_authors(BeautifulSoup(response.text, 'html.parser'), max_authors)

@ttl_cache(ttl=REFRESH_TTL)
def get_popular(max_songs: int = 1) -> list[tuple[str, str]]:
    """
    Get <max_songs> number of song titles and authors pairs on the billboard on billboard.com

    Parameter
    ---------
    <max_songs> : int
        the number of songs to scrap on the billboard
    
    Return
    ------
    a list of lenght <max_songs> of pair of a song title and author

    Return Example
    --------------
    >>> [('sabrina carpenter', 'please please please'), ('post malone featuring morgan wallen', 'i had some help'), ('shaboozey', 'a bar song tipsy')]

    """
    try:
        song_authors = _get_songs_authors(max_songs)
        song_titles = _get_songs_titles(max_songs)
        return list(zip(song_authors, song_titles))
    except Exception as error:
        print(error)
        raise BillboardError()