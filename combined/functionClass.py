from urllib.request import urlopen
import beerClass

class collection:
    def readURL(self, url):
        raw = urlopen(url)
        content = raw.read()
        content = content.decode("utf-8")
        return content
    def stripURL(self):
        link = []
        url = "http://www.thebeerstore.ca/beers/search"

        content = collection.readURL(collection, url)
        start = 0
        point = 0

        while(content.find("brand-link teaser", start + 1) != -1):
            point = content.find("brand-link teaser", start + 1)
            start = content.find("href=", point) + len("href=") + 1
            link.append('http://www.thebeerstore.ca' + content[start:content.find('"', start+1)])

        print('Strip done.')
        return link

    def collectInfo(self, url, listOfBeer):
        content = collection.readURL(collection, url)
        #Class Instantiation
        typeClass = beerClass.Beer

        #Beer name
        begin = content.find('only-desktop')
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
                if(content.find('sale-price', price_location, price_location + 50) != -1):
                    price_location = content.find('sale-price', price_location)
                    price_location = content.find('$', price_location + 1) + 1
                    sale = 1
                price = float(content[price_location:content.find('<', price_location)])
                #Calculate next quantity location (and whether it exists)
                quantity_location = content.find('<td class="size">', quantity_location + 1, type_end)
                brew = typeClass(brewer, beer_name, type, int(size), int(quantity), float(alcohol[0]), float(price), sale)
                listOfBeer.append(brew)
                sale = 0

        return listOfBeer

    def ripList(self, links):
        listClass = beerClass.BeerList
        listOfBeer = listClass()
        linkLength = len(links)
        for i in range(0, linkLength):
            listOfBeer = collection.collectInfo(listOfBeer, links[i], listOfBeer)
            print(str(i) + ' Beers complete of ' + str(linkLength) + '.')
        return listOfBeer
