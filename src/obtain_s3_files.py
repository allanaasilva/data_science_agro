"""
    Save the files that compose a shapefile, available on S3
"""
import boto3


def main():
    """Main function to obtain and save the files that compose a shapefile in
    the raw folder"""

    session = boto3.Session(profile_name='default')
    s3 = session.client('s3')

    # Nome do bucket e prefixo do arquivo
    bucket_name = 'underberg-data-lake-agro-dev'
    prefix = (
        'sandbox/processo_seletivo/'
        'processo_seletivo_2024/tabela_geometria'
    )
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)

    # Baixa e salva cada arquivo
    for obj in response.get('Contents', []):
        file_key = obj['Key']
        # O caminho local terá como base no nome do arquivo no S3 com sua
        # extensão
        local_file_path = f'data/raw/{file_key.split("/")[-1]}'
        s3.download_file(bucket_name, file_key, local_file_path)
        print(f'Arquivo salvo em: {local_file_path}')


if __name__ == "__main__":
    main()
