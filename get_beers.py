from utilities import make_request
from json import loads
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


def requester(page, retries=1):
    for retry_number in range(retries + 1):
        try:
            request_data = make_request(URL, data=build_payload(page))
            return loads(request_data)
        except JSONDecodeError:
            print('WARNING: decode error, pausing before retry %d' % (retry_number + 1))
            sleep(2)
            continue

    return


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
        print('%2d of %d' % (index, total_pages))
        beers += processor(requester(index))

        sleep(1)

    return beers
