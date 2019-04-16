import csv
data = open("temp.dat")
content = data.read()

#Beer name
begin = content.find('only-desktop')
beer_name_location = content.find('class="filter"', begin)
beer_name_location = content.find('class="filter"', beer_name_location + 1) + len('class="filter"') + 1
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
i = 0
type = []
size = []
price = []
quantity = []
type_location = alcohol_location

while(content.find('<th class="large">', type_location) != -1):
    type_location = content.find('<th class="large">', type_location + 1) + len('<th class="large">')
    type.append(content[type_location:content.find('<', type_location)])
    next_type = content.find('<th class="large">', type_location + 1)

    type_end = content.find('</tbody>', type_location + 1)
    quantity_location = content.find('<td class="size">', type_location + 1, type_end)

    while(quantity_location != -1):
        #Extract Quantity
        quantity_location += len('<td class="size">')
        quantity.append(int(content[quantity_location:content.find('&', quantity_location)-1]))
        #Extract Size
        size_location = content.find(type[i], quantity_location) + len(type[i]) + 1
        size.append(int(content[size_location:content.find('&', size_location)]))
        #Extract price
        price_location = content.find('price', size_location) + len('price') + 3
        price.append(float(content[price_location:content.find('<', price_location)]))
        #Calculate next quantity location (and whether it exists)
        quantity_location = content.find('<td class="size">', quantity_location + 1, type_end)
    #Add break between types
    quantity.append(' ')
    size.append(' ')
    price.append(' ')
    i += 1 #Increment type


with open('Site.csv', 'wb') as site_file:
    writer = csv.writer(site_file)
    writer.writerow(beer_name)
    writer.writerow(brewer)
    writer.writerow(type)
    writer.writerow(quantity)
    writer.writerow(size)
    writer.writerow(price)

data.close()
