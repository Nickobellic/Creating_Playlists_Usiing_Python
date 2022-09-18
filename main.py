import requests
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
from spotipy.client import Spotify

user = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{user}/")
data = response.text
all_songs = BeautifulSoup(data, "html.parser")
list_of_songs = all_songs.find_all(name="h3", id="title-of-a-story")

top_songs = []
for song in list_of_songs:
    s = song.text.strip()
    if s != "Songwriter(s):":
        if s != "Producer(s):":
            if s != "Imprint/Promotion Label:":
                 top_songs.append(s)

top_100_songs = [ f"{top_songs[i]}" for i in range(3,103)]

SPOTIFY_CLIENT_ID = "<client-id>"
SPOTIFY_CLIENT_SECRET = "<secret-id>"


scope = "playlist-modify-private"
t = Spotify(auth_manager=SpotifyOAuth(
    scope="playlist-modify-private",
    redirect_uri="https://open.spotify.com/user/31qhwsnwns3jx6f4zum4ez3nwwfq",
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    show_dialog=True,
    cache_path="token.txt"
))

user_id = t.current_user()['id']
song_uris = []

for i in top_100_songs:
    try:
        result = t.search(q=f"track:{i} year:{user[0:4]}", type="track", limit=1)
        song_uris.append(result['tracks']['items'][0]['uri'])
    # result['tracks']['items'][0]['album']['id']
    except:
        continue

playlist = t.user_playlist_create(user=user_id,name=f"{user} Billboard 100", public=False, description="Birthday present for You, Sweety ❤😘")
PLAYLIST_ID = playlist['id']

add_tracks =t.playlist_add_items(playlist_id=PLAYLIST_ID, items=song_uris)
print(add_tracks)
