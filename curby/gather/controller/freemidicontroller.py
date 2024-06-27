from cachetools.func import ttl_cache 

from curby.gather.service import (
    freemidiservice,
)
from curby.core import (
    generic_search,
    REFRESH_TTL
)

@ttl_cache(ttl=REFRESH_TTL)
def get_artist_route(artist_name: str) -> str:
    artists_names: list[str] = freemidiservice.get_names(artist_name[0])
    artists_routes: list[str] = freemidiservice.get_routes(artist_name[0])
    artists: list[tuple[str, str]] = list(zip(artists_names, artists_routes))
    find_index: int = generic_search(artists, lambda element: element[0] == artist_name)
    artists_name, artists_route = artists[find_index]
    return artists_route

@ttl_cache(ttl=REFRESH_TTL)
def get_song_route(artist_name: str, song_title: str) -> str:
    artist_route: str = get_artist_route(artist_name)
    songs_titles: list[str] = freemidiservice.get_song_titles(artist_route)
    songs_routes: list[str] = freemidiservice.get_song_routes(artist_route)
    songs: list[tuple[str, str]] = list(zip(songs_titles, songs_routes))
    find_index: int = generic_search(songs, lambda element: element[0] == song_title)
    title, song_route = songs[find_index]
    return song_route

@ttl_cache(ttl=REFRESH_TTL)
def get_download_route(artist_name: str, song_title: str) -> str:
    song_route: str = get_song_route(artist_name, song_title)
    return freemidiservice.get_download_route(song_route)

@ttl_cache(ttl=REFRESH_TTL)
def get_cookie(artist_name: str, song_title: str) -> str:
    song_route: str = get_song_route(artist_name, song_title)
    return freemidiservice.get_cookie(song_route)