from get_beers import get_beers
from scrape_data import scrape_beer
from utilities import make_requests
from time import time
from utilities import save_compressed, commit_to_s3
from datetime import date


def handler(event, context):
    """ Collects data for all beers listed on The Beer Store """

    # Constants
    test = False
    urls = get_beers(test)

    print('Collected beers. ', len(urls), ' to strip')
    if test: urls = urls[:15]

    start = time()
    raw_beers = make_requests(urls, processor=scrape_beer)
    beers = list(filter(lambda beer: beer is not None, raw_beers))

    end = time()
    print('Scraped all beers in', round(end - start), 's')

    # Sort beers by value
    beers = sorted(beers, key=lambda beer: beer['alcohol_value'], reverse=True)
    for index, _ in enumerate(beers):
        beers[index]['rank'] = index + 1

    beer_data = {
        'beers': beers,
        'collection_date': str(date.today())
    }

    save_compressed(beer_data, 'beers.json.gz')
    commit_to_s3()
