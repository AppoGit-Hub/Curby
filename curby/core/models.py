from dataclasses import dataclass, field
from threading import Thread
from enum import Enum
from typing import Callable

from pydantic import BaseModel

@dataclass
class Artist:
    name: str
    genres: list[str]

@dataclass
class Song:
    title: str
    author: str
    genres: list[str] = field(default_factory=list)

    def get_display_name(self, format: str):
        return f"{self.title} by {self.author}"

@dataclass
class FrameMetadata(BaseModel): 
    width: int
    height: int
    font_name: str
    background_color: tuple
    song_title_color: tuple
    song_higligth_color: tuple
    song_color: tuple
    format_model: str
    higligth_key: str

class TaskStatus(Enum):
    QUEUED = 0
    PROCESSING = 2
    FINISHED = 3

class SongCompilationThread(Thread):
    def __init__(self, callback, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.callback: Callable = callback
    
    def run(self):
        super().run()
        self.callback()

@dataclass
class SongCompilationTask:
    task_id: str
    status: TaskStatus
    thread: SongCompilationThread