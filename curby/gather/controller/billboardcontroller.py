from cachetools.func import ttl_cache 

from curby.gather.service import (
    billboardservice
)
from curby.core import (
    REFRESH_TTL
)

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
    song_authors: list[str] = billboardservice.get_songs_authors(max_songs)
    song_titles: list[str] = billboardservice.get_songs_titles(max_songs)
    return list(zip(song_authors, song_titles))