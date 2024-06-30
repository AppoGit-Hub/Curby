from curby.core import FrameMetadata, Song
from curby.gather.binder import get_song
from curby.gather.service import billboardservice
from curby.generate import generate_compilation

theme = FrameMetadata(
    1920, 
    1080, 
    "arial.ttf", 
    (0, 0, 128), 
    (173, 216, 230), 
    (152, 255, 152), 
    (173, 216, 230), 
    "{title} - {author}", 
    "> "
)

songs: list[tuple[str, str]] = billboardservice.get_popular()
all_songs: list[Song] = []
for author, title in songs:
    try:
        all_songs.append(get_song(author, title))
    except Exception as error:
        print(f"Error: {author} - {title} | {error}")

generate_compilation(theme, all_songs)