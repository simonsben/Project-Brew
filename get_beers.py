from bs4 import BeautifulSoup
from utilities import make_request

URL = 'https://www.thebeerstore.ca/wp-admin/admin-ajax.php'


def get_beers(test=False):
    """ Gets the URLs to all individual beer pages """

    # Get all data from lazy-loaded page
    content, i = '', 1
    while True:
        payload = {'action': 'beer_ajax_load_more', 'page': i, 'is_new': 0, 'query': ''}
        response = make_request(URL, data=payload)
        content += response

        if response == '' or test:
            break
        i += 1

    # Get links to every beer page
    soup = BeautifulSoup(content, 'html.parser')
    raw_beers = soup.find_all('a', class_='result_box_link', href=True)

    beers = [beer['href'] for beer in raw_beers]

    return beers
