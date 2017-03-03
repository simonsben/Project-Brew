import beerClass
import functionClass

#Class Instantiation
typeClass = beerClass.Beer
listClass = beerClass.BeerList
funcClass = functionClass.collection

#Variable declaration

#Class initalization
listOfBeer = listClass()

#Strip links for all beer pages
link = funcClass.stripURL(funcClass)
listOfBeer = funcClass.ripList(funcClass, link)

#Print list of beers
listOfBeer.prnt()
