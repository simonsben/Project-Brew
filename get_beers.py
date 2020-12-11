from utilities import make_request, dump_bad_data
from multiprocessing.dummy import Pool
from os import cpu_count
from json import loads, dumps
from json.decoder import JSONDecodeError
from time import sleep

URL = 'https://www.thebeerstore.ca/wp-admin/admin-ajax.php'


def build_payload(page):
    return {
        'action': 'beer_filter_ajax',
        'page': str(page),
        'in_stock': '',
        'searchval': '',
        'store_id': 2314
    }


def get_num_pages(response):
    meta = response['pagination']

    return meta['total_pages']


def requester(page):
    request_data = make_request(URL, data=build_payload(page))

    return loads(request_data)


def get_beers(processor, test=False):
    """ Gets the URLs to all individual beer pages """

    # Request first page to get pagination data
    base_request = requester(1)

    beers = processor(base_request)
    total_pages = get_num_pages(base_request)

    if test:
        return beers

    # Get remainder of the pages
    for index in range(2, total_pages):
        print('Requesting page %d' % index)
        beers += requester(index)

        sleep(500)

    return beers
