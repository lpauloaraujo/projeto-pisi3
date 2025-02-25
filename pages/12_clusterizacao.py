import streamlit as st
import pandas as pd
import plotly.express as px
from kmodes.kmodes import KModes

# Carregar os dados
dataset_path = "TMDB_movie_dataset_v11_tratado2.parquet"
dataset = pd.read_parquet(dataset_path)

st.title("Análise de Clusters de Filmes")

# Função para criar gráfico de Pareto
def diagrama_pareto(data_frame, coluna, titulo):
    aparicoes_dados = data_frame[coluna].value_counts().sort_values(ascending=False)
    agrupado = aparicoes_dados.reset_index(name='Contagem')
    agrupado = agrupado.sort_values('Contagem', ascending=False)
    agrupado['Acumulado'] = agrupado['Contagem'].cumsum() / agrupado['Contagem'].sum() * 100
    agrupado_principal = agrupado[agrupado['Acumulado'] <= 70]
    agrupado_outros = agrupado[agrupado['Acumulado'] > 70]
    outros_contagem = agrupado_outros['Contagem'].sum()
    linha_outros = pd.DataFrame({coluna: ['Outros'], 'Contagem': [outros_contagem], 'Acumulado': [100]})
    agrupado_principal = pd.concat([agrupado_principal, linha_outros], ignore_index=True)
    return agrupado_principal

# Gráficos de Pareto
st.header("Distribuição de Países de Produção")
paises_principais = diagrama_pareto(dataset, 'production_countries', 'Produção por País')
fig_paises = px.bar(paises_principais, x='production_countries', y='Contagem', title='Produção por País')
st.plotly_chart(fig_paises)

st.header("Distribuição de Línguas Faladas")
linguas_principais = diagrama_pareto(dataset, 'spoken_languages', 'Línguas Faladas')
fig_linguas = px.bar(linguas_principais, x='spoken_languages', y='Contagem', title='Línguas Faladas')
st.plotly_chart(fig_linguas)

st.header("Clusters de Filmes")
num_clusters = st.slider("Escolha o número de clusters", min_value=2, max_value=10, value=3)

# One-hot encoding para clustering
def onehotencoding(df, coluna):
    df[coluna] = df[coluna].fillna('')
    valores = diagrama_pareto(df, coluna).iloc[:, 0].values
    return pd.DataFrame(one_hot_data, index=df.index)

encoded_paises = onehotencoding(dataset, 'production_countries')
km = KModes(n_clusters=num_clusters, init='Huang', n_init=5, verbose=0)
clusters = km.fit_predict(encoded_paises)
dataset['Cluster'] = clusters

fig_clusters = px.scatter(dataset, x='popularity', y='vote_average', color=dataset['Cluster'].astype(str), title='Clusters de Filmes')
st.plotly_chart(fig_clusters)

st.write("## Dados dos Filmes")
st.dataframe(dataset)
