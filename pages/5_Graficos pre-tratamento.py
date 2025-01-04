import streamlit as st
import pandas as pd
from utils import carregar_dados, grafico_barras, diagrama_pareto

df = carregar_dados("data/TMDB_movie_dataset_v11.parquet")

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
    'Planned': 'Planejado',
    'Canceled': 'Cancelado'
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

df['status'] = df['status'].replace(traducao_status)

df['spoken_languages'] = df['spoken_languages'].apply(traduzir_spoken_languages, args=(traducao_spoken_language,))

df['production_countries'] = df['production_countries'].apply(traduzir_production_countries, args=(traducao_production_countries,))

# Título da aplicação
st.title("Gráficos")

# Gráfico de barras - Estado de lançamento das produções
st.plotly_chart(grafico_barras(df, 'status', 'Estado de Lançamento das Produções'))
st.write("O gráfico apresenta visualmente o estado em que os filmes registrados no dataset se encontram. O resultado demonstra que a imensa maioria dos registros se encontram na categoria de já lançados, o que possibilita o estudo visto que são precisos dados sobre os resultados obtidos pelos filmes.")

# Gráfico de barras - Aparições de Gêneros
st.plotly_chart(grafico_barras(df, 'genres', 'Aparições de Gêneros'))
st.write("O gráfico permite observar a quantidade de vezes que cada gênero aparece no dataset para que seja possível entender melhor a distribuição desses dados.")

# Diagrama de Pareto - Envolvimento de países
st.plotly_chart(diagrama_pareto(df, 'production_countries', 'Envolvimento de Países nas Produções'))
st.write("O gráfico demonstra, através de um diagrama de Pareto, que o dataset utilizado possui um grande número de filmes com o envolvimento do país EUA (Estados Unidos da América) em suas produções, com uma grande diferença de quantidade em relação aos outros países. Em seguida, temos França, Reino Unido, Alemanha e Japão com números parecidos, seguidos pelos outros países. A coluna “Outros” ter um tamanho elevado indica que o dataset é bastante variado em países envolvidos nas produções, visto que ela é formada por uma grande quantidade de países que possuem, relativamente, poucas produções.")

# Diagrama de Pareto - Distribuição de línguas faladas
st.plotly_chart(diagrama_pareto(df, 'spoken_languages', 'Distribuição de Línguas Faladas'))
st.write("A Figura 4 explica a quantidade de filmes onde determinada língua é falada, através de um diagrama de Pareto. É possível observar a predominância do inglês.")
