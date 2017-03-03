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
print(link[281])

#Pull information from each beer page
listOfBeer = funcClass.ripList(funcClass, link)

#Sort list of beers by mL / $
listOfBeer.sort('value')

with open('dataTaken.txt', 'w+') as f:
    for i in range(0, listOfBeer.length):
        print(listOfBeer.prntSng(i), file=f)

#Print list of beers
listOfBeer.prnt()
