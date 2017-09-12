import beerClass
import functionClass
import jsonOutput
import updatedFunctionClass
import time

#Class Instantiation
typeClass = beerClass.Beer
listClass = beerClass.BeerList
funcClass = functionClass.collection
newFuncClass = updatedFunctionClass

#Variable declaration
outputFolder = 'data/'

#Class initalization
listOfBeer = listClass()
newListOfBeer = listClass()
topTenList = listClass()
saleList = listClass()
kegList = listClass()

#Strip links for all beer pages
link = funcClass.stripURL(funcClass)

#Pull information from each beer page
startOriginal = time.time()
listOfBeer = funcClass.ripList(funcClass, link)
endOriginal = time.time()

print('Done first set.')

#New Strip Function
startNew = time.time()
newListOfBeer = newFuncClass.ripList(link)
endNew = time.time()

print('And the times are: ')
print('Original: ' + endOriginal - startOriginal)
print('Remastered '  + endNew - startNew)

print('Check for symmetry: ')
print(listOfBeer.length)
print(newListOfBeer.length)

#Sort list of beers by mL / $
listOfBeer.sort('valueAlcohol')

#Populate new topTen list to reduce file size
for i in range(0, 10):
    topTenList.append(listOfBeer.list[i])

#Populate new sale list to reduce file size
for bit in listOfBeer.list:
    if bit.sale == 1:
        saleList.append(bit)
saleList.sort('salePercent')

#Populate new keg list to reduce file size
for bit in listOfBeer.list:
    if(bit.type == 'Keg'):
        kegList.append(bit)
kegList.sort('value')

#Output list of beers to text summary
with open(outputFolder + 'dataTaken.txt', 'w+') as f:
    for bit in listOfBeer.list:
        print(bit, file=f)

#Output list of beers to JSON
with open(outputFolder + 'jsonAllData.txt', 'w+') as f:
    print(jsonOutput.dataToFile.toJSON(jsonOutput.dataToFile, listOfBeer), file=f)

with open(outputFolder + 'top10jsonData.txt', 'w+') as f:
    print(jsonOutput.dataToFile.toJSON(jsonOutput.dataToFile, topTenList), file=f)

with open(outputFolder + 'jsonSaleData.txt', 'w+') as f:
    print(jsonOutput.dataToFile.toJSON(jsonOutput.dataToFile, saleList), file=f)

with open(outputFolder + 'jsonKegData.txt', 'w+') as f:
    print(jsonOutput.dataToFile.toJSON(jsonOutput.dataToFile, kegList), file=f)
