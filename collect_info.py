from get_beers import get_beers
from scrape_data import scrape_beer
from utilities import make_requests
from time import time

# Constants
test = True
urls = get_beers()

print('Collected beers. ' + str(len(urls)) + ' to strip')
if test: urls = urls[:5]

start = time()
raw_beers = make_requests(urls)
# beers = [scrape_beer(page) for page in raw_beers]
print(raw_beers)

end = time()
print('Scraped all beers in ' + str(end-start) + 's')
