from bs4 import BeautifulSoup
from re import compile


value_regex = compile(r'[\w.]+')
quantity_regex = compile(r'(\d+)\sX\s(\w+)[\n ]+\s+(\d+) (\w+)')
price_regex = compile(r'\d+\.\d+(?=\s+$)')
non_numeric_regex = compile(r'[a-zA-Z ]+')
sale_regex = compile(r'(?<=\$)(\d+\.\d+)')
quantity_map = {1: 'number', 2: 'container_type', 3: 'capacity'}
info_map = {'Type': 'kind', 'Category': 'category', 'Country': 'country', 'ABV': 'alcohol'}
is_numeric = lambda info: non_numeric_regex.search(info) is None
container_order = [
    'container_type', 'capacity', 'number',
    'price', 'on_sale', 'sale_price', 'sale_percent',
    'quantity_per_dollar', 'alcohol_per_dollar'
]


def int_cast(value):
    if is_numeric(value):
        return int(value)
    return value


def get_value(raw):
    return ' '.join(value_regex.findall(raw))


# Scrape info for a given beer
def scrape_beer(page, url):
    # Initialize parser
    soup = BeautifulSoup(page, 'html.parser')
    beer = {}

    # Ensure that a valid page was returned
    try:
        title_panel = soup.find('div', class_='detail_block single_beer_eq_ht')
        beer['brand'] = title_panel.find('h3').get_text()
    except AttributeError:
        print('Bad page', url)
        return None

    # Get general information on beer
    beer['name'] = title_panel.find('h2').get_text()
    beer['description'] = title_panel.find('p').get_text()
    beer['pageLink'] = url
    beer['main'] = 0

    # Get additional information
    info_panel = soup.find('div', class_='deatil_box single_beer_dt_sec')
    for child in info_panel.findChildren('div'):
        info_name = info_map[get_value(child.find('h3').get_text())]
        info_value = get_value(child.find('p').get_text())
        beer[info_name] = info_value
    beer['alcohol'] = float(beer['alcohol'])

    # Image link
    image_panel = soup.find('div', class_='img_thumb')
    beer['pictureLink'] = image_panel.find('img')['src']

    # Get quantity and price information
    quantity_panel = soup.find('div', class_='more_detail')
    beer['info'] = []

    # For each type of container
    for container_panel in quantity_panel.findChildren('div', class_='more_detail_box', recursive=True):
        # container_type = get_value(container_panel.find('h3').text)
        sizes = []

        # For each variant of container
        for quantity_info in container_panel.findChildren('li', class_='single_beer_details'):
            raw_container_info = quantity_regex.search(quantity_info.find('div', class_='col_1').text)
            container_info = {quantity_map[key]: int_cast(raw_container_info.group(key)) for key in quantity_map}

            raw_price = quantity_info.find('div', class_='col_2').text
            price = float(price_regex.search(raw_price)[0])
            container_info['price'] = price
            container_info['on_sale'] = int('sale' in raw_price)

            # If beer is on sale, get sale price
            if container_info['on_sale']:
                container_info['sale_price'] = container_info['price']
                container_info['price'] = float(sale_regex.search(raw_price)[1])
                container_info['sale_percent'] = (1 - container_info['sale_price'] / container_info['price']) * 100
            else:
                container_info['sale_price'] = 0
                container_info['sale_percent'] = 0

            container_info['quantity_per_dollar'] = container_info['capacity'] * container_info['number'] / container_info['price']
            container_info['alcohol_per_dollar'] = container_info['quantity_per_dollar'] * beer['alcohol'] / 100

            sizes.append([container_info[info] for info in container_order])

        # form['sizes'] = sizes
        beer['info'] += sizes

    return beer
