from get_beers import get_beers
from scrape_data import scrape_beer
from multiprocessing.dummy import Pool

# Constants
test = True
quiet = False

url_extensions = get_beers()

if not quiet: print('Collected beers.')
if test: url_extensions = url_extensions[:5]

pool = Pool(5)

beers = pool.map(scrape_beer, url_extensions)
pool.close()
pool.join()

if not quiet: print('Scraped all beers.')

print(beers)
