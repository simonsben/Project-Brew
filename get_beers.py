from bs4 import BeautifulSoup
from utilities import make_request

url = 'https://www.thebeerstore.ca/wp-admin/admin-ajax.php'


# Function to get url extensions of each beer
def get_beers(headers):
    # Get all data from lazy-loaded page
    content, i = '', 1
    while True:
        payload = {'action': 'beer_ajax_load_more', 'page': i, 'is_new': 0, 'query': ''}
        response = make_request(url, headers, payload)
        if response.text == '':
            break
        content += response.text
        i += 1

    soup = BeautifulSoup(content, 'html.parser')
    raw_beers = soup.find_all('a', class_='result_box_link', href=True)

    beers = [beer['href'] for beer in raw_beers]

    return beers
