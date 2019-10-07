from json import dumps, load
from gzip import GzipFile
from boto3 import resource
from os import listdir
from pathlib import Path


def save_compressed(datasets, filenames, directory='data/'):
    """ Takes list of datasets and filenames and saves them as GZIPed JSON """
    directory = Path(directory) if not aws_execution else Path('/tmp/')

    for filename, dataset in zip(filenames, datasets):
        with GzipFile(directory / (filename + '.json.gz'), 'w') as file:
            file.write((dumps(dataset) + '\n').encode('utf-8'))

    print('Exported data to compressed files.')


def load_config():
    """ Loads configuration data form file """
    path = Path('config.json')

    # If config file is present
    if path.exists():
        # Load file
        with path.open('r') as fl:
            data = load(fl)

        # Add variables to global scope
        for key in data:
            globals()[key] = data[key]

        print('Config data loaded.')
        return
    print('No config present.')


def commit_to_s3():
    """ Exports config data from tmp/ to target bucket """
    if not aws_execution:
        print('Not running on AWS, will not export data to bucket')
        return

    direcotry = Path('/tmp/')
    s3 = resource('s3')
    for fl in listdir('/tmp'):
        s3.meta.client.upload_file(direcotry / fl, bucket_name, 'data/'+fl)
        print(fl + 'saved to S3')
