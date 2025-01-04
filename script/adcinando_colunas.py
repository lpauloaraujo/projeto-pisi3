import os
import pandas as pd
from lucratividade import main as classificar_lucratividade

def open_parquet():
    """
    Abre o arquivo parquet e retorna um dataframe.
    """
    caminho_script = os.path.dirname(os.path.abspath(__file__))
    caminho_data = os.path.join(caminho_script, '..', 'data', 'TMDB_movie_dataset_v11.parquet')
    df = pd.read_parquet(caminho_data)
    return df

def add_column(df):
    """
    Adiciona uma coluna com a lucratividade calculada.
    """
    # Verificar se as colunas 'budget' e 'revenue' existem
    if 'budget' not in df.columns or 'revenue' not in df.columns:
        raise KeyError("As colunas 'budget' e 'revenue' devem existir no DataFrame.")
    
    # Adicionar a coluna 'lucratividade'
    df['lucratividade'] = df.apply(lambda row: classificar_lucratividade(row['budget'], row['revenue']), axis=1)
    return df

def save_parquet(df):
    """
    Salva o DataFrame em um arquivo parquet na pasta 'data'.
    """
    data_dir = os.path.join(os.getcwd(), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    new_file_path = os.path.join(data_dir, 'TMDB_movie_dataset_v11(com correçao).parquet')
    df.to_parquet(new_file_path)

def main():
    df = open_parquet()
    df = add_column(df)
    save_parquet(df)

if __name__ == '__main__':
    main()