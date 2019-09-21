from utilities import make_request
from bs4 import BeautifulSoup
from re import match, search

base_url = 'http://www.thebeerstore.ca'
info_order = ['category', 'brewer', 'alcohol_content']


# Scrape info for a given beer
def scrape_beer(page):
    # Initialize parser
    soup = BeautifulSoup(page, 'html.parser')

    # Initialize beer data
    beer = dict()

    # Get general information on beer
    beer['name'] = soup.find('h1', class_='page-title').get_text()
    beer['img_link'] = soup.find('img', class_='image-style-none')['src']

    info_mark = soup.find('dd')
    for info in info_order:
        beer[info] = info_mark.get_text()
        info_mark = info_mark.find_next_sibling('dd')

    beer[info_order[2]] = float(match(r'[0-9.]+', beer[info_order[2]]).group(0))

    # Collect information on beer qualities/sizes
    forms = []
    curr_form = soup.find('th', class_='large')
    while curr_form is not None:    # For each container type (ex. can, bottle, etc.)
        # Initialize form and get name of container type
        form = dict()
        form['type'] = curr_form.get_text()

        sizes = []
        curr_size = curr_form.find_next('tr')
        while curr_size is not None:    # For each quantity/size of container (ex. 12 x 355ml)
            size = {}   # Initialize size

            # Parse information
            info_mark = curr_size.find_next('td')
            info = info_mark.get_text()     # Get text in form quantity x form size
            size['quantity'] = int(match(r'^[0-9]+', info).group(0))
            size['volume'] = int(search(r'[0-9]{2,}', info[3:]).group(0))

            # Parse price
            raw_price = info_mark.next_sibling
            sale_price = raw_price.findChild('span', class_='sale-price')

            if sale_price is not None:
                size['sale'] = float(search(r'[0-9.]+', sale_price.get_text()).group(0))
            size['price'] = float(search(r'[0-9.]+', raw_price.get_text()).group(0))

            # Add size to list and get next
            sizes.append(size)
            curr_size = curr_size.find_next('tr')
        form['sizes'] = sizes

        # Add form to list
        forms.append(form)
        curr_form = curr_form.find_next_sibling('th', class_='large')

    # Add forms to beer
    beer['forms'] = forms

    return beer
