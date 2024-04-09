import streamlit as st
import pickle

# Load data functions
def load_data(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

# Recommendation function
def recommend(movie, movies_list, similarity):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    sorted_movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies, recommended_posters = [], []
    for i in sorted_movie_list:
        movie_title = movies_list.iloc[i[0]].title
        poster_path = movies_list.iloc[i[0]]['poster_path']
        full_poster_path = "https://image.tmdb.org/t/p/original" + poster_path

        recommended_movies.append(movie_title)
        recommended_posters.append(full_poster_path)

    return recommended_movies, recommended_posters

# Set Streamlit theme with dark and galaxy theme
def set_theme():
    st.set_page_config(
        page_title="Movie Recommender System",
        page_icon="🎥",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'Get Help': 'https://www.streamlit.io',
            'Report a bug': "https://github.com",
            'About': "# This is a movie recommendation app. Enjoy!"
        }
    )

    # Custom CSS for dark and galaxy theme and animated title
    st.markdown("""
        <style>
        .main {
           background-color: #0e1117;
           background-image: url("https://www.transparenttextures.com/patterns/stardust.png");
        }
        h1 {
           color: #c2c5cc;
           background-color: #151a21;
           padding: 10px;
           border-radius: 10px;
           text-align: center;
           animation: glow 2s ease-in-out infinite alternate;
        }
        @keyframes glow {
            from {
              text-shadow: 0 0 10px #00e6e6, 0 0 20px #00e6e6, 0 0 30px #00e6e6, 0 0 40px #00e6e6, 0 0 50px #00e6e6, 0 0 60px #00e6e6, 0 0 70px #00e6e6;
            }
            to {
              text-shadow: 0 0 20px #00ace6, 0 0 30px #00ace6, 0 0 40px #00ace6, 0 0 50px #00ace6, 0 0 60px #00ace6, 0 0 70px #00ace6, 0 0 80px #00ace6;
            }
        }
        </style>
        """, unsafe_allow_html=True)

# Load the data
movies_list = load_data("movies.pkl")
similarity = load_data("similarity.pkl")

# Streamlit UI
def streamlit_ui():
    st.title("🌌 Project Movie Recommender System 🌌")
    movies_list_title = movies_list['title'].values
    selected_movie_name = st.selectbox("Type or select a movie from the dropdown", movies_list_title)

    if st.button("Recommend"):
        recommendation, movie_posters = recommend(selected_movie_name, movies_list, similarity)

        cols = st.columns(5)
        for i, col in enumerate(cols):
            with col:
                st.write(recommendation[i])
                st.image(movie_posters[i])

# Run the Streamlit UI with theme
if __name__ == '__main__':
    set_theme()  # Setting theme
    streamlit_ui()
