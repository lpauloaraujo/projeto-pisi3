import streamlit as st
from utils import carregar_dados

df = carregar_dados("data/TMDB_movie_dataset_v11.parquet")
df_tratado = carregar_dados('data/TMDB_movie_dataset_v11_tratado2.parquet')

st.title("Análises Categóricas")
st.write("Aqui estão as análises categóricas do dataset:")

# Pre tratamento
st.write("Análise da coluna 'status':")
st.write(df['status'].value_counts())

st.write("Análise da coluna 'genres':")
st.write(df['genres'].str.split(', ').explode().value_counts())

# Pos tratamento
st.write("Análise da coluna 'status' pos-tratamento:")
st.write(df_tratado['status'].value_counts())

st.write("Análise da coluna 'genres' pos-tratamento:")
st.write(df_tratado['genres'].str.split(', ').explode().value_counts())
