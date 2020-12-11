from requests import post, get
from requests.exceptions import ReadTimeout
from multiprocessing.dummy import Pool
from functools import partial
from time import sleep

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
timeout = 10


def make_request(url, headers=None, data=None, sleep_process=False, processor=None, retries=1):
    """
    Makes GET or POST requests
    :param str url: URL of target site
    :param dict headers: request headers, optional
    :param dict data: POST request data, optional
    :param bool sleep_process: Whether to sleep after making request (rough rate limiting)
    :param function processor: Function to be applied to the data
    :param int retries: Number of retries for the request
    :return str: webpage
    """

    if headers is None:
        headers = def_headers

    for i in range(retries + 1):
        try:
            if data is None:
                tmp = get(url, headers=headers, timeout=timeout).text
            else:
                tmp = post(url, data=data, headers=headers, timeout=timeout).text
            break
        except ReadTimeout:
            print('WARNING: %s request timed-out' % url)
            tmp = ''

    if sleep_process:
        sleep(.5)
    if processor is None:
        return tmp
    return processor(tmp, url)


def make_requests(urls, headers=None, n_workers=4, processor=None):
    """
    Makes multiple requests
    :param urls: list of URLs to get
    :param headers: request headers, optional
    :param n_workers: number of worker threads, optional
    :param processor: Function to apply to the downloaded page
    :return: list of webpages
    """
    if headers is None:
        headers = def_headers

    workers = Pool(n_workers)
    responses = workers.map(partial(make_request, headers=headers, processor=processor), urls)
    workers.close()
    workers.join()

    return responses
