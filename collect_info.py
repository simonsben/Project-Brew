from get_beers import get_beers
from scrape_data import scrape_beer
from utilities import make_requests
from time import time
from utilities import save_compressed, load_config, commit_to_s3


def collect_data(a, b):
    """ Collects data for all beers listed on The Beer Store """

    # Constants
    load_config()
    test = False
    urls = get_beers(test)

    print('Collected beers. ', len(urls), ' to strip')
    if test: urls = urls[:15]

    start = time()
    raw_beers = make_requests(urls, processor=scrape_beer)
    beers = list(filter(lambda doc: doc is not None, raw_beers))

    end = time()
    print('Scraped all beers in', round(end - start), 's')

    # Sort beers by value
    beers = sorted(beers, key=lambda beer: beer['valAlc'], reverse=True)
    for index, _ in enumerate(beers):
        beers[index]['rank'] = index + 1

    # Make datasets
    top_10 = beers[:10]

    keg_data,  sale_data = [], []
    for beer in beers:
        on_sale = len([quantity for quantity in beer['info'] if quantity[4] == 1]) > 0
        has_keg = len([quantity for quantity in beer['info'] if quantity[0] == 'Keg'])

        if on_sale:
            sale_data.append(beer)
        if has_keg:
            keg_data.append(beer)

    sale_data = sorted(sale_data, key=lambda beer: beer['salePercent'], reverse=True)

    datasets = [beers, top_10, sale_data, keg_data]
    filenames = ['jsonAllData', 'top10jsonData', 'jsonSaleData', 'jsonKegData']
    save_compressed(datasets, filenames)
    commit_to_s3()


collect_data(None, None)
