import streamlit as st
from utils import carregar_dados

df = carregar_dados("data/TMDB_movie_dataset_v11.parquet")

st.title("Análises Categóricas")
st.write("Aqui estão as análises categóricas do dataset:")

st.write("Análise da coluna 'status':")
st.write(df['status'].value_counts())

st.write("Análise da coluna 'genres':")
st.write(df['genres'].str.split(', ').explode().value_counts())
