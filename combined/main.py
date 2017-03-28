import beerClass
import functionClass
import jsonOutput

#Class Instantiation
typeClass = beerClass.Beer
listClass = beerClass.BeerList
funcClass = functionClass.collection

#Variable declaration

#Class initalization
listOfBeer = listClass()

#Strip links for all beer pages
link = funcClass.stripURL(funcClass)

#Pull information from each beer page
listOfBeer = funcClass.ripList(funcClass, link)

#Sort list of beers by mL / $
listOfBeer.sort('valueAlcohol')

#Output list of beers to text summary
with open('dataTaken.txt', 'w+') as f:
    for i in range(0, listOfBeer.length):
        print(listOfBeer.prntSng(i), file=f)

#Output list of beers to JSON
with open('jsonOut.txt', 'w+') as f:
    print(jsonOutput.dataToFile.toJSON(jsonOutput.dataToFile, listOfBeer), file=f)

#Print list of beers
#listOfBeer.prnt()
