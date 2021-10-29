from spotipy.oauth2 import SpotifyClientCredentials  # To access authorised Spotify data
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'bfadfd7dc78b48a99f30b24fe2f1c65a'
client_secret = '742ce1eb8a3040bc80946ce9fdcd4652'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)  # spotify object to access API


artist_ids = []
artist_albums = []

album_name = []
album_id = []
artist_name = []
artist_id = []

track_name = []
track_id = []
track_artist_id = []
track_album_id = []
track_number = []
track_duration = []
track_genre = []


f = open("uris.txt", "r")
for id in f.readlines():
    artist_ids.append(id.strip('\n'))

for a_id in artist_ids:
    artist_albums.append(sp.artist_albums(a_id))

for albums in artist_albums:
   for i in range(len(albums['items']) // 6):
       album_name.append(albums['items'][i]['name'])
       album_id.append(albums['items'][i]['uri'])
       artist_name.append(albums['items'][i]['artists'][0]['name'])
       artist_id.append(albums['items'][i]['artists'][0]['uri'])

       tracks = sp.album_tracks(albums['items'][i]['uri'])
       for j in range(len(tracks['items'])):
           track_name.append(tracks['items'][j]['name'])
           track_id.append(tracks['items'][j]['uri'])
           track_artist_id.append(albums['items'][i]['artists'][0]['uri'])
           track_album_id.append(albums['items'][i]['uri'])
           track_number.append(tracks['items'][j]['track_number'])
           track_duration.append(tracks['items'][j]['duration_ms'])

df_albums = pd.DataFrame({'album_name':album_name,'album_id':album_id,'artist_name':artist_name,'artist_id':artist_id})
df_tracks = pd.DataFrame({'track_name':track_name,'track_id':track_id,'track_artist_id':track_artist_id,'track_album_id':track_album_id, 'track_number':track_number, 'track_duration':track_duration})
df_albums.drop_duplicates(subset=['album_name'], inplace=True)
df_tracks.drop_duplicates(subset=['track_id'], inplace=True)


df_albums.to_csv('albums.csv')
df_tracks.to_csv('tracks.csv')