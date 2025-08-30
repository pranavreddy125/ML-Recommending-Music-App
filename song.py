class Song:
    """A single track"""
    def __init__(self, song_id, title, artist, album="", genres=None, duration=0,
                 plays=0, rank=0, bpm=None):
        if song_id is None:
            raise ValueError("song_id cannot be None")
        self.song_id = str(song_id)   # use string keys for consistancy
        self.title = title or "" #default to empty str if empty
        self.artist = artist or ""

        # extra data
        self.album = album or ""
        self.genres = list(genres) if genres is not None else []  # avoid shared lists
        self.duration = int(duration)  # seconds
        self.plays = int(plays)
        self.rank = int(rank)          # Deezer popularity proxy
        self.bpm = int(bpm) if bpm is not None and bpm != "" else None

    # the key we will store in the BST
    def key(self):
        return self.song_id

    # ---------- helpers for saving/loading ----------
    def to_dict(self):
        """Turn this object into plain JSON-safe data."""
        return {
            "song_id": self.song_id,
            "title": self.title,
            "artist": self.artist,
            "album": self.album,
            "genres": list(self.genres),
            "duration": self.duration,
            "plays": self.plays,
            "rank": self.rank,
            "bpm": self.bpm,
        }

    @classmethod
    def from_dict(cls, data):
        """Create a Song back from a dict. Missing fields fall back to defaults."""
        return cls(
            song_id=str(data.get("song_id")),
            title=data.get("title", ""),
            artist=data.get("artist", ""),
            album=data.get("album", ""),
            genres=data.get("genres", []),
            duration=data.get("duration", 0),
            plays=data.get("plays", 0),
            rank=data.get("rank", 0),
            bpm=data.get("bpm", None),
        )


    def __repr__(self):
        return f"Song(id={self.song_id}, title={self.title!r}, artist={self.artist!r})"

    def __eq__(self, other): #operator overloading
        return isinstance(other, Song) and self.song_id == other.song_id
