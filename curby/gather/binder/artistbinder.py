from cachetools.func import ttl_cache 

from curby.gather.controller import (
    musicbrainzcontroller
)
from curby.core import (
    Artist,
    REFRESH_TTL
)

@ttl_cache(ttl=REFRESH_TTL)
def get_artist(artist_name: str) -> Artist:
    """
    Tries fully fill a artist object from an artist name

    Parameter
    ---------
    artist_name : str
        the artist name
    
    Return
    ------
    an Artist object

    Example
    ------
    >>> .get_artist("ariana grande")
    >>> Artist(name='ariana grande', genres=['pop', 'r&b', 'trap soul', 'dance-pop', 'trap'])
    
    Note
    ----
    This function is cached
    """
    genres: list[str] = musicbrainzcontroller.get_artist_genres(artist_name)
    return Artist(artist_name, genres)