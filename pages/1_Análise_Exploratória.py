import streamlit as st
import pandas as pd
from utils import carregar_dados, grafico_barras, diagrama_pareto

# Carregar os dados
df = carregar_dados("df_com_clusters_atualizados.parquet")

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

traducao_production_countries = {
    'United States of America': 'EUA',
    'France': 'França',
    'United Kingdom': 'Reino Unido',
    'Germany': 'Alemanha',
    'Japan': 'Japão',
    'Canada': 'Canadá',
    'India': 'India',
    'Italy': 'Itália',
    'Brazil': 'Brasil',
    'Spain': 'Espanha',
    'Mexico': 'México',
    'China': 'China',
    'Russia': 'Russia',
    'Soviet Union': 'União Soviética'
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

def traduzir_production_countries(genre_str, traducao):
    if pd.isna(genre_str):  # Verifica se é NaN
        return genre_str
    generos = genre_str.split(', ')  # Divide os gêneros em uma lista
    generos_traduzidos = [traducao.get(g, g) for g in generos]  # Traduz os gêneros
    return ', '.join(generos_traduzidos)

df['genres'] = df['genres'].apply(traduzir_generos, args=(traducao_generos,))

# df['status'] = df['status'].replace(traducao_status)

df['spoken_languages'] = df['spoken_languages'].apply(traduzir_spoken_languages, args=(traducao_spoken_language,))

df['production_countries'] = df['production_countries'].apply(traduzir_production_countries, args=(traducao_production_countries,))

# Título da aplicação
st.title("Gráficos")

# Gráfico de barras - Aparições de Gêneros
st.plotly_chart(grafico_barras(df, 'genres', 'Aparições de Gêneros'))
st.write("Após o tratamento não há mudanças significantes na ordem das colunas, a grande diferença é a diminuição do número de filmes como podemos observar no eixo 'Quantidade'")

# Gráfico de barras - Estado de lançamento das produções
# st.plotly_chart(grafico_barras(df, 'status', 'Estado de Lançamento das Produções'))
# st.write("Depois do tratamento é possível observar que não houveram mudanças significativas. Isto indica que o dataset segue útil para o estudo, visto que precisamos de dados sobre os resultados que os filmes obtiveram após seus lançamentos, dados esses que só os filmes que compõem a coluna 'Lançado' proporcionam.")

# Diagrama de Pareto - Envolvimento de países
st.plotly_chart(diagrama_pareto(df, 'production_countries', 'Envolvimento de Países nas Produções'))
st.write("""Após o tratamento, podemos observar que:\n - A quantidade de filmes com envolvimento do país 'Alemanha' ultrapassou as quantidades dos com envolvimento do país 'França' e 'Reino Unido'\n - A quantidade de filmes com o envolvimento do país 'Índia' ultrapassou a com o envolvimento do país 'Canadá'\n - As quantidades de filmes com o envolvimento do país 'Espanha' e do país 'México' ultrapassou o envolvimento do país 'Brasil'\n - Os países 'China' e 'Rússia' não aparecem mais no gráfico e o país 'União Soviética' apareceu.  """)

# Diagrama de Pareto - Distribuição de línguas faladas
st.plotly_chart(diagrama_pareto(df, 'spoken_languages', 'Distribuição de Línguas Faladas'))
st.write("Podemos observar que após o tratamento temos mais filmes onde a língua alemã é falada do que filmes onde a língua japonesa é falada. Também podemos perceber que os idiomas russo e português não aparecem mais e que o italiano apareceu.")