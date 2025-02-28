import streamlit as st
from predicao import *
import pandas as pd
import plotly.express as px

# Título do aplicativo
st.title("Filtros de Filme")

# 2. Países de Produção
pais_principal_de_producao = st.text_input("País principal de Produção", placeholder="Ex: EUA")

# 3. Línguas Originais
languages = st.text_input("Língua Original", placeholder="Ex: Inglês")

# 5. Faixa de Runtime
min_runtime = st.text_input("Faixa de Runtime (minutos) - menor valor", placeholder="Ex: 120")
min_runtime = int(min_runtime) if min_runtime else 0

max_runtime = st.text_input("Faixa de Runtime (minutos) - maior valor", placeholder="Ex: 120")
max_runtime = int(max_runtime) if max_runtime else 0

# 1. Faixa de Budget do Filme
min_budget = st.text_input("Faixa de Budget do Filme - menor valor", placeholder="Ex: 2000000")
min_budget = int(min_budget) if min_budget else 0

max_budget = st.text_input("Faixa de Budget do Filme - maior valor", placeholder="Ex: 2000000")
max_budget = int(max_budget) if max_budget else 0


# 4. Gêneros do Filme
genero_principal = st.text_input("Gênero principal do Filme", placeholder="Ex: Ação")

# Botão para processar os dados
if st.button("Aplicar Filtros"):
    # Obtém a porcentagem de lucro
    porcentagem_lucro = resultado(pais_principal_de_producao,languages,min_runtime,max_runtime,min_budget,max_budget,genero_principal) * 100
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