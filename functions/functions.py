import spotipy
import spotipy.util as util
import pandas as pd
import os
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import numpy as np

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def extract_user_playlist(url):
    # Split the url and use Spotipy to retrieve the track information for each song in the playlist
    playlist_url = url.split("/")[4].split("?")[0]
    playlist_tracks = sp.playlist_tracks(playlist_url)

    # For loop to extract the necessary track information
    track_ids = []
    track_titles = []
    track_artist = []
    track_album_art = []
    track_album_url = []

    for track in playlist_tracks['items']:
        track_ids.append(track['track']['id'])
        track_titles.append(track['track']['name'])
        track_album_art.append(track['track']['album']['images'][2]['url'])
        track_album_url.append(track['track']['album']['external_urls']['spotify'])
        artist_list = []
        for artist in track['track']['artists']:
            artist_list.append(artist['name'])
        track_artist.append(artist_list[0])

    # Create a dataframe from the track_ids to bring in features
    features = sp.audio_features(track_ids)

    features_df = pd.DataFrame(data=features, columns=features[0].keys())
    features_df['title'] = track_titles
    features_df['artist'] = track_artist
    features_df['album_art'] = track_album_art
    features_df['album_url'] = track_album_url
    features_df = features_df[['artist','title','album_url','album_art','id','danceability','energy','loudness','speechiness','acousticness','liveness','valence']]
    
    return features_df

def song_chooser(url):

    user_df = extract_user_playlist(url)
    clean_df = user_df[['acousticness', 'danceability', 'energy','liveness', 'loudness', 'speechiness', 'valence', 'title']]

    user_avg_scores = clean_df.mean(axis=0)
    search_variable = clean_df.idxmax()

    distance = []
    for index, row in clean_df.iterrows():
        point1 = user_avg_scores[search_variable]
        point2 = np.array(row[search_variable])
        dist = np.linalg.norm(point1 - point2)
        distance.append(dist)
    clean_df[f'distance_for_{search_variable}'] = distance
    clean_df.set_index('song_name', inplace= True)
    song_search = clean_df['distance_for_energy'].idxmin()
    return song_search