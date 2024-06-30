import os
import numpy as np

from PIL import (
    Image, 
    ImageDraw, 
    ImageFont
)
from moviepy.Clip import Clip
from moviepy.editor import (
    concatenate_videoclips,
    concatenate_audioclips,
    VideoFileClip, 
    AudioFileClip, 
    ImageClip
)
from sponsorblock import Segment, Client
from youtubesearchpython import VideosSearch
from pytube import YouTube

from curby.core import (
    Song,
    FrameMetadata,
    Stack,
    TEMP_FOLDER
)

def remove_sponsors(clip: Clip, sponsors: list[Segment]):
    segments = Stack()
    first_segment = sponsors[0]
    segments.push((first_segment.start, first_segment.end))
    for index in range(1, len(sponsors)):
        current_segment = sponsors[index]
        last_segment = segments.peek()
        if current_segment.start < last_segment[1]:
            segments.pop()
            segments.push((last_segment[0], current_segment.end))
        else:
            segments.push((current_segment.start, current_segment.end))
    last_segment = segments.peek()
    if (last_segment[1] < clip.duration):
        segments.push((clip.duration, clip.duration))
    parts = []
    for index in range(len(segments.items) - 1):
        current_segment = segments.items[index]
        next_segment = segments.items[index + 1]
        parts.append(clip.subclip(current_segment[1], next_segment[0]))
    if (isinstance(clip, AudioFileClip)):
        return concatenate_audioclips(parts)
    elif (isinstance(clip, VideoFileClip)):
        return concatenate_videoclips(parts)
    else:
        print("Type of clip unsupported")

def search_video(search_text: str):
    videos_search = VideosSearch(search_text, limit=1)
    results = videos_search.result()
    return results['result'][0]['id']

def download_audio(url: str, save_as: str):
    temp_fullpath: str = os.path.join(".\\", TEMP_FOLDER)
    if not os.path.exists(temp_fullpath):
        os.makedirs(temp_fullpath)

    audio_filename: str = "{filename}.mp3".format(filename=save_as)
    audio_filepath: str = os.path.join(TEMP_FOLDER, audio_filename)
    if os.path.exists(audio_filepath):
        print("Skiping audio download : file already exist")
    else:
        youtube = YouTube(url)
        audio_stream = youtube.streams.filter(only_audio=True).first()
        audio_stream.download(output_path=TEMP_FOLDER, filename=audio_filename)
    return audio_filepath

def create_frame_section(frame_np: np.ndarray, audio_clip: AudioFileClip):
    image_clip = ImageClip(frame_np, duration=audio_clip.duration)
    return image_clip.set_audio(audio_clip)

def generate_audio(search_text: str) -> AudioFileClip:
    client = Client()
    video_id: str = search_video(search_text)
    audio_filepath: str = download_audio(f"https://www.youtube.com/watch?v={video_id}", search_text)
    audio_clip = AudioFileClip(audio_filepath)
    sponsors: list = [] #client.get_skip_segments(video_id,  SPONSOR_CATEGORIES)
    if (sponsors is not None and len(sponsors) > 0):
        audio_clip = remove_sponsors(audio_clip, sponsors)
    return audio_clip

def generate_image(frame: FrameMetadata, songs: list[Song], selected_song: Song):
    image = Image.new('RGB', (frame.width, frame.height), color=frame.background_color)
    canvas = ImageDraw.Draw(image)

    song_height = frame.height * 0.02
    song_font = ImageFont.truetype(frame.font_name, size=int(song_height))

    max_width = max(canvas.textlength(song.get_display_name(frame.higligth_key + frame.format_model), song_font) for song in songs)

    pos_x = frame.width - max_width - (frame.width * 0.025)
    
    title_height = frame.height * 0.1
    title_font = ImageFont.truetype(frame.font_name, size=int(title_height))
    
    pos_y = frame.height * 0.1
    canvas.text((pos_x, pos_y), "Songs", font=title_font, fill=frame.song_title_color)
    pos_y += frame.height * 0.12

    for song in songs:
        format = frame.format_model
        color = frame.song_color
        delta = 0
        
        if song.title == selected_song.title:
            format = frame.higligth_key + frame.format_model
            color = frame.song_higligth_color
            delta = canvas.textlength(frame.higligth_key, song_font)

        canvas.text((pos_x - delta, pos_y), song.get_display_name(format), font=song_font, fill=color)
        pos_y += song_height + (song_height // 2)
    
    return image

def generate_compilation(metadata: FrameMetadata, songs: list[Song]):
    frames = []
    for song in songs:
        search: str = song.get_display_name("{title} by {author}")
        
        frame_image: Image = generate_image(metadata, songs, song)
        audio_clip: AudioFileClip = generate_audio(search)

        frame_section = create_frame_section(np.array(frame_image), audio_clip)
        frames.append(frame_section)

    compilation_fullpath = "{filename}.mp4".format(filename="final")
    compilation_clip = concatenate_videoclips(frames, method="compose")
    compilation_clip.write_videofile(compilation_fullpath, codec = "libx264", threads = 1, fps = 24)
    compilation_clip.close()
    for frame in frames:
        frame.close()
    return compilation_fullpath
    