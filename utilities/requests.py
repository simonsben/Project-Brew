from urllib.request import Request, urlopen
from gzip import GzipFile
from async_timeout import timeout
from asyncio import gather, create_task
from aiohttp import ClientSession
from time import sleep
from requests import post, get


async def make_async(session, url):
    with timeout(5):
        async with session.get(url) as resp:
            return await resp.text()


def make_request(url, headers, data=None):
    if data is None:
        return get(url, headers=headers).text
    return post(url, data=data, headers=headers)

# def make_request(url, headers):
#     req = Request(url, headers=headers)
#     raw = urlopen(req)
#
#     res_header = raw.info()
#     if 'Content-Encoding' in res_header:
#         if res_header['Content-Encoding'] == 'gzip':
#             raw = GzipFile(fileobj=raw)
#
#     page = raw.read().decode('utf-8')
#
#     return page


async def collect(extensions, headers, base):
    tasks = []
    count = 0

    async with ClientSession(headers=headers) as session:
        for ext in extensions:
            count += 1
            if count > 20:
                sleep(.25)
                count = 0

            url = base + ext
            task = create_task(make_async(session, url))
            tasks.append(task)

        responses = await gather(*tasks)

    return responses
