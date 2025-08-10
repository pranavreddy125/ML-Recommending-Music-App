import json
import os
from bst import SongBST
from song import Song

class SongLibrary:
    def __init__(self, storage_file="library.json"):
        self.storage_file = storage_file
        self.bst = SongBST()
        self.load_library() #if alr saved data it fills it in

    def load_library(self):
        """Load songs from JSON to the BST"""
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as f:
                try:
                    data = json.load(f)
                    for song_data in data:
                        song = Song.from_dict(song_data)
                        self.bst.insert(song)
                except json.JSONDecodeError:
                    print("Warning: library.json is empty or corrupted.")
        else:
            # Create empty file if it doesn't exist
            with open(self.storage_file, "w") as f:
                json.dump([], f)

    def save_library(self):
        """Save all songs from BST to JSON."""
        songs = self.bst.in_order()
        data = [song.to_dict() for song in songs]
        with open(self.storage_file, "w") as f:
            json.dump(data, f, indent=4)

    def add_song(self, song):
        self.bst.insert(song)
        self.save_library()

    def delete_song(self, title):
        self.bst.delete(title)
        self.save_library()

    def search_song(self, title):
        return self.bst.search(title)

    def get_all_by_artist(self, artist_name):
        return self.bst.get_all_by_artist(artist_name)

    def get_most_played(self, n):
        return self.bst.most_played(n)

    def play_song(self, title):
        song = self.bst.search(title)
        if song:
            song.plays += 1 #increments for a 'play'
            self.save_library()
            return song
        return None
