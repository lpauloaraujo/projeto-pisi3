import streamlit as st

st.set_page_config(
    page_title="Análise Exploratória de Dados TMDB",
    layout="wide",
)

st.title("Análise Explorátoria")
st.write(
    """
    Este aplicativo viza realizar análises exploratórias no dataset 
    "TMDB_movie_dataset_v11", que contém informações detalhadas sobre produções de filmes. 
    Utilize o menu lateral para navegar entre as páginas.
    """
)
