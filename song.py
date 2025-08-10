class Song:
    def __init__(self,title, song_id, artist, plays = 0):
        self.title = title
        self.song_id = song_id
        self.artist = artist
        self.plays = plays
    def __str__(self):
        return f"{self.title} by {self.artist} (ID: {self.song_id})"
    
    def to_dict(self): #store songs into json
        return {
            "title": self.title,
            "song_id": self.song_id,
            "artist": self.artist,
            "plays": self.plays
        }

    @classmethod #creates obj instead of needing one bc dont have a Song obj yet
    def from_dict(cls, data):   #make bst from saved data
        return cls(
            title=data["title"],
            song_id=data["song_id"],
            artist=data["artist"],
            plays=data.get("plays", 0)
        )