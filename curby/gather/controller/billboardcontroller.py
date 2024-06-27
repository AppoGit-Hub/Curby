from cachetools.func import ttl_cache 

from curby.gather.service import (
    billboardservice
)
from curby.core import (
    REFRESH_TTL
)

@ttl_cache(ttl=REFRESH_TTL)
def get_popular(max_songs: int = 1) -> list[tuple[str, str]]:
    song_authors: list[str] = billboardservice.get_songs_authors(max_songs)
    song_titles: list[str] = billboardservice.get_songs_titles(max_songs)
    return list(zip(song_authors, song_titles))