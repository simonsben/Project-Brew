from json import dumps, load
from gzip import open
from boto3 import resource
from os import listdir, environ
from pathlib import Path


def save_compressed(data, filename, directory='data/'):
    """ Takes list of datasets and filenames and saves them as GZIPed JSON """
    directory = Path(directory) if 'bucket_name' not in environ else Path('/tmp/')

    encoded_content = (dumps(data) + '\n').encode('utf-8')
    with open(directory / filename, 'w') as fl:
        fl.write(encoded_content)

    print('Exported data to compressed files.')


def commit_to_s3():
    """ Exports config data from tmp/ to target bucket """
    if 'bucket_name' not in environ:
        print('No bucket name available, skipping push')
        return

    source = Path('/tmp/')
    dest = Path('data/')

    s3 = resource('s3')
    for fl in listdir('/tmp'):
        s3.meta.client.upload_file(str(source / fl), environ['bucket_name'], str(dest / fl))
        print(fl + 'saved to S3')
