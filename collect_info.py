from get_beers import get_beers
from scrape_data import scrape_beer
from utilities import make_requests
from time import time
from json import dumps
from gzip import GzipFile


def collect_data():
    # Constants
    test = False
    urls = get_beers(test)

    print('Collected beers. ' + str(len(urls)) + ' to strip')
    if test: urls = urls[:15]

    start = time()
    raw_beers = make_requests(urls, processor=scrape_beer)
    beers = list(filter(lambda doc: doc is not None, raw_beers))
    # beers = [scrape_beer(page, url) for page, url in zip(raw_beers, urls)]
    print(beers)

    end = time()
    print('Scraped all beers in ' + str(end-start) + 's')

    # Sort beers by value
    best_values = [max([value[-2] for value in beer['info']]) for beer in beers]
    value_indexes = [index for index, _ in sorted(enumerate(best_values), key=lambda inf: inf[1], reverse=True)]

    for rank, index in enumerate(value_indexes):
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

    datasets = [beers, top_10, sale_data, keg_data]
    filenames = ['jsonAllData', 'top10jsonData', 'jsonSaleData', 'jsonKegData']

    for filename, dataset in zip(filenames, datasets):
        with GzipFile('data/' + filename + '.json.gz', 'w') as file:
            file.write((dumps(dataset) + '\n').encode('utf-8'))


collect_data()
