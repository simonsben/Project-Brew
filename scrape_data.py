from bs4 import BeautifulSoup
from re import compile


value_regex = compile(r'[\w.]+')
quantity_regex = compile(r'(\d+)\sX\s(\w+)\s(\d+)\s(\w+)')
price_regex = compile(r'\d+\.\d+(?=\s+$)')
non_numeric_regex = compile(r'[a-zA-Z ]+')
sale_regex = compile(r'(?<=\$)(\d+\.\d+)')
brand_pattern = compile(r'(\w[\w\s]+\w)')
title_panel_pattern = compile(r'[\n\s]{2,}')

quantity_map = {1: 'number', 2: 'container_type', 3: 'capacity'}
info_map = {'Type': 'kind', 'Category': 'category', 'Country': 'country', 'ABV': 'alcohol'}

is_numeric = lambda info: non_numeric_regex.search(info) is None
alc_value_key = 'alcohol_value'
value_key = 'value'


def int_cast(value):
    """ Casts value to integer """
    if is_numeric(value):
        return int(value)
    return value


def get_value(raw):
    """ Extracts info """
    return ' '.join(value_regex.findall(raw))


def get_keg_return(size):
    """ Estimates the return value of the keg """
    if not isinstance(size, int):
        size = int(size)

    if size < 25000:
        return 20
    return 50


def get_general_info(page, url):
    """
    Initializes beer object and extracts general info from page

    :param str page: Raw source of the page
    :param str url: URL of the page
    :return tuple[dict, BeautifulSoup]:
    """
    # Initialize parser
    soup = BeautifulSoup(page, 'html.parser')
    beer = {
        'page_link': url
    }

    # Get general information on beer
    title_panel = soup.find('div', class_='desc')
    content = title_panel_pattern.sub('\n', title_panel.get_text()).split('\n')[1:-1]

    (beer['brand'], beer['name']) = content[:2]
    beer['description'] = ' '.join(content[2:])

    # Get additional information
    info_panel = soup.find('div', class_='detail-coloums deatil_box single_beer_dt_sec')
    for child in info_panel.findChildren('div'):
        info_name = info_map[get_value(child.find('h3').get_text())]
        info_value = get_value(child.find('p').get_text())
        beer[info_name] = info_value
    beer['alcohol'] = float(beer['alcohol'])

    # Image link
    image_panel = soup.find('div', class_='img_thumb')
    beer['picture_link'] = image_panel.find('img')['src']

    return beer, soup


def get_container_info(quantity_info, beer):
    """
    Extracts information about a specific container size for the given beer

    :param BeautifulSoup quantity_info: Beautiful Soup object for the div containing the information
    :param dict beer: Beer
    :return dict: Information about the container
    """
    raw_container_info = quantity_regex.search(quantity_info.find('div', {'class': 'col_1'}).text)
    container_info = {quantity_map[key]: int_cast(raw_container_info.group(key)) for key in quantity_map}

    raw_price = quantity_info.find('div', class_='col_3').text
    price = float(price_regex.search(raw_price)[0])
    container_info['price'] = price
    on_sale = int('sale' in raw_price)

    # If beer is on sale, get sale price
    if on_sale:
        container_info['sale_price'] = container_info['price']
        container_info['price'] = float(sale_regex.search(raw_price)[1])
        container_info['sale_percent'] = (1 - container_info['sale_price'] / container_info['price']) * 100

    # Remove keg deposit cost
    if container_info['container_type'] == 'Keg':
        capacity = container_info['capacity']

        keg_return = get_keg_return(capacity)

        container_info['price'] -= keg_return
        if on_sale:
            container_info['sale_price'] -= keg_return

    container_info[value_key] = container_info['capacity'] * container_info['number'] / container_info['price']
    container_info[alc_value_key] = container_info[value_key] * beer['alcohol'] / 100

    return container_info


def calculate_overall_stats(beer):
    """ Computes overall information about the beer (ex. best possible value) """
    # Additional legacy parameters
    sale_percent = [beer['sale_percent'] for beer in beer['info'] if 'sale_percent' in beer] + [0]
    raw_value = [beer[value_key] for beer in beer['info']]
    alcohol_value = [beer[alc_value_key] for beer in beer['info']]

    best_sale = max(sale_percent)
    best_value = max(raw_value)
    best_alc_value = max(alcohol_value)

    beer['main'] = alcohol_value.index(best_alc_value)
    beer['price'] = beer['info'][beer['main']]['price']
    beer['value'] = best_value
    beer['alcohol_value'] = best_alc_value
    beer['sale_percent'] = best_sale


# Scrape info for a given beer
def scrape_beer(page, url):
    """
    Scrapes the beer information from the given page

    :param str page: Page to-be-scraped
    :param str url: URL of the page
    :return dict: Information about the beer on the page
    """
    try:
        beer, soup = get_general_info(page, url)
    except (TypeError, AttributeError):
        print('Bad page', url)
        return None

    # Get quantity and price information
    quantity_panel = soup.find('div', class_='tabbed-deatil-desc')
    beer['info'] = []

    # For each type of container
    for container_panel in quantity_panel.findChildren('div', class_='more_detail_box', recursive=True):
        sizes = []

        # For each variant of container
        for quantity_info in container_panel.findChildren('li', class_='d-column d-row option _cart'):
            try:
                sizes.append(get_container_info(quantity_info, beer))
            except:
                print('Bad container', str(quantity_info))

        beer['info'] += sizes

    calculate_overall_stats(beer)

    return beer
