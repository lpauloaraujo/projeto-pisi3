import streamlit as st
from predicao import *
import pandas as pd
import plotly.express as px

# Título do aplicativo
st.title("Filtros de Filme")

# 1. Faixa de Budget do Filme
budget = st.text_input("Faixa de Budget do Filme", placeholder="Ex: 2000000")
budget = int(budget) if budget else 0

# 2. Países de Produção
pais_principal_de_producao = st.text_input("País principal de Produção", placeholder="Ex: EUA")

# 3. Línguas Originais
languages = st.text_input("Língua Original", placeholder="Ex: Inglês")

Traducoes = st.text_input("Número de Línguas", placeholder="Ex: 1")
Traducoes = int(Traducoes) if Traducoes else 0

# 4. Gêneros do Filme
genero_principal = st.text_input("Gênero principal do Filme", placeholder="Ex: Ação")

# 5. Faixa de Runtime
runtime = st.text_input("Faixa de Runtime (minutos)", placeholder="Ex: 120")
runtime = int(runtime) if runtime else 0

# Botão para processar os dados
if st.button("Aplicar Filtros"):
    # Obtém a porcentagem de lucro
    porcentagem_lucro = resultado(genero_principal, budget, pais_principal_de_producao, languages, Traducoes, runtime)
    porcentagem_nao_lucro = 100 - porcentagem_lucro

    # Exibe a porcentagem de lucro em verde e não lucro em vermelho
    st.markdown(
        f"**<span style='color:green'>Porcentagem de Lucro:</span> <span style='color:green'>{porcentagem_lucro:.2f}%</span>**", 
        unsafe_allow_html=True
    )
    st.markdown(
        f"**<span style='color:red'>Porcentagem de Não Lucro:</span> <span style='color:red'>{porcentagem_nao_lucro:.2f}%</span>**", 
        unsafe_allow_html=True
    )

    # Cria um DataFrame para o Plotly
    dados = {
        "Categoria": ["Lucro", "Não Lucro"],
        "Porcentagem": [porcentagem_lucro, porcentagem_nao_lucro]
    }
    df = pd.DataFrame(dados)

    # Cria o gráfico de barras com Plotly
    fig = px.bar(df, x="Categoria", y="Porcentagem", 
                 text="Porcentagem", 
                 title="Probabilidade de Lucro vs Não Lucro",
                 labels={"Porcentagem": "Porcentagem (%)", "Categoria": "Categoria"},
                 color="Categoria", 
                 color_discrete_map={"Lucro": "green", "Não Lucro": "red"})

    # Ajusta o texto das barras
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')

    # Exibe o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)