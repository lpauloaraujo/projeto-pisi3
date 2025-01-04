import streamlit as st
from utils import carregar_dados

df = carregar_dados("data/TMDB_movie_dataset_v11.parquet")
df_tratado = carregar_dados('data/TMDB_movie_dataset_v11_tratado2.parquet')

st.title("Estatísticas Numéricas")
st.write("Aqui estão as estatísticas descritivas do dataset:")
st.write(df.describe())

st.write("Aqui estão as estatísticas descritivas do dataset já tratado:")
st.write(df_tratado.describe())
