from bs4 import BeautifulSoup
from re import compile


info_order = ['category', 'brewer', 'alcohol_content']
value_regex = compile(r'[\w.]+')
quantity_regex = compile(r'(\d+)\sX\s(\w+)[\n ]+\s+(\d+) (\w+)')
price_regex = compile(r'\d+\.\d+(?=\s+$)')
quantity_map = {1: 'number', 3: 'capacity'}


def get_value(raw):
    return ' '.join(value_regex.findall(raw))


# Scrape info for a given beer
def scrape_beer(page):
    # Initialize parser
    soup = BeautifulSoup(page, 'html.parser')
    beer = {}

    # Get general information on beer
    title_panel = soup.find('div', class_='detail_block single_beer_eq_ht')
    beer['brewery'] = title_panel.find('h3').get_text()
    beer['brand'] = title_panel.find('h2').get_text()
    beer['description'] = title_panel.find('p').get_text()

    # Get additional information
    info_panel = soup.find('div', class_='deatil_box single_beer_dt_sec')
    for child in info_panel.findChildren('div'):
        info_name = get_value(child.find('h3').get_text())
        info_value = get_value(child.find('p').get_text())
        beer[info_name] = info_value
    beer['ABV'] = float(beer['ABV'])

    # Image link
    image_panel = soup.find('div', class_='img_thumb')
    beer['pictureLink'] = image_panel.find('img')['src']

    # Get quantity and price information
    quantity_panel = soup.find('div', class_='more_detail')
    beer['forms'] = []

    # For each type of container
    for container_panel in quantity_panel.findChildren('div', class_='more_detail_box', recursive=True):
        container_type = get_value(container_panel.find('h3').text)
        form = {'type': container_type}
        sizes = []

        # For each variant of container
        for quantity_info in container_panel.findChildren('li', class_='single_beer_details'):
            raw_container_info = quantity_regex.search(quantity_info.find('div', class_='col_1').text)
            container_info = {quantity_map[key]: int(raw_container_info.group(key)) for key in quantity_map}

            raw_price = quantity_info.find('div', class_='col_2').text
            price = float(price_regex.search(raw_price)[0])
            container_info['price'] = price
            container_info['on_sale'] = 'sale' in raw_price

            container_info['quantity_per_dollar'] = container_info['capacity'] / container_info['price']
            container_info['alcohol_per_dollar'] = container_info['quantity_per_dollar'] * beer['ABV'] / 100

            sizes.append(container_info)

        form['sizes'] = sizes
        beer['forms'].append(form)

    return beer
