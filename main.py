import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth


ask_user_date = input("Which year do you want to travel? Type the date in this format: YYYY-MM-DD: ")

URL = f"https://www.billboard.com/charts/hot-100/{ask_user_date}"

response = requests.get(url=URL)
music_page = response.text
soup = BeautifulSoup(music_page, "html.parser")
songs = soup.select("div li ul li h3")
song_list = [song.getText().strip() for song in songs]

client_id = "id"
secret_id = "secret_id"
scope = "playlist-modify-private"
redirect_uri = "http://example.com"
username = "name"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=secret_id,
                                               redirect_uri=redirect_uri,
                                               scope=scope,
                                               show_dialog=True,
                                               cache_path="token.txt",
                                               username=username))
user_id = sp.current_user()["id"]

year = ask_user_date.split("-")[0]
uri_list = []
for song in song_list:
    result = sp.search(q=f"track:{song} year:{year}", type='track')
    try:
        uri = result['tracks']['items'][0]['uri']
        uri_list.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

print(uri_list)
playlist = sp.user_playlist_create(user=user_id,public=False, name=f"{year} Billboard Songs")
sp.playlist_add_items(playlist_id=playlist["id"], items=uri_list)
