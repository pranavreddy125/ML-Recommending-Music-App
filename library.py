# song_library.py — wrapper around your title-keyed BST + JSON persistence
import json
import os
from bst import SongBST        # your BST with in_order/search/delete by title
from song import Song

class SongLibrary:
    def __init__(self, storage_file="library.json"):
        self.storage_file = storage_file
        # ensure the parent folder exists (if user passes paths like data/library.json)
        parent = os.path.dirname(self.storage_file)
        if parent and not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)

        self.bst = SongBST()
        self.load_library()  # if already saved, fill the BST in

    def load_library(self):
        """Load songs from JSON to the BST"""
        if os.path.exists(self.storage_file):
            # read as utf-8 and tolerate empty/corrupt files
            with open(self.storage_file, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    print("Warning: library.json is empty or corrupted.")
                    data = []

            # data should be a list of dicts; skip bad rows safely
            for song_data in data:
                try:
                    song = Song.from_dict(song_data)
                    # avoid inserting Nones or broken rows
                    if song and song.title is not None:
                        self.bst.insert(song)
                except Exception:
                    continue
        else:
            # Create empty file if it doesn't exist
            with open(self.storage_file, "w", encoding="utf-8") as f:
                json.dump([], f, indent=4, ensure_ascii=False)

    def save_library(self):
        """Save all songs from BST to JSON."""
        songs = self.bst.in_order()  # List of Song objects
        data = [song.to_dict() for song in songs]
        # write as utf-8; pretty print
        with open(self.storage_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def add_song(self, song: Song):
        """Insert (or replace same-title) then persist."""
        self.bst.insert(song)
        self.save_library()

    def delete_song(self, title: str):
        """Delete by title (BST is keyed by title) then persist."""
        self.bst.delete(title)
        self.save_library()

    def search_song(self, title: str):
        """Find a song by exact title key."""
        return self.bst.search(title)

    def get_all_by_artist(self, artist_name: str):
        """Return a list of all songs where song.artist == artist_name."""
        return self.bst.get_all_by_artist(artist_name)

    def get_most_played(self, n: int):
        """Top-N by .plays (descending)."""
        return self.bst.most_played(n)

    def play_song(self, title: str):
        """Increment the play count of a song and persist."""
        song = self.bst.search(title)
        if song:
            song.plays = int(song.plays) + 1  # increments for a 'play'
            # since the node stores the same object reference, no need to re-insert
            self.save_library()
            return song
        return None
