import json
class BSTnode: #key is song.title
    def __init__(self, key, song):
        self.key = song.title
        self.song = song
        self.left = None
        self.right = None

class SongBST:
    def __init__(self):
        self.root = None
    def insert(self,song):
        def rec_insert(node,song):
            if node is None:
                return BSTnode(song.title, song)
            if song.title < node.key:
                node.left = rec_insert(node.left, song)
            elif song.title > node.key:
                node.right = rec_insert(node.right, song)
            return node
        self.root = rec_insert(self.root,song)
    def search(self,key):
        def rec_search(node,key):
            if node is None:
                return None
            if key == node.key: #figure
                return node.song
            elif key < node.key:
                return rec_search(node.left,key)
            else: 
                return rec_search(node.right,key)
        return rec_search(self.root,key)
    def delete(self,key):
        def rec_delete(node,key):
            if node is None:
                return None
            if node.key < key:
                node.left = rec_delete(node.left, key)
            elif key > node.key:
                node.right = rec_delete(node.right, key)
            else:
                if node.left is None:
                    return node.right
                elif node.right is None:
                    return node.left
            # Node has two children: find inorder successor
                succ = node.right
                while succ.left:
                    succ = succ.left
                node.key = succ.key
                node.song = succ.song
                node.right = rec_delete(node.right, succ.key)
            return node
        self.root = rec_delete(self.root, key)
    def in_order(self): #sorting title by alphabet
        result = []
        def rec_in_order(node):
            if node:
                rec_in_order(node.left)
                result.append(node.song)  # Or node.key if you only want titles
                rec_in_order(node.right)
        rec_in_order(self.root)
        return result
    def get_all_by_artist(self,artist_name):
        ans = []
        def rec_get_all_by_artist(node):
            if node:
                rec_get_all_by_artist(node.left)    #in order so uses alphabetical order also but doesn't matter
                if node.song.artist == artist_name:
                    ans.append(node.song)
                rec_get_all_by_artist(node.right)
        rec_get_all_by_artist(self.root)
        return ans
    def most_played(self, n):
        all_songs = self.in_order()
        all_songs.sort(key=lambda song: song.plays, reverse=True)
        return all_songs[:n]
    #persistance automated
    def save_library(self):
        songs = self.in_order()  # List of Song objects
        data = [song.to_dict() for song in songs]
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def load_library(self):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
            for song_data in data:
                self.insert(Song.from_dict(song_data), save=False)  # Avoid recursive saving
        except FileNotFoundError:
            print("No library file found, starting with an empty BST.")
