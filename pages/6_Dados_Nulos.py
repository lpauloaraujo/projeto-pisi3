import streamlit as st
from utils import carregar_dados

df = carregar_dados("data/TMDB_movie_dataset_v11.parquet")

st.title("Dados Nulos")
st.write("Aqui está a quantidade de valores nulos em cada coluna:")
st.write(df.isnull().sum())
