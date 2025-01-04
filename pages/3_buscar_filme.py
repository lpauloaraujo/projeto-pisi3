import streamlit as st
from utils import carregar_dados
import pandas as pd

# Carregar os dados
df = carregar_dados('data/TMDB_movie_dataset_v11_tratado2.parquet')

# Título da interface
st.title('Mecanismo de Busca de Filme')

# Campo de entrada para o usuário digitar o título do filme
titulo_busca = st.text_input('Digite o título do filme:')

# Verifica se o título foi digitado
if titulo_busca:
    # Filtra o dataset para buscar o título (fazendo a busca insensível a maiúsculas/minúsculas)
    resultado_busca = df[df['title'].str.contains(titulo_busca, case=False, na=False)]

    if not resultado_busca.empty:
        # Filtra os resultados para excluir os filmes onde revenue, budget, vote_count e vote_average são todos menores ou iguais a 1
        resultado_filtrado = resultado_busca[
            ~((resultado_busca['revenue'] <= 1) &
              (resultado_busca['budget'] <= 1) &
              (resultado_busca['vote_count'] <= 1) &
              (resultado_busca['vote_average'] <= 1))
        ]

        if not resultado_filtrado.empty:
            # Se encontrar o filme com dados válidos, exibe os dados desejados
            st.write(f"Resultados encontrados para '{titulo_busca}':")
            st.write(resultado_filtrado[['title', 'revenue', 'budget', 'vote_count', 'popularity', 'vote_average']])
        else:
            # Caso não encontre filmes válidos
            st.write(f"Não há filmes com dados válidos para o título '{titulo_busca}'.")
    else:
        # Caso não encontre nenhum filme com o título fornecido
        st.write(f"Não foi encontrado nenhum filme com o título '{titulo_busca}'.")
