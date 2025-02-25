from typing import List, Tuple

def levenshtein(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0:
                dp[i][j] = j  # Inserções
            elif j == 0:
                dp[i][j] = i  # Remoções
            elif s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]  # Nenhuma operação
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],    # Remoção
                                   dp[i][j - 1],    # Inserção
                                   dp[i - 1][j - 1]) # Substituição
    
    return dp[m][n]

def encontrar_palavra_mais_proxima(palavra_alvo: str, lista_palavras: List[str]) -> Tuple[str, int]:
    mais_prox = float('inf')  # Inicializa com infinito
    palavra_proxima = ""

    for palavra in lista_palavras:
        distancia = levenshtein(palavra_alvo, palavra)

        if distancia < mais_prox:
            mais_prox = distancia
            palavra_proxima = palavra

    return palavra_proxima, mais_prox

# Exemplo de uso:
generos = ['Action', 'Science Fiction', 'Adventure', 'Drama', 'Crime',
           'Thriller', 'Fantasy', 'Comedy', 'Romance', 'Western', 'Mystery', 'War',
           'Animation', 'Family', 'Horror', 'Music']

idiomas_permitidos = ['en', 'fr', 'es', 'de', 'ja', 'zh', 'pt', 'it']
selected_countries = ['United States', 'France', 'United Kingdom', 'Germany', 
                      'Canada', 'Japan', 'China', 'India', 'Italy', 'Spain']

listas = {
    "generos": generos,
    "idiomas": idiomas_permitidos,
    "paises": selected_countries
}

# Entrada do usuário:
palavra = input("Digite a palavra para comparar: ")
nome_da_lista = input("Digite o nome da lista (generos, idiomas ou paises): ")

# Verifica se a lista existe e encontra a palavra mais próxima:
if nome_da_lista in listas:
    lista_selecionada = listas[nome_da_lista]
    palavra_proxima, distancia = encontrar_palavra_mais_proxima(palavra, lista_selecionada)
    print(f"Palavra mais próxima em '{nome_da_lista}': {palavra_proxima} (distância: {distancia})")
else:
    print("Lista não encontrada.")
