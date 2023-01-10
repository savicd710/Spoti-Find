from flask import Flask, render_template, redirect, url_for, request
import os
import json
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from functions.functions import extract_user_playlist
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
    # Interacting with the user on the html side
    URL = request.form['URL']

    # Extract the songs from the user input playlist
    user_playlist = extract_user_playlist(URL)

    return render_template('recommendations.html', user_playlist=user_playlist)


# debugger to edit while running
if __name__ == "__main__":
    app.run(debug=True)
