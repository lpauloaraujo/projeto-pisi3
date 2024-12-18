import csv
import os

def abrir():
    """
    Abre o arquivo csv e retorna um dicionário com as datas e valores de inflação.
    """
    caminho_script = os.path.dirname(os.path.abspath(__file__))
    caminho_data = os.path.join(caminho_script, '..', 'data', 'inflacao1957.csv')

    with open(caminho_data, 'r') as arquivo_csv:

        leitor_csv = csv.reader(arquivo_csv)
        dictionary = {}
        leitor_csv.__next__()
        for linha in leitor_csv:
           dictionary[linha[0]] = linha[13]
        
        return dictionary


def calcular_indice_correcao(dicionario_cpi, data_inicial, data_final):
    """
    Calcula o índice de correção pela inflação acumulada entre duas datas.
    """
    if not isinstance(data_inicial, str):
       data_inicial = "2023"
    
    data_inicial = data_inicial.split("-")[0]

    if float(data_inicial) < 1958 or float(data_inicial) > 2023:
        cpi_inicial = dicionario_cpi['1958']
    else:
        cpi_inicial = dicionario_cpi[data_inicial]

    cpi_final = dicionario_cpi[data_final]
    
    
    # Fórmula do índice de correção
    #indice_correcao = float(cpi_final) / float(cpi_inicial)
    indice_correcao = 1 + (float(cpi_final) - float(cpi_inicial)) / float(cpi_inicial)
    return indice_correcao

def main(budget, revenue, release_date):
    pass

if __name__ == '__main__':
    main()
