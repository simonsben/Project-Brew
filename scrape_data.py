from re import compile
from json import loads


fields_of_interest = {
    'ABV': 'alcohol',
    'Type': 'type',
    'Producer': 'company',
    'product_image_1': 'image_link'
}

# Pattern captures [QUANTITY, CONTAINER_TYPE, VOLUME, VOLUME_UNIT]
container_pattern = compile(r'(\d+)\sX\s(\w+)\s(\d+)\s(\w+)')
info_keys = ['quantity', 'container_type', 'volume', 'volume_unit']

index_pattern = compile(r'^(\d+)')
price_index_pattern = compile(r'Price_Metadata_(\d+)')


def get_general_information(raw_beer):
    beer = {
        'name': raw_beer['name'],
        'description': raw_beer['description'],
        'url_extension': raw_beer['custom_url']['url']
    }

    for field in raw_beer['custom_fields']:
        if field['name'] in fields_of_interest:
            key = fields_of_interest[field['name']]
            beer[key] = field['value']

    beer['alcohol'] = float(beer['alcohol']) / 100

    return beer


def digest_container(container_info, extra_price_info, beer):
    container_info_match = container_pattern.search(container_info['option_values'][0]['label'])

    container = {
        'price': container_info['price'],
        'container_index': index_pattern.search(container_info['sku'])[1],
        'sale_percent': (container_info['price'] - container_info['sale_price']) / container_info['price']
    }
    for index, key in enumerate(info_keys):
        value = container_info_match[index + 1]
        if value.isnumeric():
            value = float(value)

        container[key] = value

    container['total_volume'] = container['quantity'] * container['volume']
    container['value'] = container['total_volume'] / container['price']
    container['alcohol_value'] = container['value'] * beer['alcohol']

    current_info = extra_price_info[container['container_index']]['current_price']
    container['deposit'] = current_info['deposit']

    return container


def digest_containers(raw_beer, beer):
    containers = []

    extra_price_info = {}
    for field in raw_beer['custom_fields']:
        match = price_index_pattern.search(field['name'])
        if match is not None:
            extra_price_info[match[1]] = loads(field['value'])

    for container_info in raw_beer['variants']:
        try:
            container = digest_container(container_info, extra_price_info, beer)
            containers.append(container)
        except ZeroDivisionError:
            print('Bad container price', container_info)

    return containers


beer_level_keys = ['price', 'container_type', 'value', 'alcohol_value']


def digest_beer(raw_beer):
    beer = get_general_information(raw_beer)
    containers = digest_containers(raw_beer, beer)

    beer['containers'] = containers

    values = [beer['value'] for beer in containers]
    if len(values) <= 0:
        return None

    best_value = values.index(max(values))

    for key in beer_level_keys:
        beer[key] = containers[best_value][key]

    return beer


def digest_beers(beers):
    """ Extracts information from page of beers """
    beers = [digest_beer(beer) for beer in beers['data']]

    return beers
