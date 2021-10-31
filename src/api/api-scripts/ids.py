from spotipy.oauth2 import SpotifyClientCredentials  # To access authorised Spotify data
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'bfadfd7dc78b48a99f30b24fe2f1c65a'
client_secret = ''
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)  # spotify object to access API


artists = []
f = open("artists.txt", "r")
dest = open("uris_dest.txt", "w")
for line in f.readlines():
    artists.append(line.strip('\n'))

for artist in artists:
    result = sp.search(artist)
    dest.write(result['tracks']['items'][0]['artists'][0]['uri'])
    dest.write('\n')

f.close()
dest.close()
