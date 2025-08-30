# song_library.py — wrapper around BST keyed by song_id + JSON persistence
# Switched API to use song_id everywhere (more stable than titles).

import json
import os
from bst import SongBST        # this BST should be keyed by song.song_id
from song import Song

class SongLibrary:
    def __init__(self, storage_file="library.json"):
        self.storage_file = storage_file
        # ensure parent folder exists (e.g., data/library.json)
        parent = os.path.dirname(self.storage_file)
        if parent and not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)
        self.bst = SongBST()
        self.load_library()  # if already saved data it fills it in

    def load_library(self): #same fn as bst but with error handling and insert w/o saving each time
        """Load songs from JSON to the BST"""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    print("Warning: library.json is empty or corrupted.")
                    data = []
            for song_data in data:
                try:
                    song = Song.from_dict(song_data)
                    if song and song.song_id is not None:
                        self.bst.insert(song)  # keyed by song_id under the hood
                except Exception:
                    continue
        else:
            # Create empty file if it doesn't exist
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4, ensure_ascii=False)

    def save_library(self):
        """Save all songs from BST to JSON."""
        songs = self.bst.inorder()  # List of Song objects (sorted by song_id)
        data = [song.to_dict() for song in songs]
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def add_song(self, song: Song):
        self.bst.insert(song)
        self.save_library()

    def delete_song(self, song_id: str):
        self.bst.delete(str(song_id))
        self.save_library()

    def search_song(self, song_id: str):
        return self.bst.find(str(song_id))

    # convenience helpers staying the same
    def get_all_by_artist(self, artist_name: str):
        return self.bst.inorder() if artist_name == "*" else [
            s for s in self.bst.inorder() if s.artist == artist_name
        ]

    def get_most_played(self, n: int):
        all_songs = self.bst.inorder()
        all_songs.sort(key=lambda song: song.plays, reverse=True)
        return all_songs[:n]

    def play_song(self, song_id: str):
        song = self.bst.find(str(song_id))
        if song:
            song.plays = int(song.plays) + 1  # increments for a 'play'
            # replace stored node value to be safe (same key)
            self.bst.insert(song)
            self.save_library()
            return song
        return None
