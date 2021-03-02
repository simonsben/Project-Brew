from json import dumps
from gzip import compress
from boto3 import client
from os import environ
from pathlib import Path


def compress_content(data):
    """
    Convert dict to a compressed byte array

    :param dict data: Data to be compressed
    :return bytes: Compressed data
    """
    json_string = dumps(data) + '\n'
    byte_string = json_string.encode('utf-8')

    return compress(byte_string)


def transfer_to_s3(data, filename):
    """
    Compress and transfer data to S3 bucket

    :param dict data: Data to be uploaded
    :param str filename: Name of file in bucket
    :return dict: S3 response
    """
    if 'bucket_name' not in environ:
        print('No bucket name available, skipping push')
        return

    compressed_data = compress_content(data)

    s3_client = client('s3')
    response = s3_client.put_object(
        Body=compressed_data,
        Bucket=environ['bucket_name'],
        Key=f'data/{filename}'
    )

    return response


def save_compressed(data, filename, directory='data/'):
    """
    Compress and save data locally
    :param dict data: Data to be saved
    :param str filename: Filename to save data as
    :param str directory: Directory to save the file in
    :return Path: Path to the created file
    """
    file_path = Path(directory) / filename
    encoded_content = compress_content(data)

    # Open file in binary writing mode
    with file_path.open('wb') as fl:
        fl.write(encoded_content)

    print('Exported data to compressed file.')

    return file_path
