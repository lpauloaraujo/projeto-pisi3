import streamlit as st
from utils import carregar_dados, df_head

df = carregar_dados("data/TMDB_movie_dataset_v11.parquet")

st.title("Head do Dataset")
st.write("Os 5 primeiros registros do dataset são:")
st.write(df_head(df))
