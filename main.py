import streamlit as st
import pickle
import numpy as np
import pandas as pd
import requests
import time

# --- Page Config ---
st.set_page_config(page_title="Movie Recommender", page_icon="🎬", layout="wide")

# --- Custom CSS ---
st.markdown("""
    <style>
    body { background-color: #0f0f0f; }
    .stApp { background-color: #0f0f0f; color: #ffffff; }
    .main-title { text-align: center; font-size: 2.5rem; color: #e50914; font-weight: bold; margin-bottom: 0.2rem; }
    .sub-title { text-align: center; color: #aaaaaa; margin-bottom: 2rem; }
    .login-box { background-color: #1a1a1a; padding: 2rem; border-radius: 12px; max-width: 400px; margin: auto; }
    .movie-title { text-align: center; font-size: 0.85rem; color: #dddddd; margin-top: 0.4rem; }
    .stButton>button { background-color: #e50914; color: white; border: none; border-radius: 8px; padding: 0.5rem 2rem; font-size: 1rem; width: 100%; }
    .stButton>button:hover { background-color: #b20710; }
    .stSelectbox label { color: #aaaaaa; }
    </style>
""", unsafe_allow_html=True)

# --- Load Data ---
movies = pickle.load(open('movies_small.pkl', 'rb'))
similarity = np.load('similarity.npz')['similarity']

session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})

# --- Fetch Poster ---
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

# --- Recommend ---
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

# --- Login Page ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown('<div class="main-title">🎬 Movie Recommender</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Discover movies you\'ll love</div>', unsafe_allow_html=True)

    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown('<div class="login-box">', unsafe_allow_html=True)
            st.markdown("### Welcome 👋")
            st.markdown("Enter your details to continue")
            name = st.text_input("Your Name", placeholder="John Doe")
            email = st.text_input("Email", placeholder="john@gmail.com")
            if st.button("Get Started →"):
                if name and email:
                    st.session_state.logged_in = True
                    st.session_state.user_name = name
                    st.rerun()
                else:
                    st.error("Please fill in both fields!")
            st.markdown('</div>', unsafe_allow_html=True)

# --- Main App ---
else:
    st.markdown(f'<div class="main-title">🎬 Movie Recommender</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="sub-title">Welcome, {st.session_state.user_name}! 👋</div>', unsafe_allow_html=True)

    option = st.selectbox('Choose a movie', movies['title'].values)

    if st.button('Recommend 🎬'):
        with st.spinner('Finding recommendations...'):
            name, poster = recommend(option)

        col1, col2, col3, col4, col5 = st.columns(5)
        for col, title, img in zip([col1, col2, col3, col4, col5], name, poster):
            with col:
                st.image(img, use_column_width=True)
                st.markdown(f'<div class="movie-title">{title}</div>', unsafe_allow_html=True)