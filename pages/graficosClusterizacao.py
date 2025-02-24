import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Função para carregar os dados
def carregar_dados(filepath):
    return pd.read_parquet(filepath)

# Função para plotar gráfico de barras
def grafico_barras(cluster, data, coluna, qtd):
    contagem = data.groupby(coluna).size()
    top_10_contagem = contagem.nlargest(qtd)
    top_10_contagem = top_10_contagem.sort_values(ascending=True)
    fig = px.bar(top_10_contagem, x=top_10_contagem.values, y=top_10_contagem.index, title=f"{coluna} mais presentes no cluster {cluster}", labels={"x": "Contagem", coluna: coluna})
    return fig

# Carregar os dados
dataset = carregar_dados("dataset_com_clusters.parquet")

# Explorando os clusters provenientes do KModes (clusterização dos dados categóricos)
cores_cinema = ["#1B1B1B", "#D90429", "#FFD700", "#FFAA33", "#A2A2A2", "#001F3F", "#8B4513", "#F5C518", "#5A5A5A", "#B22222"]

cluster0kmodes = dataset[dataset['cluster'] == 0]
cluster1kmodes = dataset[dataset['cluster'] == 1]
cluster2kmodes = dataset[dataset['cluster'] == 2]
cluster3kmodes = dataset[dataset['cluster'] == 3]
cluster4kmodes = dataset[dataset['cluster'] == 4]
cluster5kmodes = dataset[dataset['cluster'] == 5]

# Título da aplicação
st.title("Visualização de Gráficos de Clusterização")

# Selecionar o cluster para visualização
cluster_selecionado = st.selectbox("Selecione o Cluster", ["0", "1", "2", "3", "4", "5"])

# Selecionar o tipo de gráfico
tipo_grafico = st.selectbox("Selecione o Tipo de Gráfico", ["Gêneros", "Línguas Faladas", "Países de Produção"])

# Plotar o gráfico correspondente
if tipo_grafico == "Gêneros":
    if cluster_selecionado == "0":
        fig = grafico_barras('0', cluster0kmodes, 'genres', 5)
    elif cluster_selecionado == "1":
        fig = grafico_barras('1', cluster1kmodes, 'genres', 5)
    elif cluster_selecionado == "2":
        fig = grafico_barras('2', cluster2kmodes, 'genres', 5)
    elif cluster_selecionado == "3":
        fig = grafico_barras('3', cluster3kmodes, 'genres', 5)
    elif cluster_selecionado == "4":
        fig = grafico_barras('4', cluster4kmodes, 'genres', 5)
    elif cluster_selecionado == "5":
        fig = grafico_barras('5', cluster5kmodes, 'genres', 5)
elif tipo_grafico == "Línguas Faladas":
    if cluster_selecionado == "0":
        fig = grafico_barras('0', cluster0kmodes, 'spoken_languages', 8)
    elif cluster_selecionado == "1":
        fig = grafico_barras('1', cluster1kmodes, 'spoken_languages', 8)
    elif cluster_selecionado == "2":
        fig = grafico_barras('2', cluster2kmodes, 'spoken_languages', 8)
    elif cluster_selecionado == "3":
        fig = grafico_barras('3', cluster3kmodes, 'spoken_languages', 8)
    elif cluster_selecionado == "4":
        fig = grafico_barras('4', cluster4kmodes, 'spoken_languages', 8)
    elif cluster_selecionado == "5":
        fig = grafico_barras('5', cluster5kmodes, 'spoken_languages', 8)
elif tipo_grafico == "Países de Produção":
    if cluster_selecionado == "0":
        fig = grafico_barras('0', cluster0kmodes, 'production_countries', 8)
    elif cluster_selecionado == "1":
        fig = grafico_barras('1', cluster1kmodes, 'production_countries', 8)
    elif cluster_selecionado == "2":
        fig = grafico_barras('2', cluster2kmodes, 'production_countries', 8)
    elif cluster_selecionado == "3":
        fig = grafico_barras('3', cluster3kmodes, 'production_countries', 8)
    elif cluster_selecionado == "4":
        fig = grafico_barras('4', cluster4kmodes, 'production_countries', 8)
    elif cluster_selecionado == "5":
        fig = grafico_barras('5', cluster5kmodes, 'production_countries', 8)

st.plotly_chart(fig)