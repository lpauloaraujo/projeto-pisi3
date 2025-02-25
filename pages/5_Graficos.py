import streamlit as st
from utils import carregar_dados, grafico_barras, diagrama_pareto

df = carregar_dados("data/TMDB_movie_dataset_v11.parquet")

st.title("Gráficos")
st.plotly_chart(grafico_barras(df, 'genres', 'Aparições de Gêneros'))
st.plotly_chart(grafico_barras(df, 'status', 'Estado de lançamento das produções'))
st.plotly_chart(diagrama_pareto(df, 'production_countries', 'Envolvimento de países nas produções'))
st.plotly_chart(diagrama_pareto(df, 'spoken_languages', 'Distribuição de Línguas Faladas'))
