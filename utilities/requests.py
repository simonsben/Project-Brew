from urllib.request import Request, urlopen
from gzip import GzipFile

def_headers = {
    'Host': 'www.thebeerstore.ca',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Referer': 'http://www.thebeerstore.ca/',
    'Accept-Language': 'en-CA,en-GB;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cookie': 'sucuri_cloudproxy_uuid_c32eb98e2=0939486cecdf4c071c4b6a85ec316a8c'
}


def make_request(url, header=None):
    headers = def_headers if header is None else header

    req = Request(url, headers=headers)
    raw = urlopen(req)

    res_header = raw.info()
    if 'Content-Encoding' in res_header:
        if res_header['Content-Encoding'] == 'gzip':
            raw = GzipFile(fileobj=raw)

    page = raw.read().decode('utf-8')

    return page
