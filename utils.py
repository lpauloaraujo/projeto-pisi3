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

    cores_generos = {
    'Drama': 'blue',
    'Documentário': 'blue',
    'Comédia': 'yellow',
    'Animação': 'orange',
    'Terror': 'black',
    'Romance': 'pink',
    'Música': 'black',
    'Suspense': 'grey',
    'Ação': 'red',
    'Crime': 'red',
    'Família': 'orange',
    'Filme de TV': 'purple',
    'Aventura': 'green',
    'Fantasia': 'purple',
    'Ficção Científica': 'grey',
    'Mistério': 'grey',
    'História': 'brown',
    'Guerra': 'red',
    'Faroeste': 'yellow'
    }

    cores_status = {
    'Lançado': 'green',
    'Rumor': 'red',
    'Pós-Produção': 'red',
    'Em Produção': 'red',
    'Planejado': 'red',
    'Cancelado': 'red'
    }

    if coluna == 'genres':
        cores = cores_generos
    elif coluna == 'status':
        cores = cores_status

    dados_separados = data_frame[coluna].str.split(', ').explode()
    aparicoes_dados = dados_separados.value_counts().sort_values(ascending=False)
    aparicoes_dados_df = aparicoes_dados.reset_index(name='Quantidade')

    fig = px.bar(
        data_frame=aparicoes_dados_df,
        x= 'Quantidade',
        y=coluna,
        title=titulo,
        color=coluna,  # Usar os valores do eixo y para definir as cores
        color_discrete_map=cores
    )

    fig.update_layout(
    xaxis=dict(
        title=None,  # Remove o título do eixo X
        tickfont=dict(
            color='black',
            size=14,
            family="Arial"
        )
    ),
    yaxis=dict(
        title=None,  # Remove o título do eixo Y
        tickfont=dict(
            color='black',
            size=10,
            family="Arial"
        )
    ),
    )
    

    return fig
def diagrama_pareto(data_frame, coluna, titulo):

    cores_linguas = {
    'Inglês': 'red',
    'Francês': 'blue',
    'Espanhol': 'yellow',
    'Japonês': 'blue',
    'Alemão': 'black',
    'Sem Idioma': 'grey',
    'Russo': 'brown',
    'Português': 'green',
    'Italiano': 'green',
    'Outros': 'grey'
    }

    cores_paises = {
    'EUA': 'red',
    'França': 'blue',
    'Reino Unido': 'red',
    'Alemanha': 'black',
    'Japão': 'blue',
    'Canadá': 'red',
    'India': 'orange',
    'Itália': 'green',
    'Brasil': 'green',
    'Espanha': 'yellow',
    'México': 'green',
    'China': 'red',
    'Russia': 'blue',
    'União Soviética': 'red',
    'Outros': 'grey'
    }

    if coluna == 'spoken_languages':
        cores = cores_linguas
    elif coluna == 'production_countries':
        cores = cores_paises

    #Contando as aparições de dados
    dados_separados = data_frame[coluna].str.split(', ').explode()
    aparicoes_dados = dados_separados.value_counts().sort_values(ascending=False)
    agrupado = aparicoes_dados.reset_index(name='Contagem')
    agrupado = agrupado.sort_values('Contagem', ascending=False)

    #Criando a série do somas acumulativas
    agrupado['Acumulado'] = agrupado['Contagem'].cumsum() / agrupado['Contagem'].sum() * 100

    #Criando a barra 'outros' após a linha atingir os 70%
    agrupado_principal = agrupado[agrupado['Acumulado'] <= 90]
    agrupado_outros = agrupado[agrupado['Acumulado'] > 90]
    outros_contagem = agrupado_outros['Contagem'].sum()
    linha_outros = pd.DataFrame({coluna: ['Outros'], 'Contagem': [outros_contagem], 'Acumulado': [100]})
    agrupado_principal = pd.concat([agrupado_principal, linha_outros], ignore_index=True)

    #Criando o diagrama em si
    fig = px.bar(
        agrupado_principal,
        y=coluna,
        x='Contagem',
        title=titulo,
        color=coluna,
        color_discrete_map=cores,
        labels={'Contagem': 'Contagem'})
    fig.add_scatter(
        y=agrupado_principal[coluna],
        x=agrupado_principal['Acumulado'],
        mode='lines+markers',
        name='Porcentagem',
        line=dict(color='#800080', width=2),
        xaxis='x2',
    )
    fig.update_layout(
    xaxis=dict(
        title=None,  # Remove o título do eixo X
        tickfont=dict(
            color='black',
            size=14,
            family="Arial"
        )
    ),
    yaxis=dict(
        title=None,  # Remove o título do eixo Y
        tickfont=dict(
            color='black',
            size=14,
            family="Arial"
        )
    ),
    xaxis2=dict(title=None, overlaying='x', side='top', showgrid=False),  # Remove título do segundo eixo
)

    return fig


def grafico_caixa(data_frame, coluna, titulo):
    fig = px.box(data_frame, y=coluna, title=titulo)
    return fig

def grafico_heatmap(data_frame, colunas, titulo):
    # Filtra o DataFrame para as colunas desejadas
    df_filtrado = data_frame[colunas]
    
    # Calcula a matriz de correlação (apenas numéricas)
    matriz_correlacao = df_filtrado.corr()
    
    # Cria o heatmap com um colorscale válido
    fig = px.imshow(
        matriz_correlacao,
        text_auto=True,  # Mostra os valores diretamente no gráfico
        title=titulo,
        color_continuous_scale="viridis"  # Substitua por outro esquema se desejar
    )
    return fig


