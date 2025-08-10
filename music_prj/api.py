from bst import Song
import requests
def search_song(query):
    url = f"https://api.deezer.com/search?q={query}"
    responce = requests.get(url)
    songs = []
    data = responce.json()
    for track in data['data'][:5]:
        title = track['title']
        artist = track['artist']['name']
        song_id = track['id']
        songs.append(Song(title,song_id,artist))
    return songs
def song_id(input1, input2): #artist and song title
    url = f"https://api.deezer.com/search?q={input1}+{input2}"
    responce = requests.get(url)
    songs = []
    data = responce.json()
    for track in data['data'][:5]:
        title = track['title']
        artist = track['artist']['name']
        song_id = track['id']
        songs.append(Song(title,song_id,artist))
    return songs
