from cachetools.func import ttl_cache 

from curby.gather.service import (
    musicbrainzservice
)
from curby.core import (
    generic_search,
    REFRESH_TTL
)

@ttl_cache(ttl=REFRESH_TTL)
def get_all_songs(artist_name: str) -> list[tuple[str, str]]:
    """
    Get all the songs as a pair title, route from the artist name

    Parameter
    ---------
    artist_name : str
        the artist name

    Return
    ------
    a list of pair of title, route

    Example
    -------
    >>> .get_all_songs("ariana grande")
    >>> [('my everything', '/release-group/1237b040-fb8f-4f23-8000-fb6909486c83'), ('dangerous woman', '/release-group/17fd3576-b584-4f32-8ff0-12206d4cb66c'), ... ]
    
    Note
    ----
    This function is cached
    """
    artist_route: str = musicbrainzservice.get_artist_route(artist_name)
    songs_titles: list[str] = musicbrainzservice.get_songs_titles(artist_route)
    songs_routes: list[str] = musicbrainzservice.get_songs_routes(artist_route)
    return list(zip(songs_titles, songs_routes))

@ttl_cache(ttl=REFRESH_TTL)
def get_artist_genres(artist_name: str) -> list[str]:
    """
    Get all artist genres from the artist name

    Parameter
    ---------
    artist_name : str
        the artist name

    Return
    ------
    the list of the artist genres

    Example
    -------
    >>> .get_artist_genres("ariana grande")
    >>> ['pop', 'r&b', 'trap soul', 'dance-pop', 'trap']

    Note
    ----
    This function is cached
    """
    artist_route: str = musicbrainzservice.get_artist_route(artist_name)
    return musicbrainzservice.get_artist_genres(artist_route)

@ttl_cache(ttl=REFRESH_TTL)
def get_song_genres(artist_name: str, song_title: str) -> list[tuple[str, str]]:
    """
    Get all the genres of a song from the  artist name and song title

    Paramter
    --------
    artist_name : str
        the artist name
    song_title : str
        the song title
    
    Return
    ------
    the list of genres of the song

    Example
    -------
    >>> .get_song_genres("ariana grande", "my everything")
    >>> ['pop', 'contemporary r&b', 'dance-pop', 'ballad', 'hip hop']
    
    Note
    ----
    This function is cached
    """
    artist_route: str = musicbrainzservice.get_artist_route(artist_name)
    songs_titles: list[str] = musicbrainzservice.get_songs_titles(artist_route)
    songs_routes: list[str] = musicbrainzservice.get_songs_routes(artist_route)
    songs: list[tuple[str, str]] = list(zip(songs_titles, songs_routes))
    search_index: int = generic_search(songs, lambda element: element[0] == song_title)
    title, route = songs[search_index]
    return musicbrainzservice.get_song_genres(route)

