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
    artist_route: str = musicbrainzservice.get_route(artist_name)
    songs_titles: list[str] = musicbrainzservice.get_songs_titles(artist_route)
    songs_routes: list[str] = musicbrainzservice.get_songs_routes(artist_route)
    return list(zip(songs_titles, songs_routes))

@ttl_cache(ttl=REFRESH_TTL)
def get_artist_genres(artist_name: str) -> list[str]:
    artist_route: str = musicbrainzservice.get_route(artist_name)
    return musicbrainzservice.get_artist_genres(artist_route)

@ttl_cache(ttl=REFRESH_TTL)
def get_song_genres(artist_name: str, song_title: str) -> list[tuple[str, str]]:
    artist_route: str = musicbrainzservice.get_route(artist_name)
    songs_titles: list[str] = musicbrainzservice.get_songs_titles(artist_route)
    songs_routes: list[str] = musicbrainzservice.get_songs_routes(artist_route)
    songs: list[tuple[str, str]] = list(zip(songs_titles, songs_routes))
    search_index: int = generic_search(songs, lambda element: element[0] == song_title)
    title, route = songs[search_index]
    return musicbrainzservice.get_song_genres(route)

