#Importando bibliotecas
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Função para carregar os dados
def carregar_dados(filepath):
    return pd.read_parquet(filepath)

# Carregar os dados
dataset = carregar_dados("dataset_com_clusters.parquet")



# Explorando os clusters provenientes do KModes (clusterização dos dados categóricos)
cores_cinema = [
    "#1F77B4", "#FF7F0E", "#2CA02C", "#D62728", "#9467BD", 
    "#8C564B", "#E377C2", "#7F7F7F", "#BCBD22", "#17BECF"
]

cluster0kmodes = dataset[dataset['cluster'] == 0]
cluster1kmodes = dataset[dataset['cluster'] == 1]
cluster2kmodes = dataset[dataset['cluster'] == 2]
cluster3kmodes = dataset[dataset['cluster'] == 3]
cluster4kmodes = dataset[dataset['cluster'] == 4]
cluster5kmodes = dataset[dataset['cluster'] == 5]

def grafico_barras(cluster, data, coluna, qtd):
    # Dicionário de tradução
    traducao_colunas = {
        'genres': 'Gêneros',
        'spoken_languages': 'Idiomas Falados',
        'production_countries': 'Países de Produção'
    }
    
    contagem = data.groupby(coluna).size()
    top_10_contagem = contagem.nlargest(qtd)
    top_10_contagem = top_10_contagem.sort_values(ascending=True)
    
    # Traduzir o título da coluna
    coluna_traduzida = traducao_colunas.get(coluna, coluna)
    
    fig = px.bar(top_10_contagem, x=top_10_contagem.values, y=top_10_contagem.index, title=f"{coluna_traduzida} mais presentes no cluster {cluster}", labels={"x": "Contagem", coluna: coluna_traduzida})
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
lucrou4 = contar_lucro(cluster4kmodes)
lucrou5 = contar_lucro(cluster5kmodes)

#Explorando os clusters provenientes do KMeans (clusterização dos dados numéricos)
cluster0kmeans = dataset[dataset['clusters_n'] == 0]
cluster1kmeans = dataset[dataset['clusters_n'] == 1]
cluster2kmeans = dataset[dataset['clusters_n'] == 2]

#Porcentagem de filmes que lucraram por cluster
lucrou0kmeans = contar_lucro(cluster0kmeans)
lucrou1kmeans = contar_lucro(cluster1kmeans)
lucrou2kmeans = contar_lucro(cluster2kmeans)

# Título da aplicação
st.title("Visualização de Gráficos de Clusterização")

# Selecionar o tipo de clusterização
tipo_clusterizacao = st.selectbox("Selecione o Tipo de Clusterização", ["KModes", "KMeans"])

if tipo_clusterizacao == "KModes":
    
    st.text("Dispersão dos Clusters (KModes)")
    st.image(r"pages\dispersao_kmodes.png")
    st.text("Boxplot dos Clusters (KModes)")
    st.image(r"pages\boxplot_kmodes.png")

    # Porcentagem de filmes que lucraram por cluster
    dic_lucrou = {'Cluster': ['0', '1', '2', '3', '4', '5'], 'Quantidade': [lucrou0, lucrou1, lucrou2, lucrou3, lucrou4, lucrou5]}

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

    st.text("Primeiramente, devemos nos atentar ao cluster 5. O cluster 5, formado dominantemente for filmes japoneses, parece ter uma grande lucratividade, porém isso está equivacado, se deve ao fato desse cluster possuir um número grande de registros com valor nulo em 'budget' e 'revenue'. Segundamente, podemos observar o cluster que é realmente o mais lucrativo, o cluster 3, que representa filmes estadunidenses. Por fim, o cluster menos lucrativo é o 4, que possui filmes com valores nulos no atributo gênero.")

else:
    st.text("Dispersão dos Clusters (KMeans)")
    st.image(r"pages\dispersao_kmeans.png")
    st.text("Boxplot dos Clusters (KMeans)")
    st.image(r"pages\boxplot_kmeans.png")

    # Porcentagem de filmes que lucraram por cluster
    dic_lucrou = {'Cluster': ['0', '1', '2'], 'Quantidade': [lucrou0kmeans, lucrou1kmeans, lucrou2kmeans]}

    fig = go.Figure(
        data=[go.Bar(
            x=dic_lucrou['Cluster'], 
            y=dic_lucrou['Quantidade'], 
            marker_color=cores_cinema[:3]
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

    st.text("Essa é a porcentagem de lucratividade dos clusters formados pelo KMeans (para a definição do número de clusters foi utilizado o elbow method). A primeira coisa que chama atenção é a lucratividade fora do normal do cluster 2. Isso se dá pelo algoritmo ter posto outliers nesse cluster, outliers esses que não vemos sentido em remover, visto que pro nosso trabalho analisar o sucesso de outliers também é válido. Quanto a outros cluster, é possível ver que o cluster 0 ficou nos 40% de lucratividade, já o cluster 1 bem abaixo, possuindo, segundo o KMeans, os filmes menos lucrativos.")

# Contando quantos registros pertencem a cada combinação de clusters
heatmap_data = dataset.groupby(['cluster', 'clusters_n']).size().reset_index(name='Contagem')

colorscale_cinema = [
    [0.0, "#FF5733"],
    [0.2, "#FF8D1A"],
    [0.4, "#FFC300"],
    [0.6, "#FFD700"],
    [0.8, "#A8E63D"],
    [1.0, "#4CAF50"]
]

# Criando um heatmap para melhor observar a relação entre a clusterização categórica e a numérica

heatmap_data['cluster'] = heatmap_data['cluster'].astype(str)
heatmap_data['cluster_n'] = heatmap_data['clusters_n'].astype(str)

fig = go.Figure(data=go.Heatmap(
    z=heatmap_data['Contagem'],
    x=heatmap_data['clusters_n'],
    y=heatmap_data['cluster'],
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

st.text("Esse mapa de calor é uma relação entre os clusters gerados pelo KModes (eixo Y) e os gerados pelo KMeans (eixo X). Podemos observar que a maior parte dos ohtliers (cluster 2 do KMeans) fazem parte também do cluster 3 do KModes (filmes produzidos pelos Estados Unidos da América). Podemos observar que esse país também produziu uma grande quantia dos filmes presentes no cluster 0 do KMeans (cluster que possui a lucratividade mais alta, que é de 40%, com excessão do cluster 2).")

#Porcentagem de lucro nas regiões do heatmap
contagem_lucro_regioes = dataset.groupby(['cluster', 'clusters_n'], group_keys=False).apply(contar_lucro, include_groups=False).reset_index(name='porcentagem_lucro')

contagem_lucro_regioes['categoria'] = contagem_lucro_regioes['cluster'].astype(str) + '-' + contagem_lucro_regioes['clusters_n'].astype(str)

fig = px.bar(
    contagem_lucro_regioes, 
    x='categoria', 
    y='porcentagem_lucro', 
    text='porcentagem_lucro',
    labels={'categoria': 'Região do Heatmap', 'porcentagem_lucro': 'Porcentagem de Lucro'},
    title='Porcentagem de Lucro por região no Heatmap',
    color='categoria',
    color_discrete_sequence=cores_cinema
)

fig.update_traces(texttemplate='%{text:.1%}', hovertemplate='%{y:.1%}')

st.plotly_chart(fig)

st.text("Aqui temos a lucratividade de cada região do mapa de calor que mostra o relacionamento entre os clusters provenientes do KModes e do KMeans.")

if tipo_clusterizacao == "KModes":
    cluster_selecionado = st.selectbox("Selecione o Cluster", ["0", "1", "2", "3", "4", "5"])
    if cluster_selecionado == "0":
        cluster_data = cluster0kmodes
        st.plotly_chart(grafico_barras(cluster_selecionado, cluster_data, 'genres', 5))
        st.text("O algoritmo KModes agrupou nesse cluster filmes que possuem 'documentário' em seus gêneros.")
        st.plotly_chart(grafico_barras(cluster_selecionado, cluster_data, 'spoken_languages', 8))
        st.text("O inglês é a língua mais falada do cluster, mas isso não foge do quadro geral do dataset, logo a língua não foi o fator determinante da formação desse cluster.")
        st.plotly_chart(grafico_barras(cluster_selecionado, cluster_data, 'production_countries', 8))
        st.text("Os três países com mais filmes nesse cluster são europeus. Em seguida, os países parecem variados. Porém, não foram os países que determinaram esse cluster, e sim os gêneros. Cheque o gráfico de gêneros predominantes nesse cluster para mais detalhes.")
    elif cluster_selecionado == "1":
        cluster_data = cluster1kmodes
        st.plotly_chart(grafico_barras(cluster_selecionado, cluster_data, 'genres', 5))
        st.text("O algoritmo KModes agrupou nesse cluster filmes que possuem 'Drama' em seus gêneros.")
        st.plotly_chart(grafico_barras(cluster_selecionado, cluster_data, 'spoken_languages', 8))
        st.text("O inglês é a língua mais falada do cluster, mas isso não foge do quadro geral do dataset, logo a língua não foi o fator determinante da formação desse cluster.")
        st.plotly_chart(grafico_barras(cluster_selecionado, cluster_data, 'production_countries', 8))
        st.text("Os países são variados nesse cluster, os países não foram o fator determinante aqui, e sim os gêneros. Cheque o gráfico de gêneros predominantes nesse cluster para mais detalhes.")
    elif cluster_selecionado == "2":
        cluster_data = cluster2kmodes
        st.plotly_chart(grafico_barras(cluster_selecionado, cluster_data, 'genres', 5))
        st.text("O algoritmo KModes agrupou nesse cluster filmes que possuem 'Comédia' em seus gêneros.")
        st.plotly_chart(grafico_barras(cluster_selecionado, cluster_data, 'spoken_languages', 8))
        st.text("O inglês é a língua mais falada do cluster, mas isso não foge do quadro geral do dataset, logo a língua não foi o fator determinante da formação desse cluster.")
        st.plotly_chart(grafico_barras(cluster_selecionado, cluster_data, 'production_countries', 8))
        st.text("Os países são variados nesse cluster, os países não foram o fator determinante aqui, e sim os gêneros. Cheque o gráfico de gêneros predominantes nesse cluster para mais detalhes.")
    elif cluster_selecionado == "3":
        cluster_data = cluster3kmodes
        st.plotly_chart(grafico_barras(cluster_selecionado, cluster_data, 'genres', 5))
        st.text("Os gêneros não possuíram muita influência na formação desse cluster.")
        st.plotly_chart(grafico_barras(cluster_selecionado, cluster_data, 'spoken_languages', 8))
        st.text("É possível ver uma dominância do inglês nesse cluster. Contudo, isso não ocorreu por conta do atributo 'língua falada', mas sim por esse cluster ter sido formado levando em conta filmes que possuem o país 'Estados Unidos da América' em sua produção. É possível observar melhor checando o gráfico de países envolvidos na produção desse cluster.")
        st.plotly_chart(grafico_barras(cluster_selecionado, cluster_data, 'production_countries', 8))
        st.text("É possível observar que o KModes formou esse cluster para filmes que possuem o país 'Estados Unidos da América' em sua produção.")
    elif cluster_selecionado == "4":
        cluster_data = cluster4kmodes
        st.plotly_chart(grafico_barras(cluster_selecionado, cluster_data, 'genres', 5))
        st.text("O algoritmo KModes agrupou filmes que possuem gênero nulo (não possuem dados disponíveis sobre seus gêneros).")
        st.plotly_chart(grafico_barras(cluster_selecionado, cluster_data, 'spoken_languages', 8))
        st.text("O inglês é a língua mais falada do cluster, mas isso não foge do quadro geral do dataset, logo a língua não foi o fator determinante da formação desse cluster.")
        st.plotly_chart(grafico_barras(cluster_selecionado, cluster_data, 'production_countries', 8))
        st.text("Os países são variados nesse cluster, os países não foram o fator determinante aqui, e sim os gêneros. Cheque o gráfico de gêneros predominantes nesse cluster para mais detalhes.")
    elif cluster_selecionado == "5":
        cluster_data = cluster5kmodes
        st.plotly_chart(grafico_barras(cluster_selecionado, cluster_data, 'genres', 5))
        st.text("Por mais que seja observável uma grande presença de filmes de gênero nulo ou drama, os gêneros não foram a razão da formação desse agrupamento.")
        st.plotly_chart(grafico_barras(cluster_selecionado, cluster_data, 'spoken_languages', 8))
        st.text("É possível ver a predominância da língua japonesa nesse cluster.")
        st.plotly_chart(grafico_barras(cluster_selecionado, cluster_data, 'production_countries', 8))
        st.text("É possível observar que o KModes formou esse cluster para filmes japoneses.")

elif tipo_clusterizacao == "KMeans":
    cluster_selecionado = st.selectbox("Selecione o Cluster", ["0", "1", "2"])
    if cluster_selecionado == "0":
        cluster_data = cluster0kmeans
    elif cluster_selecionado == "1":
        cluster_data = cluster1kmeans
    elif cluster_selecionado == "2":
        cluster_data = cluster2kmeans
    
    st.plotly_chart(grafico_barras(cluster_selecionado, cluster_data, 'genres', 5))
    st.plotly_chart(grafico_barras(cluster_selecionado, cluster_data, 'spoken_languages', 8))
    st.plotly_chart(grafico_barras(cluster_selecionado, cluster_data, 'production_countries', 8))