import streamlit as st
import pandas as pd
from utils import carregar_dados, grafico_barras, diagrama_pareto

# Carregar os dados
df = carregar_dados("data/TMDB_movie_dataset_v11_tratado2.parquet")

# Dicionário para traduzir os gêneros
traducao_generos = {
    'Drama': 'Drama',
    'Documentary': 'Documentário',
    'Comedy': 'Comédia',
    'Animation': 'Animação',
    'Horror': 'Terror',
    'Romance': 'Romance',
    'Music': 'Música',
    'Thriller': 'Suspense',
    'Action': 'Ação',
    'Crime': 'Crime',
    'Family': 'Família',
    'TV Movie': 'Filme de TV',
    'Adventure': 'Aventura',
    'Fantasy': 'Fantasia',
    'Science Fiction': 'Ficção Científica',
    'Mystery': 'Mistério',
    'History': 'História',
    'War': 'Guerra',
    'Western': 'Faroeste'
}

traducao_status = {
    'Released': 'Lançado',
    'Rumored': 'Rumor',
    'Post Production': 'Pós-Produção',
    'In Production': 'Em Produção',
    'Planned': 'Planejado'
}

traducao_spoken_language = {
    'English': 'Inglês',
    'French': 'Francês',
    'Spanish': 'Espanhol',
    'Japanese': 'Japonês',
    'German': 'Alemão',
    'No Language': 'Sem Idioma',
    'Russian': 'Russo',
    'Portuguese': 'Português',

}

# Função para traduzir os gêneros corretamente
def traduzir_generos(genre_str, traducao):
    if pd.isna(genre_str):  # Verifica se é NaN
        return genre_str
    generos = genre_str.split(', ')  # Divide os gêneros em uma lista
    generos_traduzidos = [traducao.get(g, g) for g in generos]  # Traduz os gêneros
    return ', '.join(generos_traduzidos)  # Junta os gêneros traduzidos de volta

def traduzir_spoken_languages(genre_str, traducao):
    if pd.isna(genre_str):  # Verifica se é NaN
        return genre_str
    generos = genre_str.split(', ')  # Divide os gêneros em uma lista
    generos_traduzidos = [traducao.get(g, g) for g in generos]  # Traduz os gêneros
    return ', '.join(generos_traduzidos)  # Junta os gêneros traduzidos de volta


df['genres'] = df['genres'].apply(traduzir_generos, args=(traducao_generos,))

df['status'] = df['status'].replace(traducao_status)

df['spoken_languages'] = df['spoken_languages'].apply(traduzir_spoken_languages, args=(traducao_spoken_language,))

# Título da aplicação
st.title("Gráficos")

# Gráfico de barras - Aparições de Gêneros
st.plotly_chart(grafico_barras(df, 'genres', 'Aparições de Gêneros'))

# Gráfico de barras - Estado de lançamento das produções
st.plotly_chart(grafico_barras(df, 'status', 'Estado de Lançamento das Produções'))

# Diagrama de Pareto - Envolvimento de países
st.plotly_chart(diagrama_pareto(df, 'production_countries', 'Envolvimento de Países nas Produções'))

# Diagrama de Pareto - Distribuição de línguas faladas
st.plotly_chart(diagrama_pareto(df, 'spoken_languages', 'Distribuição de Línguas Faladas'))