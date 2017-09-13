from urllib.request import urlopen, URLError
import beerClass
import multiprocessing

def readURL(url):
    raw = urlopen(url)
    content = raw.read()
    content = content.decode("utf-8")
    return content
def stripURL():
    link = []
    url = "http://www.thebeerstore.ca/beers/search"

    content = readURL(url)
    start = 0
    point = 0

    while(content.find("brand-link teaser", start + 1) != -1):
        point = content.find("brand-link teaser", start + 1)
        start = content.find("href=", point) + len("href=") + 1
        link.append('http://www.thebeerstore.ca' + content[start:content.find('"', start+1)])

    print('Strip done.')
    return link

def collectInfo(url):
    content = readURL(url)

    #Beer picture
    begin = content.find('brand-image-container')
    beer_link_location = content.find('src', begin) + len('src') + 2
    beer_link = content[beer_link_location:content.find('"', beer_link_location)]

    #Beer name
    begin = content.find('only-desktop', begin)
    beer_name_location = content.find('class="page-title"', begin) + len('class="page-title"') + 1
    beer_name = content[beer_name_location:content.find('<', beer_name_location + 1)]

    #Brewer
    brewer_location = content.find('Brewer', beer_name_location)
    brewer_location = content.find('<dd>', brewer_location) + len('<dd>')
    brewer = content[brewer_location:content.find('<', brewer_location)]

    #Alcohol content
    alcohol_location = content.find('Alcohol Content', brewer_location)
    alcohol_location = content.find('<dd>', alcohol_location) + len('<dd>')
    alcohol = content[alcohol_location:content.find('<', alcohol_location)-1]

    #Initializing arrays and variables required
    type_location = alcohol_location
    sale = 0

    setOfBrews = []
    while(content.find('<th class="large">', type_location) != -1):
        type_location = content.find('<th class="large">', type_location + 1) + len('<th class="large">')
        type = content[type_location:content.find('<', type_location)]
        type_end = content.find('</tbody>', type_location + 1)

        quantity_location = content.find('<td class="size">', type_location + 1, type_end)

        while(quantity_location != -1):
            #Extract Quantity
            quantity_location += len('<td class="size">')
            quantity = int(content[quantity_location:content.find('&', quantity_location)-1])

            #Extract Size
            size_location = content.find('&', quantity_location + 5) - 7
            size_location = content.find(' ', size_location)
            #size_location = content.find(';', quantity_location + 15) + 3 #content.find(type, quantity_location) + len(type) + 1
            size = int(content[size_location:content.find('&', size_location)])

            #Extract price
            price_location = content.find('price', size_location) + len('price') + 3
            sale_price_location = price_location
            salePrice = 0
            if(content.find('sale-price', price_location, price_location + 50) != -1):
                price_location = content.find('$', price_location) + 1
                sale_price_location = content.find('sale-price', sale_price_location)
                sale_price_location = content.find('$', sale_price_location + 1) + 1
                salePrice = float(content[sale_price_location:content.find('<', sale_price_location)])
                sale = 1
            price = float(content[price_location:content.find('<', price_location)])
            #Calculate next quantity location (and whether it exists)
            quantity_location = content.find('<td class="size">', quantity_location + 1, type_end)
            setOfBrews.append(beerClass.Beer(brewer, beer_name, type, int(size), int(quantity), float(alcohol[0]), float(price), sale, salePrice, beer_link, url))
            sale = 0

    print('Done' + beer_name)

    return setOfBrews

def ripList(links):
    listOfBeer = beerClass.BeerList()

    results = []
    with multiprocessing.Pool(processes=35) as p:
        results = p.map(collectInfo, links)

    for brand in results:
        for brew in brand:
            listOfBeer.append(brew)

    return listOfBeer

def connectionCheck():
    try:
        urlopen('http://www.thebeerstore.ca/', timeout=2)
        return True
    except URLError as err:
        return False
