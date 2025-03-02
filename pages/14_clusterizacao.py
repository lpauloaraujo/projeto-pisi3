#Análise exploratória dos resultados da clusterização
#Importando bibliotecas
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import streamlit as st

# Função para carregar os dados
def carregar_dados(filepath):
    return pd.read_parquet(filepath)

#Carregando dados
dataset = pd.read_parquet("df_com_clusters_atualizados.parquet")

#Explorando os clusters provenientes do KModes (clusterização dos dados categóricos)
cores_cinema = ["#1B1B1B", "#D90429", "#FFD700", "#FFAA33", "#A2A2A2", 
                "#001F3F", "#8B4513", "#F5C518", "#5A5A5A", "#B22222"]

cluster0kmodes = dataset[dataset['cluster_kmodes'] == 0]
cluster1kmodes = dataset[dataset['cluster_kmodes'] == 1]
cluster2kmodes = dataset[dataset['cluster_kmodes'] == 2]
cluster3kmodes = dataset[dataset['cluster_kmodes'] == 3]

# Dicionário de tradução
traducao = {
    'genres': 'Gêneros',
    'spoken_languages': 'Línguas Faladas',
    'production_countries': 'Países de Produção'
}

def grafico_barras(cluster, data, coluna, qtd):
    contagem = data.groupby(coluna).size()
    top_10_contagem = contagem.nlargest(qtd)
    top_10_contagem = top_10_contagem.sort_values(ascending=True)
    
    coluna_traduzida = traducao.get(coluna, coluna)  # Traduz a coluna se houver tradução disponível
    
    fig = px.bar(top_10_contagem, x=top_10_contagem.values, y=top_10_contagem.index, 
                 title=f"{coluna_traduzida} mais presentes no cluster {cluster}", 
                 labels={"x": "Contagem", coluna: coluna_traduzida})
    fig.update_traces(marker=dict(color=cores_cinema))
    return fig

#Comparação de existência de lucro
def contar_lucro (df):
    return (df['revenue'] > df['budget']).sum() / ((df['revenue'] > df['budget']).sum() + (df['revenue'] < df['budget']).sum())

#Quantidades de filmes que lucraram por cluster
lucrou0 = contar_lucro(cluster0kmodes)
lucrou1 = contar_lucro(cluster1kmodes)
lucrou2 = contar_lucro(cluster2kmodes)
lucrou3 = contar_lucro(cluster3kmodes)

#Explorando os clusters provenientes do KMeans (clusterização dos dados numéricos)
cluster0kmeans = dataset[dataset['cluster_kmeans'] == 0]
cluster1kmeans = dataset[dataset['cluster_kmeans'] == 1]

#Porcentagem de filmes que lucraram por cluster
lucrou0kmeans = contar_lucro(cluster0kmeans)
lucrou1kmeans = contar_lucro(cluster1kmeans)

#Porcentagem de lucro nas regiões do heatmap
contagem_lucro_regioes = dataset.groupby(['cluster_kmodes', 'cluster_kmeans'], group_keys=False).apply(contar_lucro, include_groups=False).reset_index(name='porcentagem_lucro')

# Título da aplicação
st.title("Visualização da Clusterização")

# Selecionar o tipo de clusterização
tipo_clusterizacao = st.selectbox("Selecione o Tipo de Clusterização", ["KModes", "KMeans"])

if tipo_clusterizacao == "KModes":

    #Porcentagem de filmes que lucraram por cluster

    dic_lucrou = {'Cluster' : ['0', '1', '2', '3'], 'Quantidade' : [lucrou0, lucrou1, lucrou2, lucrou3]}

    fig = go.Figure(
        data=[go.Bar(
            x=dic_lucrou['Cluster'], 
            y=dic_lucrou['Quantidade'], 
            marker_color=cores_cinema
        )]
    )

    fig.update_layout(
        title="Porcentagem de Filmes que Lucraram por Cluster",
        xaxis_title="Clusters",
        yaxis_title="Quantidade de Filmes",
        yaxis=dict(range=[0, 1])
    )

    fig.update_traces(hovertemplate='%{y:.1%}')

    st.plotly_chart(fig)

    st.text("Podemos observar que essa é a sequência do cluster mais sucrativo pro menos: cluster 1 (ação e subgêneros), cluster 0 (comédia e subgêneros), cluster 2 (terror/suspende e subgêneros), cluster 3 (drama e subgêneros).")

else:

    #Porcentagem de filmes que lucraram por cluster

    dic_lucrou = {'Cluster' : ['0', '1'], 'Quantidade' : [lucrou0kmeans, lucrou1kmeans]}

    fig = go.Figure(
        data=[go.Bar(
            x=dic_lucrou['Cluster'], 
            y=dic_lucrou['Quantidade'], 
            marker_color=cores_cinema
        )]
    )

    fig.update_layout(
        title="Porcentagem de Filmes que Lucraram por Cluster",
        xaxis_title="Clusters",
        yaxis_title="Quantidade de Filmes",
        yaxis=dict(range=[0, 1]),
    )

    fig.update_traces(hovertemplate='%{y:.1%}')

    st.plotly_chart(fig)

    st.text("Podemos observar a porcentagem de lucro extrema do cluster 1 (outliers) e, mesmo o cluster 0 não possuindo outliers, podemos perceber")

# Contando quantos registros pertencem a cada combinação de clusters
heatmap_data = dataset.groupby(['cluster_kmodes', 'cluster_kmeans']).size().reset_index(name='Contagem')

colorscale_cinema = [
    [0.0, "#0D0D0D"],
    [0.2, "#383838"],
    [0.4, "#FFC300"],
    [0.6, "#E25822"],
    [0.8, "#8B0000"],
    [1.0, "#FF0000"]
]

# Criando um heatmap para melhor observar a relação entre a clusterização categórica e a numérica

heatmap_data['cluster_kmodes'] = heatmap_data['cluster_kmodes'].astype(str)
heatmap_data['cluster_kmeans'] = heatmap_data['cluster_kmeans'].astype(str)

fig = go.Figure(data=go.Heatmap(
    z=heatmap_data['Contagem'],
    x=heatmap_data['cluster_kmeans'],
    y=heatmap_data['cluster_kmodes'],
    colorscale=colorscale_cinema,
    text=heatmap_data['Contagem'],
    texttemplate="%{text}",
    hovertemplate="Cluster Numérico: %{x}<br>Cluster Categórico: %{y}<br>Contagem: %{text}<extra></extra>"
))

fig.update_layout(
    title="Heatmap da Relação entre Clusters Categóricos e Numéricos",
    xaxis_title="Clusters Numéricos",
    yaxis_title="Clusters Categóricos"
)

st.plotly_chart(fig)

st.text("O Heatmap demonstra a relação na distribuição dos registros entre os clusters categóricos e numéricos. Podemos observar, por exemplo, que a maioria dos filmes com lucratividade muito alta (filmes na posição 1 do eixo X) fazem parte do cluster 1 categórico (filmes de ação e subgêneros).")

contagem_lucro_regioes['categoria'] = contagem_lucro_regioes['cluster_kmodes'].astype(str) + '-' + contagem_lucro_regioes['cluster_kmeans'].astype(str)

fig = px.bar(
    contagem_lucro_regioes, 
    x='categoria', 
    y='porcentagem_lucro', 
    text='porcentagem_lucro',
    labels={'categoria': 'Região do Heatmap', 'porcentagem_lucro': 'Porcentagem de Lucro'},
    title='Porcentagem de Lucro por região no Heatmap',
    color = 'categoria',
    color_discrete_sequence = cores_cinema
)

fig.update_traces(texttemplate='%{text:.1%}', hovertemplate='%{y:.1%}')

st.plotly_chart(fig)

st.text("Podemos observar que as regiões que fazem parte do cluster 1 numérico possuem, em média, lucratividades extremamente altas (acima de 90%), devido ao algoritmo ter selecionado filmes que foram muito lucrativos para esse cluster. As outras regiões, embora não tão altas, também possuem boas porcentagens de lucro. Isso é devido ao fato de estarmos trabalhando apenas com filmes que possuíram um grande orçamento.")

if tipo_clusterizacao == "KModes":
    cluster_selecionado = st.selectbox("Selecione o Cluster", ["0", "1", "2", "3"])
    if cluster_selecionado == "0":
        #Gêneros mais presentes no cluster 0
        fig = grafico_barras('0', cluster0kmodes, 'genres', 5)
        st.plotly_chart(fig)
        st.text("O algoritmo K-Modes selecionou para o cluster 0 filmes de comédia e seus subgêneros.")
        #Línguas mais faladas no cluster 0
        fig = grafico_barras('0', cluster0kmodes, 'spoken_languages', 8)
        st.plotly_chart(fig)
        st.text("O inglês é a língua mais falada no cluster, as outras seguem equilibradas.")
        #Páises mais presentes no cluster 0
        fig = grafico_barras('0', cluster0kmodes, 'production_countries', 8)
        st.plotly_chart(fig)
        st.text("A maioria dos filmes presentes no cluster possuem o país Estados Unidos da América em suas produções.")
    elif cluster_selecionado == "1":
        #Gêneros mais presentes no cluster 1
        fig = grafico_barras('1', cluster1kmodes, 'genres', 5)
        st.plotly_chart(fig)
        st.text("O algoritmo K-Modes selecionou para o cluster 1 filmes de ação e seus subgêneros.")
        #Línguas mais faladas no cluster 1
        fig = grafico_barras('1', cluster1kmodes, 'spoken_languages', 8)
        st.plotly_chart(fig)
        st.text("O inglês é a língua mais falada no cluster, as outras seguem equilibradas.")
        #Páises mais presentes no cluster 1
        fig = grafico_barras('1', cluster1kmodes, 'production_countries', 8)
        st.plotly_chart(fig)
        st.text("A maioria dos filmes presentes no cluster possuem o país Estados Unidos da América em suas produções.")
    elif cluster_selecionado == "2":
        #Gêneros mais presentes no cluster 2
        fig = grafico_barras('2', cluster2kmodes, 'genres', 5)
        st.plotly_chart(fig)
        st.text("O algoritmo K-Modes selecionou para o cluster 2 filmes de terror/suspense e seus subgêneros.")
        #Línguas mais faladas no cluster 2
        fig = grafico_barras('2', cluster2kmodes, 'spoken_languages', 8)
        st.plotly_chart(fig)
        st.text("O inglês é a língua mais falada no cluster, as outras seguem equilibradas.")
        #Páises mais presentes no cluster 2
        fig = grafico_barras('2', cluster2kmodes, 'production_countries', 8)
        st.plotly_chart(fig)
        st.text("A maioria dos filmes presentes no cluster possuem o país Estados Unidos da América em suas produções.")
    else:
        #Gêneros mais presentes no cluster 3
        fig = grafico_barras('3', cluster3kmodes, 'genres', 5)
        st.plotly_chart(fig)
        st.text("O algoritmo K-Modes selecionou para o cluster 3 filmes de drama e seus subgêneros.")
        #Línguas mais faladas no cluster 3
        fig = grafico_barras('3', cluster3kmodes, 'spoken_languages', 8)
        st.plotly_chart(fig)
        st.text("O inglês é a língua mais falada no cluster, as outras seguem equilibradas.")
        #Páises mais presentes no cluster 3
        fig = grafico_barras('3', cluster3kmodes, 'production_countries', 8)
        st.plotly_chart(fig)
        st.text("A maioria dos filmes presentes no cluster possuem o país Estados Unidos da América em suas produções.")

else:
    tipo_clusterizacao = "KMeans"
    cluster_selecionado = st.selectbox("Selecione o Cluster", ["0", "1"])
    if cluster_selecionado == "0":
        #Gêneros mais presentes no cluster 0
        fig = grafico_barras('0', cluster0kmeans, 'genres', 5)
        st.plotly_chart(fig)
        st.text("O cluster 0 gerado pelo K-Means é o cluster que não possui apenas filmes que foram altamente lucrativos, então podemos observar através desse gráfico os gêneros menos propensos a terem uma lucratividade extrema.")
        #Línguas mais faladas no cluster 0
        fig = grafico_barras('0', cluster0kmeans, 'spoken_languages', 8)
        st.plotly_chart(fig)
        st.text("A maioria dos filmes do cluster são de língua inglêsa.")
        #Páises mais presentes no cluster 0
        fig = grafico_barras('0', cluster0kmeans, 'production_countries', 8)
        st.plotly_chart(fig)
        st.text("A maioria dos filmes do cluster possuem os Estados Unidos da América em sua produção.")
    else:
        #Gêneros mais presentes no cluster 1
        fig = grafico_barras('1', cluster1kmeans, 'genres', 5)
        st.plotly_chart(fig)
        st.text("O cluster 1 gerado pelo K-Means é o cluster que possui filmes com as mais altas lucratividades, então podemos observar através do gráficos os gêneros mais propensos a fazerem tanto sucesso.")
        #Línguas mais faladas no cluster 1
        fig = grafico_barras('1', cluster1kmeans, 'spoken_languages', 8)
        st.plotly_chart(fig)
        st.text("A maioria dos filmes do cluster são de língua inglêsa.")
        #Páises mais presentes no cluster 1
        fig = grafico_barras('1', cluster1kmeans, 'production_countries', 8)
        st.plotly_chart(fig)
        st.text("A maioria dos filmes do cluster possuem os Estados Unidos da América em sua produção.")