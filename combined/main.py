import beerClass
import functionClass
from urllib.request import urlopen

#Class Instantiation
typeClass = beerClass.Beer
listClass = beerClass.BeerList
funcClass = functionClass.collection

#Variable declaration

#Class initalization
listOfBeer = listClass()

#Strip links for all beer pages
link = funcClass.stripURL(funcClass)
print("Strip done.")

print(link[0])
listOfBeer = funcClass.collectInfo(listOfBeer, link[0])
listOfBeer.prnt()
