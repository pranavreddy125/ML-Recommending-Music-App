# bst.py — BST keyed by song.song_id (string)
# Same structure as before, but comparisons now use song_id instead of title.

import json
from song import Song  # make sure song.py is in your module path

class BSTNode:
    def __init__(self, key, song):
        self.key = str(key)   # song_id (string)
        self.song = song      # the actual Song object
        self.left = None
        self.right = None

class SongBST:
    def __init__(self, filename="library.json"):
        self.root = None
        self.filename = filename

    # INSERT (recursive)
    def insert(self, song):
        # key is song_id; we store the Song
        def rec_insert(node, song):
            if node is None:
                return BSTNode(song.song_id, song)
            if song.song_id < node.key:
                node.left = rec_insert(node.left, song)
            elif song.song_id > node.key:
                node.right = rec_insert(node.right, song)
            else:
                # same id → replace existing song record
                node.song = song
            return node
        self.root = rec_insert(self.root, song)

    # SEARCH (recursive, by key = song_id)
    def find(self, song_id):
        key = str(song_id)
        def rec_search(node, key):
            if node is None:
                return None
            if key == node.key:
                return node.song
            elif key < node.key:
                return rec_search(node.left, key)
            else:
                return rec_search(node.right, key)
        return rec_search(self.root, key)

    # DELETE (recursive, by key = song_id)
    def delete(self, song_id):
        key = str(song_id)
        def rec_delete(node, key):
            if node is None:
                return None, False
            # compare key vs node.key in the same direction as search
            if key < node.key:
                node.left, removed = rec_delete(node.left, key)
                return node, removed
            elif key > node.key:
                node.right, removed = rec_delete(node.right, key)
                return node, removed
            else:
                # found node to delete
                if node.left is None and node.right is None:
                    return None, True
                if node.left is None:
                    return node.right, True
                if node.right is None:
                    return node.left, True
                # Node has two children: find inorder successor
                succ_parent = node
                succ = node.right
                while succ.left:
                    succ_parent = succ
                    succ = succ.left
                # copy successor's data into current node
                node.key = succ.key
                node.song = succ.song
                # delete successor from right subtree
                if succ_parent.left is succ:
                    succ_parent.left, _ = rec_delete(succ_parent.left, succ.key)
                else:
                    succ_parent.right, _ = rec_delete(succ_parent.right, succ.key)
                return node, True
        self.root, _ = rec_delete(self.root, key)

    def inorder(self):  # sorting by song_id
        result = []
        def rec_inorder(node):
            if node:
                rec_inorder(node.left)
                result.append(node.song)  # Or node.key if you only want ids
                rec_inorder(node.right)
        rec_inorder(self.root)
        return result

    def get_all_by_artist(self, artist_name):
        ans = []
        def rec_get_all_by_artist(node):
            if node:
                rec_get_all_by_artist(node.left)
                if node.song.artist == artist_name:
                    ans.append(node.song)
                rec_get_all_by_artist(node.right)
        rec_get_all_by_artist(self.root)
        return ans

    def most_played(self, n):
        all_songs = self.inorder()
        all_songs.sort(key=lambda song: song.plays, reverse=True)
        return all_songs[:n]

    # persistence automated
    '''
    whole tree (entire library of songs) is saved/loaded at once
    '''
    def save_library(self):
        songs = self.inorder()  # List of Song objects
        data = [song.to_dict() for song in songs]  # turn each song into dict
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)  # put into .json

    def load_library(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:  # open json and reverse the process
                data = json.load(f)
            for song_data in data:
                self.insert(Song.from_dict(song_data))
        except FileNotFoundError:
            print("No library file found, starting with an empty BST.")
