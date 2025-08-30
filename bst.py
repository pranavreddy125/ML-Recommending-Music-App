# bst_titles.py — BST keyed by song.title (alphabetical)
# Keeps your comments and overall structure, just fixes logic/typos.

import json
from song import Song  # make sure song.py is in your module path

class BSTNode:
    def __init__(self, key, song):
        self.key = key        # song.title (string)
        self.song = song      # the actual Song object
        self.left = None
        self.right = None

class SongBSTByTitle:
    def __init__(self, filename="library.json"):
        self.root = None
        self.filename = filename

    # INSERT (recursive)
    def insert(self, song):
        # keep: key is title; we store the Song
        def rec_insert(node, song):
            if node is None:
                return BSTNode(song.title, song) 
            if song.title < node.key:
                node.left = rec_insert(node.left, song)
            elif song.title > node.key:
                node.right = rec_insert(node.right, song)
            else:
                # same title → replace existing song record
                node.song = song
            return node
        self.root = rec_insert(self.root, song)

    # SEARCH (recursive, by key = title)
    def search(self, key):
        def rec_search(node, key):
            if node is None:
                return None
            if key == node.key:  # figure
                return node.song
            elif key < node.key:
                return rec_search(node.left, key)
            else:
                return rec_search(node.right, key)
        return rec_search(self.root, key)

    # DELETE (recursive, by key = title)
    def delete(self, key):
        def rec_delete(node, key):
            if node is None:
                return None
            # compare key vs node.key in the same direction as search
            if key < node.key:
                node.left = rec_delete(node.left, key)
                return node
            elif key > node.key:
                node.right = rec_delete(node.right, key)
                return node
            else:
                # found node to delete
                if node.left is None and node.right is None:
                    return None
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
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
                    succ_parent.left = rec_delete(succ_parent.left, succ.key)
                else:
                    succ_parent.right = rec_delete(succ_parent.right, succ.key)
                return node
        self.root = rec_delete(self.root, key)

    def in_order(self):  # sorting title by alphabet
        result = []
        def rec_in_order(node):
            if node:
                rec_in_order(node.left)
                result.append(node.song)  # Or node.key if you only want titles
                rec_in_order(node.right)
        rec_in_order(self.root)
        return result

    def get_all_by_artist(self, artist_name):
        ans = []
        def rec_get_all_by_artist(node):
            if node:
                rec_get_all_by_artist(node.left)    # in order so uses alphabetical order also but doesn't matter
                if node.song.artist == artist_name:
                    ans.append(node.song)
                rec_get_all_by_artist(node.right)
        rec_get_all_by_artist(self.root)
        return ans

    def most_played(self, n):
        all_songs = self.in_order()
        all_songs.sort(key=lambda song: song.plays, reverse=True)
        return all_songs[:n]

    # persistence automated
    '''
    whole tree (entire library of songs) is saved/loaded at once
    '''
    def save_library(self):
        songs = self.in_order()  # List of Song objects
        data = [song.to_dict() for song in songs] #turn each song into dict
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False) #put into .json

    def load_library(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f: #open json and reverse the process
                data = json.load(f)
            for song_data in data:
                self.insert(Song.from_dict(song_data))
        except FileNotFoundError:
            print("No library file found, starting with an empty BST.")
