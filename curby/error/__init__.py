from dataclasses import dataclass

@dataclass
class BillboardError(Exception):
    pass

@dataclass
class FreeMidiError(Exception):
    pass

@dataclass
class MusicBrainzError(Exception):
    pass

@dataclass
class ArtistBinderError(Exception):
    pass

@dataclass
class SongBinderError(Exception):
    pass