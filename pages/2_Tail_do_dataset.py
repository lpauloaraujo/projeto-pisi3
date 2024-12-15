import streamlit as st
from utils import carregar_dados, df_tail

df = carregar_dados("data/TMDB_movie_dataset_v11.parquet")
df_tratado = carregar_dados('data/TMDB_movie_dataset_v11_tratado2.parquet')

st.title("Tail do Dataset")
st.write("Os 5 últimos registros do dataset são:")
st.write(df_tail(df))

st.write('Os 5 últimos registros do dataset tratado são:')
st.write(df_tail(df_tratado))


