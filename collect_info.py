from get_beers import get_beers
from scrape_data import scrape_beer
# from asyncio import create_task, get_event_loop
from utilities import collect, generate_headers, make_request
from time import time
from multiprocessing.dummy import Pool
from functools import partial

# Constants
test = True
base = 'https://www.thebeerstore.ca/'

headers = generate_headers()
url_extensions = get_beers(headers)

print('Collected beers. ' + str(len(url_extensions)) + ' to strip')
if test: url_extensions = url_extensions[:5]

start = time()

workers = Pool(25)
raw_beers = workers.map(partial(make_request, headers=headers), url_extensions)
workers.close()
workers.join()

beers = [scrape_beer(page) for page in raw_beers]
print(beers)

# loop = get_event_loop()
# raw_beers = loop.run_until_complete(collect(url_extensions, headers, base))
# beers = [scrape_beer(page) for page in raw_beers]

end = time()
print('Scraped all beers in ' + str(end-start) + 's')
