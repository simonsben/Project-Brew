import beerClass
import functionClass as funcClass
import jsonOutput

if __name__ == '__main__' and funcClass.connectionCheck():
    #Class Instantiation
    typeClass = beerClass.Beer
    listClass = beerClass.BeerList

    #Variable declaration
    outputFolder = 'data/'

    #Object instatiation
    listOfBeer = listClass()
    topTenList = listClass()
    saleList = listClass()
    kegList = listClass()

    #Pull beers and sort
    link = funcClass.stripURL()     #Strip links for all beer pages
    listOfBeer = funcClass.ripList(link)    #Pull information from each beer page
    listOfBeer.sort('valueAlcohol')     #Sort list of beers by mL / $
    print('Collection done.')

    #Populate new topTen list to reduce its file size
    for i in range(0, 10):
        topTenList.append(listOfBeer.list[i])

    #Populate new sale list to reduce its file size
    for bit in listOfBeer.list:
        if bit.sale == 1:
            saleList.append(bit)
    saleList.sort('salePercent')

    #Populate keg list to reduce its file size
    for bit in listOfBeer.list:
        if(bit.type == 'Keg'):
            kegList.append(bit)
    kegList.sort('value')

    #Output list of beers to text summary
    with open(outputFolder + 'dataTaken.txt', 'w+') as f:
        for bit in listOfBeer.list:
            print(bit.prntAsString, file=f)

    #Output list of beers to JSON
    with open(outputFolder + 'jsonAllData.txt', 'w+') as f:
        print(jsonOutput.dataToFile.toJSON(jsonOutput.dataToFile, listOfBeer), file=f)

    with open(outputFolder + 'top10jsonData.txt', 'w+') as f:
        print(jsonOutput.dataToFile.toJSON(jsonOutput.dataToFile, topTenList), file=f)

    with open(outputFolder + 'jsonSaleData.txt', 'w+') as f:
        print(jsonOutput.dataToFile.toJSON(jsonOutput.dataToFile, saleList), file=f)

    with open(outputFolder + 'jsonKegData.txt', 'w+') as f:
        print(jsonOutput.dataToFile.toJSON(jsonOutput.dataToFile, kegList), file=f)

elif __name__ == '__main__':
    print('Connection to The Beer Store failed.')
