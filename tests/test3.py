from curby.gather.service import billboardservice, freemidiservice, musicbrainzservice
from curby.gather.controller import billboardcontroller, freemidicontroller, musicbrainzcontroller
from curby.gather.binder import artistbinder, songbinder

"""
print(billboardservice.get_songs_authors(3))
print(billboardservice.get_songs_titles(3))

print(freemidiservice.get_names("a"))
print(freemidiservice.get_routes("a"))
print(freemidiservice.get_song_routes('artist-1886-a-flock-of-seagulls'))
print(freemidiservice.get_cookie('artist-1886-a-flock-of-seagulls'))
print(freemidiservice.get_song_titles('artist-1191-a-dub'))

print(billboardcontroller.get_popular(3))

print(freemidicontroller.get_artist_route("ariana grande"))
print(freemidicontroller.get_song_route("ariana grande", "pov"))
print(freemidicontroller.get_download_route("ariana grande", "pov"))
print(freemidicontroller.get_cookie("ariana grande", "pov"))
"""

"""
print(musicbrainzservice.get_artist_route("ariana grande"))
print(musicbrainzservice.get_artist_genres("/artist/f4fdbb4c-e4b7-47a0-b83b-d91bbfcfa387"))
print(musicbrainzservice.get_songs_titles("/artist/f4fdbb4c-e4b7-47a0-b83b-d91bbfcfa387"))
print(musicbrainzservice.get_songs_routes("/artist/f4fdbb4c-e4b7-47a0-b83b-d91bbfcfa387"))
print(musicbrainzservice.get_song_genres("/release-group/1237b040-fb8f-4f23-8000-fb6909486c83"))
"""

"""
print(musicbrainzcontroller.get_all_songs(("ariana grande")))
print(musicbrainzcontroller.get_artist_genres(("ariana grande")))
print(musicbrainzcontroller.get_song_genres("ariana grande", "my everything"))
"""

print(artistbinder.get_artist("ariana grande"))
print(songbinder.get_song("ariana grande", "my everything"))