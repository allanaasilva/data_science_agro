"""
    Save data from the 'talhao' table (Postgres) to the 'data/raw' folder, as
    a parquet file
"""
import os
from sqlalchemy import create_engine
import pandas as pd


def main():
    """Main function to save data from the 'talhao' table to 'data/raw' as
    a parquet file"""

    local_file_path = 'data/raw/'

    # String de conexão da variável de ambiente
    conn_str = os.environ['DATABASE_URL']
    engine = create_engine(conn_str)

    # Consulta SQL
    query = '''
    SELECT *
    FROM talhao t
    '''

    # Paginação para otimização
    chunk_size = 10000

    chunks = pd.read_sql_query(query, engine, chunksize=chunk_size)
    talhao = pd.concat(chunks)

    talhao.to_parquet(local_file_path + 'talhao.parquet', index=False)
    print(f'Arquivo salvo em: {local_file_path}talhao.parquet')


if __name__ == "__main__":
    main()
