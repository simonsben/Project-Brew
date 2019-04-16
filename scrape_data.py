from utilities import make_request
from bs4 import BeautifulSoup

base_url = 'http://www.thebeerstore.ca'
info_order = ['category', 'brewer', 'alcohol_content']


def scrape_beer(extension):
    url = base_url + extension
    page = make_request(url)

    soup = BeautifulSoup(page, 'html.parser')

    beer = dict()
    beer['name'] = soup.find('h1', class_='page-title').get_text()

    info_mark = soup.find('dd')
    for info in info_order:
        beer[info] = info_mark.get_text()
        info_mark = info_mark.find_next_sibling('dd')

    forms = []
    curr_form = soup.find('th', class_='large')
    while curr_form != None:
        form = dict()
        form['type'] = curr_form.get_text()

        sizes = []
        curr_size = curr_form.find_next('tr')
        while curr_size != None:
            size = {}
            info = curr_size.find_next('td')
            size['info'] = info.get_text()
            size['price'] = info.next_sibling.get_text()

            sizes.append(size)
            curr_size = curr_size.find_next_subling('tr')

        forms.append(form)
        curr_form = curr_form.find_next_sibling('th', class_='large')

    beer['forms'] = forms

    print(beer)
