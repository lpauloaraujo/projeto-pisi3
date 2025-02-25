import pandas as pd
from levenshtein import main as corrigir
from sklearn.svm import SVC


def dados_usuario(genero,budget,pais_producao,lingua,n_linguas,runtime):
    
    # Corrige entradas com base em dicionários externos
    genero = corrigir(genero, "generos")
    pais_producao = corrigir(pais_producao, "paises")
    lingua = corrigir(lingua, "idiomas")

    return genero, budget, pais_producao, lingua, n_linguas, runtime


def filtrar(genero, budget, pais_producao, lingua, n_lingua, runtime, dados_teste_encoded, dados_treino_encoded):
    # Filtra os dados para que correspondam aos critérios do usuário
    dados_teste_encoded = dados_teste_encoded[
        (dados_teste_encoded["genres"].str.contains(genero)) &
        (dados_teste_encoded["budget"] <= budget) &
        (dados_teste_encoded["budget"] >= budget // 2) &
        (dados_teste_encoded["production_countries"].str.contains(pais_producao)) &
        (dados_teste_encoded["original_language"] == lingua) &
        (dados_teste_encoded["runtime"] <= runtime)
    ]
    
    dados_treino_encoded = dados_treino_encoded[
        (dados_treino_encoded["genres"].str.contains(genero)) &
        (dados_treino_encoded["budget"] <= budget) &
        (dados_treino_encoded["budget"] >= budget // 2) &
        (dados_treino_encoded["production_countries"].str.contains(pais_producao)) &
        (dados_treino_encoded["original_language"] == lingua) &
        (dados_treino_encoded["runtime"] <= runtime)
    ]
    
    # Remove as colunas desnecessárias
    dados_treino_encoded.drop(columns=["release_date", "genres", "spoken_languages", "adult", "revenue", "original_language",
                                        "production_countries", "spoken_languages", "adult", "disponibilidade_lucro", "lucro"], inplace=True)
    
    dados_teste_encoded.drop(columns=["release_date", "genres", "spoken_languages", "adult", "revenue", "original_language",
                                      "production_countries", "spoken_languages", "adult", "disponibilidade_lucro", "lucro"], inplace=True)
    
    return dados_teste_encoded, dados_treino_encoded


def svm(dados_teste_encoded, dados_treino_encoded):
    X_train = dados_treino_encoded.drop(columns=['classificacao'])
    y_train = dados_treino_encoded['classificacao']
    X_test = dados_teste_encoded.drop(columns=['classificacao'])
    y_test = dados_teste_encoded['classificacao']

    # Treinando o modelo SVM com a capacidade de prever probabilidades
    model = SVC(kernel='rbf', random_state=42, probability=True)  # probability=True para prever as probabilidades
    model.fit(X_train, y_train)

    # Previsão das probabilidades de sucesso (classe 1) e fracasso (classe 0)
    probabilidade = model.predict_proba(X_test)

    # A coluna '1' contém a probabilidade de ser sucesso (classe 1)
    probabilidade_sucesso = probabilidade[:, 1] * 100  # Multiplica por 100 para obter a porcentagem de sucesso

    return probabilidade_sucesso


def calcular_media(probabilidades):
    # Função que calcula a média das probabilidades de sucesso
    media_probabilidade = probabilidades.mean()
    return media_probabilidade


def aplicar_ao_svm(treino, teste,genero,budget,pais_producao,lingua,n_linguas,runtime):
    dados_teste_encoded = pd.read_parquet(teste)
    dados_treino_encoded = pd.read_parquet(treino)

    dados_treino_encoded.drop(columns=["lucro"])
    dados_teste_encoded.drop(columns=["lucro"])

    # Obtém os dados do usuário
    genero, budget, pais_producao, lingua, n_linguas, runtime = dados_usuario(genero, budget, pais_producao, lingua, n_linguas, runtime)

    # Filtra os dados para que correspondam aos critérios do usuário
    dados_teste_encoded, dados_treino_encoded = filtrar(genero, budget, pais_producao, 
                                                        lingua, n_linguas, runtime, dados_teste_encoded, dados_treino_encoded)
    
    # Obtém as probabilidades de sucesso para o conjunto de teste
    previsoes_probabilidade = svm(dados_teste_encoded, dados_treino_encoded)
    
    # Calcula a média das probabilidades
    media_probabilidade = calcular_media(previsoes_probabilidade)
    
    return media_probabilidade


def resultado(genero, budget, pais_producao, lingua, n_linguas, runtime):
    arquivo_teste = "data/dados_teste.parquet"
    arquivo_treino = "data/dados_treino.parquet"

    # Aplica o modelo SVM para obter as probabilidades de sucesso
    media_probabilidade = aplicar_ao_svm(arquivo_treino, arquivo_teste,genero,budget,pais_producao,lingua,n_linguas,runtime)
    
    # Retorna a média das probabilidades de sucesso
    return media_probabilidade


