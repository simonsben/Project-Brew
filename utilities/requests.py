from requests import post, get
from multiprocessing.dummy import Pool
from functools import partial

def_headers = {
    'Host': 'www.thebeerstore.ca',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Referer': 'http://www.thebeerstore.ca/',
    'Accept-Language': 'en-CA,en-GB;q=0.9,en-US;q=0.8,en;q=0.7'
}
num_workers = 50


# TODO add error handling
def make_request(url, headers=def_headers, data=None):
    """
    Makes GET or POST requests
    :param url: URL of target site
    :param headers: request headers, optional
    :param data: POST request data, optional
    :return: webpage
    """
    if data is None:
        return get(url, headers=headers).text
    return post(url, data=data, headers=headers).text


def make_requests(urls, headers=def_headers, n_workers=num_workers):
    """
    Makes multiple requests
    :param urls: list of URLs to get
    :param headers: request headers, optional
    :param n_workers: number of worker threads, optional
    :return: list of webpages
    """
    workers = Pool(n_workers)
    responses = workers.map(partial(make_request, headers=headers), urls)
    workers.close()
    workers.join()

    return responses
