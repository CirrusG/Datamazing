import random

from spotipy.oauth2 import SpotifyClientCredentials  # To access authorised Spotify data
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_id = 'bfadfd7dc78b48a99f30b24fe2f1c65a'
client_secret = '1e8e21bd6250416980e16c9bf7893f4f'
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)  # spotify object to access API

artist_ids = []
artist_albums = []

album_name = []
release_date = []
album_id = []
artist_name = []
artist_id = []

track_name = []
track_id = []
track_artist_id = []
track_artist_name = []
track_album_id = []
track_album_name = []
track_number = []
track_duration = []
track_genre = []
track_release_date = []

features_album_id = []
features_song_id = []
features_track_number = []

f = open("uris.txt", "r")
for id in f.readlines():
    artist_ids.append(id.strip('\n'))

for a_id in artist_ids:
    artist_albums.append(sp.artist_albums(a_id))

artist_counter = 0
for albums in artist_albums:
    current_artist_id = artist_ids[artist_counter]
    print(current_artist_id)
    possible_genres = sp.artist(current_artist_id)['genres']
    num_genres = len(possible_genres)

    for i in range(len(albums['items']) // 6):
        album_name.append(albums['items'][i]['name'])
        album_id.append(albums['items'][i]['uri'])
        artist_name.append(albums['items'][i]['artists'][0]['name'])
        artist_id.append(albums['items'][i]['artists'][0]['uri'])
        release_date.append(albums['items'][i]['release_date'])

        tracks = sp.album_tracks(albums['items'][i]['uri'])
        for j in range(len(tracks['items'])):
            track_name.append(tracks['items'][j]['name'])
            track_id.append(tracks['items'][j]['uri'])
            track_artist_id.append(albums['items'][i]['artists'][0]['uri'])
            track_artist_name.append(albums['items'][i]['artists'][0]['name'])
            track_album_id.append(albums['items'][i]['uri'])
            track_album_name.append(albums['items'][i]['name'])
            track_number.append(tracks['items'][j]['track_number'])
            track_duration.append(tracks['items'][j]['duration_ms'])
            track_release_date.append(albums['items'][i]['release_date'])

            # decide on a random genre to set for this song
            if(num_genres > 0):
                genreChoice = random.randint(0, num_genres - 1)
                track_genre.append(possible_genres[genreChoice])
            else:
                track_genre.append('NULL')

            features_album_id.append(albums['items'][i]['uri'])
            features_song_id.append(tracks['items'][j]['uri'])
            features_track_number.append(tracks['items'][j]['track_number'])
    artist_counter = artist_counter + 1

df_albums = pd.DataFrame(
    {'album_name': album_name, 'album_id': album_id, 'artist_name': artist_name, 'artist_id': artist_id,
     'release_date': release_date})
df_tracks = pd.DataFrame({'track_name': track_name, 'track_id': track_id, 'track_artist_id': track_artist_id, 'track_artist_name': track_artist_name,
                          'track_album_id': track_album_id, 'track_album_name': track_album_name, 'track_number': track_number,
                          'track_duration': track_duration, 'track_genre': track_genre, 'track_release_date': track_release_date})
df_features = pd.DataFrame(
    {'features_album_id': features_album_id, 'features_song_id':features_song_id,
     'features_track_number': features_track_number }
)

df_albums.drop_duplicates(subset=['album_name'], inplace=True)
df_tracks.drop_duplicates(subset=['track_id'], inplace=True)
df_features.drop_duplicates(subset=['features_album_id', 'features_song_id'], inplace=True)

df_tracks.to_csv('tracks.csv')