from cachetools.func import ttl_cache 

from curby.gather.controller import (
    musicbrainzcontroller
)
from curby.gather.service import (
    musicbrainzservice
)
from curby.core import (
    Song,
    REFRESH_TTL,
    generic_search
)

@ttl_cache(ttl=REFRESH_TTL)
def get_song(artist_name: str, song_title: str) -> Song:
    song = Song(song_title, artist_name)

    songs: list[tuple[str, str]] = musicbrainzcontroller.get_all_songs(artist_name)
    index: int = generic_search(songs, lambda element: element[0] == song_title)
    if index < len(songs):
        title, route = songs[index]
        song.genres = musicbrainzservice.get_song_genres(route)

    return song
