from get_beers import get_beers
from scrape_data import scrape_beer

# Constants
test = True
quiet = False

url_extensions = get_beers()

if not quiet: print('Collected Beers.')
if test: url_extensions = url_extensions[:1]

for ext in url_extensions:
    scrape_beer(ext)
