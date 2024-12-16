import pandas as pd
import plotly.express as px
import streamlit as st


#criar as funções de carregamentos de dados
@st.cache_data
def carregar_dados(dataset):
    dados = pd.read_parquet(dataset)
    dados = dados[dados['adult'] == False]
    return dados

def df_head(data_frame):
    return data_frame.head()

def df_tail(data_frame):
    return data_frame.tail()

def grafico_barras(data_frame, coluna, titulo):

    cores_generos = {'Drama': 'blue',
    'Documentário': 'blue',
    'Comédia':'yellow',
    'Animação': 'yellow',
    'Terror': 'black',
    'Romance': 'red',
    'Música': 'purple',
    'Suspense': 'grey',
    'Ação': 'red',
    'Crime': 'red',
    'Família': 'green',
    'Filme de TV': 'purple',
    'Aventura': 'yellow',
    'Fantasia': 'green',
    'Ficção Científica': 'blue',
    'Mistério': 'grey',
    'História': 'purple',
    'Guerra': 'red',
    'Faroeste': 'yellow'}

    if coluna == 'genres':
        cores = cores_generos

    dados_separados = data_frame[coluna].str.split(', ').explode()
    aparicoes_dados = dados_separados.value_counts().sort_values(ascending=False)
    aparicoes_dados_df = aparicoes_dados.reset_index(name='Quantidade')
    fig = px.bar(
        data_frame=aparicoes_dados_df,
        x= coluna,
        y='Quantidade',
        title=titulo,
        color=coluna,  # Usar os valores do eixo X para definir as cores
        color_discrete_map=cores
    )

    fig.update_layout(
        xaxis_title=coluna,
        yaxis_title="Quantidade",
        xaxis_tickangle=45  # Define os rótulos na horizontal (ajuste conforme necessário)
    )
    return fig


def diagrama_pareto(data_frame, coluna, titulo):
    #Contando as aparições de dados
    dados_separados = data_frame[coluna].str.split(', ').explode()
    aparicoes_dados = dados_separados.value_counts().sort_values(ascending=False)
    agrupado = aparicoes_dados.reset_index(name='Contagem')
    agrupado = agrupado.sort_values('Contagem', ascending=False)

    #Criando a série do somas acumulativas
    agrupado['Acumulado'] = agrupado['Contagem'].cumsum() / agrupado['Contagem'].sum() * 100

    #Criando a barra 'outros' após a linha atingir os 70%
    agrupado_principal = agrupado[agrupado['Acumulado'] <= 70]
    agrupado_outros = agrupado[agrupado['Acumulado'] > 70]
    outros_contagem = agrupado_outros['Contagem'].sum()
    linha_outros = pd.DataFrame({coluna: ['Outros'], 'Contagem': [outros_contagem], 'Acumulado': [100]})
    agrupado_principal = pd.concat([agrupado_principal, linha_outros], ignore_index=True)

    #Criando o diagrama em si
    fig = px.bar(agrupado_principal, x=coluna, y='Contagem', title=titulo, labels={'Contagem': 'Contagem'})
    fig.add_scatter(
        x=agrupado_principal[coluna],
        y=agrupado_principal['Acumulado'],
        mode='lines+markers',
        name='Porcentagem',
        line=dict(color='red', width=2),
        yaxis='y2',
    )
    fig.update_layout(
        yaxis2=dict(title="Porcentagem (%)", overlaying='y', side='right', showgrid=False),
        margin=dict(l=40, r=40, t=40, b=40),
    )
    return fig
