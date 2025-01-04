import streamlit as st
from utils import carregar_dados, grafico_heatmap, grafico_caixa
import pandas as pd

df = carregar_dados("data/TMDB_movie_dataset_v11_tratado2.parquet")

st.plotly_chart(grafico_heatmap(df, ['revenue', 'budget', 'popularity','vote_count'], 'correlação entre colunas numericas' ))

# box plot - vote_average
st.plotly_chart(grafico_caixa(df, 'vote_average', 'media de votos'))