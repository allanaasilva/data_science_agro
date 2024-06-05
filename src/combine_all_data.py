"""
    Join and save data (meteorological, 'talhao' and spatial data)
"""
import os
from sqlalchemy import create_engine
import pandas as pd
import geopandas as gpd


def main():
    """Main function to join meteorological, 'talhao' and spatial data and save
    the combined data as a shapefile"""

    local_file_path = 'data/interim/'
    # Arquivo 'talhao.parquet' previamente salvo
    talhao_file = 'data/raw/talhao.parquet'
    talhao = pd.read_parquet(talhao_file)
    # Dados geoespaciais
    shp_file = 'data/raw/tabela_geometria.shp'
    tabela_geometria = gpd.read_file(shp_file)

    # String de conexão da variável de ambiente
    conn_str = os.environ['DATABASE_URL']
    engine = create_engine(conn_str)

    # Consulta SQL para obter os dados da tabela 'meteorologia'
    query_meteorologia = '''
    SELECT id_talhao,
    leitura_valor,
    periodo_pluviometrico_inicio,
    periodo_pluviometrico_fim
    FROM meteorologia
    WHERE id_talhao IN (
        SELECT id_talhao
        FROM talhao
        WHERE ocupacao = 'Soja'
    )
    '''

    meteorologia = pd.read_sql_query(query_meteorologia, engine)

    # Será mantido um valor de leitura por id_talhao. Este valor será a soma
    # do período
    meteorologia['leitura_valor'] = pd.to_numeric(meteorologia[
        'leitura_valor'], errors='coerce')
    meteorologia = meteorologia.groupby('id_talhao').agg({
        'leitura_valor': 'sum',
        'periodo_pluviometrico_inicio': 'min',
        'periodo_pluviometrico_fim': 'max'}).reset_index()

    combined_data = pd.merge(talhao, meteorologia, on='id_talhao', how='left')
    combined_data.to_parquet(os.path.join(local_file_path,
                                          'talhao_meteorologia_data.parquet'))
    # Para que os nomes das colunas coincidam com a tabela de geometria
    combined_data = combined_data.rename(columns={
        'codigo_talhao': 'cdg_tlh',
        'fazenda_nome': 'fznd_nm'
        })

    # A forma de relacionar os dados espaciais aos demais é pelo nome da
    # fazenda e pelo código do talhão. Porém, o nome da fazenda não coincide
    # nas duas tabelas. Portanto, será feita uma substituição fictícia para
    # que seja possível realizar o merge
    substituicoes = {
        'Boa Vista': 'F1',
        'Cachoeira': 'F2',
        'Felicidade': 'F6',
        'Nova Esperança': 'F7',
        'Repouso': 'F8',
        'Floresta Azul': 'F9'
    }
    tabela_geometria['fznd_nm'] = tabela_geometria['fznd_nm'].replace(
        substituicoes)

    # Merge GeoDataFrame com o DataFrame talhao e meteorologia
    merge_columns = ['fznd_nm', 'cdg_tlh']
    talhao_with_geo_info = tabela_geometria.merge(combined_data,
                                                  on=merge_columns,
                                                  how='right')

    # Salvar o GeoDataFrame resultante como um shapefile
    output_file = os.path.join(local_file_path, 'talhao_with_geo_info.shp')
    talhao_with_geo_info.to_file(output_file, driver='ESRI Shapefile')
    print(f'Arquivo final combinado salvo em: {output_file}')


if __name__ == "__main__":
    main()
