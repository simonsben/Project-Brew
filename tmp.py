# from requests import post
#
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
#
# URL = 'https://www.thebeerstore.ca/wp-admin/admin-ajax.php'
#
# content = ''
# i = 1
# while True:
#     tmp = post(URL, headers=def_headers, data={'action': 'beer_ajax_load_more', 'page': i, 'is_new': 0, 'query': ''})
#     if tmp.text == '':
#         break
#     content += tmp.text
#     i += 1
#
# print(content)
#


from get_beers import get_beers

get_beers(def_headers)