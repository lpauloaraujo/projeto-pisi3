import streamlit as st
from utils import carregar_dados

df = carregar_dados("data/TMDB_movie_dataset_v11.parquet")

st.title("Estatísticas Numéricas")
st.write("Aqui estão as estatísticas descritivas do dataset:")
st.write(df.describe())
