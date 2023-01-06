from flask import Flask, render_template, redirect, url_for, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import json
import pandas as pd
import os

from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(
    client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

app = Flask(__name__)

@app.route('/')
def echo():
    return render_template('index.html')

@app.route('/playlist')
def playlist():
    return render_template('playlist.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/recommendations', methods=['POST'])
def recommendations():
    def extract_user_playlist(url):
        # Split the url and use Spotipy to retrieve the track information for each song in the playlist
        playlist_url = url.split("/")[4].split("?")[0]
        playlist_tracks = sp.playlist_tracks(playlist_url)

        # For loop to extract the necessary track information
        track_ids = []
        track_titles = []
        track_artist = []

        for track in playlist_tracks['items']:
            track_ids.append(track['track']['id'])
            track_titles.append(track['track']['name'])
            artist_list = []
            for artist in track['track']['artists']:
                artist_list.append(artist['name'])
            track_artist.append(artist_list[0])

        # Create a dataframe from the track_ids to bring in features
        features = sp.audio_features(track_ids)

        features_df = pd.DataFrame(data=features, columns=features[0].keys())
        features_df['title'] = track_titles
        features_df['artist'] = track_artist
        features_df = features_df[['artist','title','id','danceability','energy','loudness','speechiness','acousticness','liveness','valence']]
        
        return features_df

    # Interacting with the user on the html side
    URL = request.form['URL']

    temp_df = extract_user_playlist(URL)

    return render_template('recommendations.html', temp_df=temp_df)

#debugger to edit while running
if __name__ == "__main__":
    app.run(debug=True)