import os
import numpy as np
import pandas as pd

from sklearn.metrics.pairwise import sigmoid_kernel
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import preprocessing

import warnings
warnings.filterwarnings("ignore")

data = pd.read_csv("../Spoti-Find/data/updated_music.csv")
data.drop(columns='Unnamed: 0',inplace=True)

feature_cols=['acousticness', 'danceability', 'duration_ms', 'energy',
            'instrumentalness', 'key', 'liveness', 'loudness', 'mode',
            'speechiness', 'tempo', 'time_signature', 'valence']

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
normalized_df =scaler.fit_transform(data[feature_cols])

# Create a pandas series with song titles as indices and indices as series values 
indices = pd.Series(data.index, index=data['song_name']).drop_duplicates()

# Create cosine similarity matrix based on given matrix
cosine = cosine_similarity(normalized_df)

def generate_recommendation(song_name, model_type=cosine ):
    """
    Purpose: Function for song recommendations 
    Inputs: song title and type of similarity model
    Output: Pandas series of recommended songs
    """
    # Get song indices
    index=indices[song_name]
    # Get list of songs for given songs
    score=list(enumerate(model_type[index]))
    # Sort the most similar songs
    similarity_score = sorted(score,key = lambda x:x[1],reverse = True)
    # Select the top-10 recommend songs
    similarity_score = similarity_score[1:21]
    top_songs_index = [i[0] for i in similarity_score]
    # Top 10 recommende songs
    top_songs=data['song_name'].iloc[top_songs_index]
    return top_songs
