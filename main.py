import streamlit as st
import pickle
import pandas as pd
import requests
import time
import gdown
import os

# Download pkl files from Google Drive if not present

gdown.download('https://drive.google.com/uc?id=1m5L--sfbYyxBYmhPEa3K26dJbU5D-jSo', 'movies.pkl', quiet=False, fuzzy=True)
gdown.download('https://drive.google.com/uc?id=1cI0fAwV2YVm6qlg6JtJXrvTe8TCXGjA1', 'similarity_compressed.pkl', quiet=False, fuzzy=True)

movies = pd.DataFrame(pickle.load(open('movies.pkl', 'rb')))
session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})

def fetch_poster(movie_id):
    for attempt in range(3):
        try:
            response = session.get(
                'https://api.themoviedb.org/3/movie/{}?api_key=adeb800e6df23bd435913e9a1d4100dc&language=en-US'.format(movie_id),
                timeout=30
            )
            data = response.json()
            if 'poster_path' in data and data['poster_path']:
                return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
            else:
                return "https://via.placeholder.com/500"
        except:
            time.sleep(1)
    return "https://via.placeholder.com/500"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
        time.sleep(1)

    return recommended_movies, recommended_movies_posters
movies = pd.DataFrame(pickle.load(open('movies.pkl', 'rb')))

similarity = pickle.load(open('similarity_compressed.pkl', 'rb'))

st.title('🎬 Movie Recommender System')

option = st.selectbox('Choose a movie to recommend', movies['title'].values)

if st.button('Recommend'):
    with st.spinner('Finding recommendations...'):
        name, poster = recommend(option)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(name[0])
        st.image(poster[0])
    with col2:
        st.text(name[1])
        st.image(poster[1])
    with col3:
        st.text(name[2])
        st.image(poster[2])
    with col4:
        st.text(name[3])
        st.image(poster[3])
    with col5:
        st.text(name[4])
        st.image(poster[4])

        # Ye hai abhi
        movies = pickle.load(open('movies.pkl', 'rb'))

        # Ye karo
