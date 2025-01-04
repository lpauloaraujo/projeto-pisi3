import streamlit as st
from utils import carregar_dados
import pandas as pd


df = carregar_dados('data/TMDB_movie_dataset_v11_tratado2.parquet')
colunas = [col for col in df.columns if col != 'title']  # Remove 'title' da lista de seleção

colunas_escolhidas = st.multiselect('Selecione as colunas que deseja visualizar:', colunas)

colunas_escolhidas = ['title'] + colunas_escolhidas 

if colunas_escolhidas:
    tabela = df[colunas_escolhidas]

    ordenar_por_receita = st.checkbox('Ordenar por receita', value=False) 
    ordenar_por_media_das_notas = st.checkbox('Ordenar por media das notas', value=False)

    if ordenar_por_receita:
        # Ordena a tabela pela coluna 'revenue', se a checkbox for marcada
        tabela = tabela.assign(revenue=df['revenue']).sort_values(by='revenue', ascending=False)

    if ordenar_por_media_das_notas:

         tabela = tabela.assign(vote_average=df['vote_average']).sort_values(by='vote_average', ascending=False)
    

    st.dataframe(tabela)
    
else:
    st.write("Nenhuma coluna selecionada.")