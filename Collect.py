#import csv
from urllib.request import urlopen
raw = urlopen("http://www.thebeerstore.ca/beers/1857-kolsch-style-ale")
page = raw.read()
page = page.decode("utf-8")

#data = open("temp.dat")
#page = data.read()

#Beer name
begin = page.find('only-desktop')
beer_name_location = page.find('class="page-title"', begin) + len('class="page-title"') + 1
#beer_name_location = page.find('class="filter"', beer_name_location + 1) + len('class="filter"') + 1
beer_name = page[beer_name_location:page.find('<', beer_name_location + 1)]

#Brewer
brewer_location = page.find('Brewer', beer_name_location)
brewer_location = page.find('<dd>', brewer_location) + len('<dd>')
brewer = page[brewer_location:page.find('<', brewer_location)]

#Alcohol content
alcohol_location = page.find('Alcohol Content', brewer_location)
alcohol_location = page.find('<dd>', alcohol_location) + len('<dd>')
alcohol = page[alcohol_location:page.find('<', alcohol_location)-1]

#Initializing arrays and variables required
i = 0
type = []
size = []
price = []
quantity = []
type_location = alcohol_location

while(page.find('<th class="large">', type_location) != -1):
    type_location = page.find('<th class="large">', type_location + 1) + len('<th class="large">')
    type.append(page[type_location:page.find('<', type_location)])
    next_type = page.find('<th class="large">', type_location + 1)

    type_end = page.find('</tbody>', type_location + 1)
    quantity_location = page.find('<td class="size">', type_location + 1, type_end)

    while(quantity_location != -1):
        #Extract Quantity
        quantity_location += len('<td class="size">')
        quantity.append(int(page[quantity_location:page.find('&', quantity_location)-1]))
        #Extract Size
        size_location = page.find(type[i], quantity_location) + len(type[i]) + 1
        size.append(int(page[size_location:page.find('&', size_location)]))
        #Extract price
        price_location = page.find('price', size_location) + len('price') + 3
        price.append(float(page[price_location:page.find('<', price_location)]))
        #Calculate next quantity location (and whether it exists)
        quantity_location = page.find('<td class="size">', quantity_location + 1, type_end)

        print(beer_name)
    #Add break between types
    quantity.append(' ')
    size.append(' ')
    price.append(' ')
    i += 1 #Increment type

'''
with open('Site.csv', 'wb') as site_file:
    writer = csv.writer(site_file)
    writer.writerow(beer_name)
    writer.writerow(brewer)
    writer.writerow(type)
    writer.writerow(quantity)
    writer.writerow(size)
    writer.writerow(price)

data.close()
'''
