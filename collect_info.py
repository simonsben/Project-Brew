from get_beers import get_beers
from scrape_data import digest_beers
from time import time
from utilities import save_compressed, commit_to_s3
from datetime import date


def handler(event, context):
    """ Collects data for all beers listed on The Beer Store """
    test = False

    # Collect beer
    start = time()
    beers = get_beers(digest_beers, test)
    end = time()

    print('Scraped all beers in', round(end - start), 's')

    # Sort beers by value
    beers = [beer for beer in beers if beer is not None]
    beers = sorted(beers, key=lambda beer: beer['alcohol_value'], reverse=True)

    for index, _ in enumerate(beers):
        beers[index]['rank'] = index + 1

    # Package data
    beer_data = {
        'beers': beers,
        'collection_date': str(date.today())
    }

    save_compressed(beer_data, 'beers.json.gz')
    commit_to_s3()


handler(None, None)
