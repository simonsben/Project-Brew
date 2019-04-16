from get_beers import get_beers
from scrape_data import scrape_beer

# Constants
test = True
quiet = False

url_extensions = get_beers()

if not quiet: print('Collected beers.')
if test: url_extensions = url_extensions[:50]

beers = []
for ext in url_extensions:
    beers.append(scrape_beer(ext))

if not quiet: print('Scraped all beers.')

print(beers)
