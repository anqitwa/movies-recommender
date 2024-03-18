import streamlit as st
import pickle
import pandas as pd
import requests

mov_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(mov_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))
api_key = st.secrets['API_KEY']

def fetch_poster(movie_id):
    url = fr'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'
    resp = requests.get(url)
    data = resp.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']

def release_year(movie_id):
    url = fr'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US'
    resp = requests.get(url)
    data = resp.json()
    return (data['release_date'])[:4]

def recommend(movie):
    movie_idx = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_idx]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        movie_title = movies.iloc[i[0]].title
        movie_year = release_year(movie_id)
        recommended_movies.append(f"{movie_title} ({movie_year})")
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


st.set_page_config(
    page_title="Movie Suggestions",
    page_icon=":clapper:",
    layout="wide",  # Wide layout to accommodate multiple columns
    initial_sidebar_state="auto",
)

# Set background color and overall styling
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
        color: #FFFFFF;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title('Movie Suggestions')

selected_movie = st.selectbox('Pick one!', movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5, gap='medium')
    with col1:
        st.write(names[0])
        st.image(posters[0], use_column_width=True)
    with col2:
        st.write(names[1])
        st.image(posters[1], use_column_width=True)
    with col3:
        st.write(names[2])
        st.image(posters[2], use_column_width=True)
    with col4:
        st.write(names[3])
        st.image(posters[3], use_column_width=True)
    with col5:
        st.write(names[4])
        st.image(posters[4], use_column_width=True)

