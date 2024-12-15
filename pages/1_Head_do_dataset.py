import streamlit as st
from utils import carregar_dados, df_head

df = carregar_dados("data/TMDB_movie_dataset_v11.parquet")
df_tratado = carregar_dados('data/TMDB_movie_dataset_v11_tratado2.parquet')

st.title("Head do Dataset")
st.write("Os 5 primeiros registros do dataset são:")
st.write(df_head(df))

st.write("Os 5 primeiros registros do dataset tratado são:")
st.write(df_head(df_tratado))
