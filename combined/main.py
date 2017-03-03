import Class
import urllib.request

#Variable declaration
link = []
partial_url = "http://www.thebeerstore.ca/beers/search/beer_type--"
suffix = ('Ale', 'Lager', 'Malt', 'Stout')

#Class Instantiation
beerClass = Class.Beer
listClass = Class.BeerList

#Class initalization
listOfBeer = listClass()

#Strip links for all beer pages
for i in range(0, 1):
    url = partial_url + suffix[i]
    raw = urllib.request.urlopen(url)
    content = raw.read()
    start = 0
    point = 0

    while(content.find("brand-link teaser", start + 1) != -1):
        point = content.find("brand-link teaser", (start + 1))
        start = content.find("href=", point) + len("href=") + 1
        #link.append(content[start:content.find('"', start+1)])
        print(content[start:start+5])

print('Links collected.')
