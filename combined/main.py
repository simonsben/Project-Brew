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
topTenList = listClass()
saleList = listClass()
kegList = listClass()

#Strip links for all beer pages
link = funcClass.stripURL(funcClass)

#Pull information from each beer page
listOfBeer = funcClass.ripList(funcClass, link)

#Sort list of beers by mL / $
listOfBeer.sort('valueAlcohol')

#Populate new topTen list to reduce file size
for i in range(0, 10):
    topTenList.append(listOfBeer.list[i])

#Populate new sale list to reduce file size
for i in range(0, listOfBeer.length):
    if(listOfBeer.list[i].sale == 1):
        saleList.append(listOfBeer.list[i])
saleList.sort('salePercent')

#Populate new keg list to reduce file size
for bit in listOfBeer.list:
    if(bit.type == 'Keg'):
        kegList.append(bit)
kegList.sort('value')

#Output list of beers to text summary
with open('dataTaken.txt', 'w+') as f:
    for i in range(0, listOfBeer.length):
        print(listOfBeer.prntSng(i), file=f)

#Output list of beers to JSON
with open('jsonAllData.txt', 'w+') as f:
    print(jsonOutput.dataToFile.toJSON(jsonOutput.dataToFile, listOfBeer), file=f)

with open('top10jsonData.txt', 'w+') as f:
    print(jsonOutput.dataToFile.toJSON(jsonOutput.dataToFile, topTenList), file=f)

with open('jsonSaleData.txt', 'w+') as f:
    print(jsonOutput.dataToFile.toJSON(jsonOutput.dataToFile, saleList), file=f)

with open('jsonKegData.txt', 'w+') as f:
    print(jsonOutput.dataToFile.toJSON(jsonOutput.dataToFile, kegList), file=f)

#Print list of beers
#listOfBeer.prnt()
