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
    genres: list[str] = musicbrainzcontroller.get_artist_genres(artist_name)
    return Artist(artist_name, genres)