from bs4 import BeautifulSoup
from utilities import make_request

url = 'http://www.thebeerstore.ca/beers/search/'


# Function to get url extensions of each beer
def get_beers():
    page = make_request(url)

    soup = BeautifulSoup(page, 'html.parser')
    raw_beers = soup.find_all('a', class_='brand-link teaser', href=True)

    beers = [beer['href'] for beer in raw_beers]

    return beers
