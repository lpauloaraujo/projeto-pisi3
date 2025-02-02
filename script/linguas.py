import pandas as pd
import os


def open_parquet():
    """
    Abre o arquivo parquet e retorna um dataframe.
    """
    caminho_script = os.path.dirname(os.path.abspath(__file__))
    caminho_data = os.path.join(caminho_script, '..', 'data', 'TMDB_movie_dataset_v11(com correçao)_updated.parquet')
    df = pd.read_parquet(caminho_data)
    return df

def add_column(df):

    # contar a quantidade de linguas em cada filme
    lista_linguas = df["spoken_languages"].tolist()
    df["num_languages"] = df["spoken_languages"].apply(lambda x: len(x.split(",")) if isinstance(x, str) else 0)
    return df

def save_parquet(df):
    """
    Salva o DataFrame em um arquivo parquet na pasta 'data'.
    """
    data_dir = os.path.join(os.getcwd(), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    new_file_path = os.path.join(data_dir, 'TMDB_movie_dataset_v11(com correçao)_updated.parquet')
    df.to_parquet(new_file_path)

def main():
    df = open_parquet()
    df = add_column(df)
    save_parquet(df)

if __name__ == "__main__":

    main()