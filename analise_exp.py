#importar as bibliotecas
import streamlit as st
import pandas as pd
import plotly.express as px

#criar as funções de carregamentos de dados
@st.cache_data
def carregar_dados(dataset):
    dados = pd.read_parquet(dataset)
    dados = dados[dados['adult'] == False]
    return dados

def df_head(data_frame):
    st.header("5 primeiros registros do dataset")
    st.write(data_frame.head())

def df_tail(data_frame):
    st.header("5 últimos registros do dataset")
    st.write(data_frame.tail())

def analise_categorica(data_frame, coluna, modo):
    if modo == 'combinados':
        agrupado = data_frame.groupby([coluna]).size()
        agrupado = agrupado.sort_values(ascending = False)
        st.write(agrupado)
    else:
        dados_separados = data_frame[coluna].str.split(', ').explode()
        aparicoes_dados = dados_separados.value_counts().sort_values(ascending = False)
        st.write(aparicoes_dados)

def grafico_barras(data_frame, coluna):
    st.header(f"Gráfico de barras sobre a coluna '{coluna}'")
    dados_separados = data_frame[coluna].str.split(', ').explode()
    aparicoes_dados = dados_separados.value_counts().sort_values(ascending = False)
    aparicoes_dados_df = aparicoes_dados.reset_index(name = 'Quantidade')
    fig = px.bar(data_frame = aparicoes_dados_df, x = coluna, y = 'Quantidade', title = 'Gráfico')
    return fig

def dados_nulos(data_frame):
    st.header("Dados em falta por coluna")
    st.write(data_frame.isnull().sum())

def analise_exploratoria():
#preparar as visualizações
    df = carregar_dados("data/TMDB_movie_dataset_v11.parquet")

    #criar a interface do streamlit
    st.title("Análise Exploratória")
    st.write('Essa é uma aplicação dedicada à análise exploratória do dataset "TMDB_movies_dataset_v11", que possui cerca de 1 milhão de registros.')

    st.sidebar.title("Navegação")
    opcoes = st.sidebar.radio("Sessões", options=[
    'Página Inicial', 
    'Head do dataset',
    'Tail do dataset',
    'Análises Categóricas',
    'Estatísticas Numéricas',
    'Gráficos',
    'Dados Nulos'
    ])

    if opcoes == 'Head do dataset':
        df_head(df)

    elif opcoes == 'Tail do dataset':
        df_tail(df)

    elif opcoes == 'Análises Categóricas':
        st.header("Análises dos dados categóricos presentes no dataset")
        analise_categorica(df, 'status', '')
        analise_categorica(df, 'genres', 'combinados')
        analise_categorica(df, 'genres', 'separados')
        analise_categorica(df, 'production_companies', 'combinados')
        analise_categorica(df, 'production_companies', 'separados')
        analise_categorica(df, 'production_contries', 'combinados')
        analise_categorica(df, 'production_contries', 'separados')
        analise_categorica(df, 'spoken_languages', 'combinados')
        analise_categorica(df, 'spoken_languages', 'separados')
        analise_categorica(df, 'keywords', 'combinados')
        analise_categorica(df, 'keywords', 'separados')

    elif opcoes == 'Estatísticas Numéricas':
        st.write(df.describe())

    elif opcoes == 'Gráficos':
        st.plotly_chart(grafico_barras(df, 'genres'))
        st.plotly_chart(grafico_barras(df, 'status'))

    elif opcoes == 'Dados Nulos':
        dados_nulos(df)

if __name__ == '__main__':
    analise_exploratoria()
