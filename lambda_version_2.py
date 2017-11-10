from time import time, sleep
from urllib.request import urlopen, URLError
from multiprocessing import Process, Queue, Manager
from copy import copy
import json

#Individual beer class
class Beer:
    infOrd = {'type': 0, 'size': 1, 'quantity': 2, 'price': 3, 'sale': 4, 'salePrice': 5, 'salePercent': 6, 'value': 7, 'valAlc': 8}
    retAmt = {'Can': 0, 'Bottle': 0}
    kRetAmt = {58600: 50, 50000:50, 30000:50, 25000: 20, 20000: 20, 12000:20}
    def __init__(self, brnd, nm, tp, sz, qnt, alc, prc, sl, slPrc, picLnk, pgLnk):
        self.brand = brnd
        self.name = nm
        self.alcohol = alc
        self.pictureLink = picLnk
        self.pageLink = pgLnk
        self.rank = 0
        self.main = 0
        #Info format: Type (0), size(1), quantity(2), price(3), sale(4), sale price(5), sale percent(6), value(7), alc value(8)
        self.info = [[tp, sz, qnt, prc, sl, slPrc, 0, 0, 0]] #NOTE: 0s are sale percent, value, and alc value
        self.cnt = 1
        self.salePercent = 0
        calcPrice = prc
        if tp == 'Keg':
            calcPrice -= Beer.kRetAmt[sz] * qnt
        else:
            calcPrice -= Beer.retAmt[tp] * qnt

        if(slPrc != 0):
            calcPrice -= (prc - slPrc)
            self.info[0][6] = (1-slPrc/prc)*100
            self.salePercent = self.info[0][6]
        self.value = round((qnt * sz) / calcPrice, 5)
        self.valAlc = round((qnt * sz * (alc / 100)) / calcPrice, 5)
        self.info[0][7] = self.value
        self.info[0][8] = self.valAlc
        self.isSale = sl == 1
        self.price = calcPrice
    def addBrew(self, tp, sz, qnt, prc, sl, slPrc):
        self.info.append([tp, sz, qnt, prc, sl, slPrc, 0, 0, 0])
        self.cnt = len(self.info)
        offset = len(self.info)-1
        calcPrice = prc
        if tp == 'Keg':
            calcPrice -= Beer.kRetAmt[sz] * qnt
        else:
            calcPrice -= Beer.retAmt[tp] * qnt
        self.info[offset][3] = calcPrice
        if(slPrc != 0):
            calcPrice -= (prc - slPrc)
            self.info[offset][6] = (1-calcPrice/prc)*100
            if self.info[offset][6] > self.salePercent:
                self.salePercent = self.info[offset][6]
        self.info[offset][7] = round((qnt * sz) / calcPrice, 5)
        self.info[offset][8] = round((qnt * sz * (self.alcohol / 100)) / calcPrice, 5)
        if self.info[offset][8] > self.valAlc:
            self.valAlc = self.info[offset][8]
            self.value = self.info[offset][7]
            self.price = self.info[offset][3]
            self.main = offset
        self.isSale = self.isSale or sl == 1
    def pullBAttr(self, attr, val):
        for i, brew in enumerate(self.info):
            delList = []
            if(brew[self.infOrd[attr]] != val):
                delList.append(i)

        if len(delList) == len(self.info):
            return False
        elif len(delList) > 0:
            for i in range(delList[len(delList)-1], 0, -1):
                del self.info[i]
        return True
    def makeMain(self, ind):
        if not ind >= 0 or not len(self.info)-1 >= ind:
            return
        self.price = self.info[ind][3]
        self.value = self.info[ind][7]
        self.valAlc = self.info[ind][8]
        self.main = ind
    def prnt(self):
        print(self.brand + "'s "  + self.name + ' with ' + str(self.alcohol.toFixed(1)) + ' in sizes:  ')
        for brew in self.info:
            if(brew[4] == 1):
                print(brew[2] + ' x ' + brew[1] + ' at ' + brew[5] + ' (' + brew[6] + '% off) or ' + brew[8] + ' mL of alc. /$')
            else:
                print(brew[2] + ' x ' + brew[1] + ' at ' + brew[3] + ' or ' + brew[8] + ' mL of alc. /$')
    def prntAsString(self):
        strng = self.brand + "'s "  + self.name + ' with ' + str(self.alcohol.toFixed(1)) + ' in sizes:  '
        for brew in self.info:
            if(brew[4] == 1):
                strng += brew[2] + ' x ' + brew[1] + ' at ' + brew[5] + ' (' + brew[6] + '% off) or ' + brew[8] + ' mL of alc. /$'
            else:
                strng += brew[2] + ' x ' + brew[1] + ' at ' + brew[3] + ' or ' + brew[8] + ' mL of alc. /$'
        return strng

#List of all beers class
class BeerList:
    def __init__(self):
        self.list = []
        self.length = 0
    def append(self, beerData):
        self.list.append(beerData)
        self.length += beerData.cnt
    def prnt(self):
        for i in range(0, self.length):
            Beer.prnt(self.list[i])
    def sort(self, quant):
        self.list.sort(key=lambda Beer: getattr(Beer, quant), reverse=True)
        for i, brew in enumerate(self.list):
            brew.rank = i + 1
            brew.info.sort(key=lambda list: list[brew.infOrd[quant]], reverse=True)
            brew.makeMain(0)
    def lightSort(self, quant):
        self.list.sort(key=lambda Beer: getattr(Beer, quant), reverse=True)
        for i, brew in enumerate(self.list):
            brew.rank = i
    def insertName(self, beerData, quant):
        for i in range(0, self.length):
            if(i == self.length - 1):
                self.append(beerData)
            elif(getattr(self.list[i], quant) > getattr(beerData, quant)):
                self.list.insert(i, beerData)
                return
    def kegListGen(self):
        kegList = BeerList()
        for brew in self.list:
            mainKeg = -1
            for i in range(0, len(brew.info)-1):
                if brew.info[i][brew.infOrd['type']] == 'Keg':
                    if mainKeg == -1:
                        mainKeg = i
                    elif brew.info[i][7] > brew.info[mainKeg][7]:
                        mainKeg = i
            if mainKeg != -1:
                kegList.append(copy(brew))
                kegList.list[len(kegList.list)-1].makeMain(mainKeg)
        kegList.list.sort(key=lambda Beer: Beer.value, reverse=True)
        for i, brew in enumerate(kegList.list):
            brew.rank = i

        return kegList
    def prntSng(self, ind):
        return Beer.prntAsString(self.list[ind])

def toJSON(listOfBeer):
    jsonString = json.dumps([Beer.__dict__ for Beer in listOfBeer.list])
    return jsonString

def readURL(url):
    success = 3
    while success > 0:
        try:
            raw = urlopen(url)
            success = -1
        except URLError:
            success -= 1
            sleep(1)
            continue
    content = raw.read().decode("utf-8")
    return content

def stripURL():
    manager = Manager()
    link = manager.Queue()
    url = "http://www.thebeerstore.ca/beers/search"

    content = readURL(url)
    start = 0
    point = 0

    while(content.find("brand-link teaser", start + 1) != -1):
        point = content.find("brand-link teaser", start + 1)
        start = content.find("href=", point) + len("href=") + 1
        link.put('http://www.thebeerstore.ca' + content[start:content.find('"', start+1)])

    print('Strip done.')
    return link

def collectInfo(urlLst, retData):
    while True:
        url = urlLst.get()

        if(url != 'DONE'):
            content = readURL(url)
            #Beer picture
            begin = content.find('brand-image-container')
            beer_link_location = content.find('src', begin) + len('src') + 2
            beer_link = content[beer_link_location:content.find('"', beer_link_location)]

            #Beer name
            begin = content.find('only-desktop', begin)
            beer_name_location = content.find('class="page-title"', begin) + len('class="page-title"') + 1
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
            type_location = alcohol_location
            sale = 0

            first = True
            while(content.find('<th class="large">', type_location) != -1):
                type_location = content.find('<th class="large">', type_location + 1) + len('<th class="large">')
                type = content[type_location:content.find('<', type_location)]
                type_end = content.find('</tbody>', type_location + 1)

                quantity_location = content.find('<td class="size">', type_location + 1, type_end)

                while(quantity_location != -1):
                    #Extract Quantity
                    quantity_location += len('<td class="size">')
                    quantity = int(content[quantity_location:content.find('&', quantity_location)-1])

                    #Extract Size
                    size_location = content.find('&', quantity_location + 5) - 7
                    size_location = content.find(' ', size_location)
                    #size_location = content.find(';', quantity_location + 15) + 3 #content.find(type, quantity_location) + len(type) + 1
                    size = int(content[size_location:content.find('&', size_location)])

                    #Extract price
                    price_location = content.find('price', size_location) + len('price') + 3
                    sale_price_location = price_location
                    salePrice = 0
                    if(content.find('sale-price', price_location, price_location + 50) != -1):
                        price_location = content.find('$', price_location) + 1
                        sale_price_location = content.find('sale-price', sale_price_location)
                        sale_price_location = content.find('$', sale_price_location + 1) + 1
                        salePrice = float(content[sale_price_location:content.find('<', sale_price_location)])
                        sale = 1
                    price = float(content[price_location:content.find('<', price_location)])
                    #Calculate next quantity location (and whether it exists)
                    quantity_location = content.find('<td class="size">', quantity_location + 1, type_end)
                    if first == True:
                        brew = Beer(brewer, beer_name, type, int(size), int(quantity), float(alcohol[0]), float(price), sale, salePrice, beer_link, url)
                        first = False
                    else:
                        brew.addBrew(type, size, quantity, price, sale, salePrice)
                    sale = 0

            print('Done ' + brew.name)

            retData.put(brew)
        else:
            break

def ripList(links):
    listOfBeer = BeerList()
    manager = Manager()
    collectedData = manager.Queue()
    procList = []

    for i in range(30):
        proc = Process(target=collectInfo, args=(links, collectedData))
        procList.append(proc)
        proc.start()
        links.put('DONE')

    for proc in procList:
        proc.join()
    collectedData.put('DONE')

    while True:
        brew = collectedData.get()
        if brew != 'DONE':
            listOfBeer.append(brew)
        else:
            break

    return listOfBeer

def connectionCheck():
    try:
        urlopen('http://www.thebeerstore.ca/', timeout=2)
        return True
    except URLError as err:
        return False

def main():
    if __name__ == '__main__' and connectionCheck():
        #Variable declaration
        outputFolder = 'data/'

        #Object instatiation
        listOfBeer = BeerList()
        topTenList = BeerList()
        saleList = BeerList()
        kegList = BeerList()

        start = time()
        #Pull beers and sort
        link = stripURL()     #Strip links for all beer pages
        listOfBeer = ripList(link)    #Pull information from each beer page
        listOfBeer.sort('valAlc')     #Sort list of beers by mL / $

        #Populate new topTen list to reduce its file size
        for i in range(0, 10):
            topTenList.append(copy(listOfBeer.list[i]))

        #Populate new sale list to reduce its file size
        for bit in listOfBeer.list:
            if bit.isSale == 1:
                saleList.append(copy(bit))
        saleList.lightSort('salePercent')

        #Populate keg list to reduce its file size
        kegList = listOfBeer.kegListGen()

        #Output list of beers to JSON
        with open(outputFolder + 'jsonAllData.json', 'w+') as f:
            f.write(toJSON(listOfBeer))

        with open(outputFolder + 'top10jsonData.json', 'w+') as f:
            f.write(toJSON(topTenList))

        with open(outputFolder + 'jsonSaleData.json', 'w+') as f:
            f.write(toJSON(saleList))

        with open(outputFolder + 'jsonKegData.json', 'w+') as f:
            f.write(toJSON(kegList))

    elif __name__ == '__main__':
        print('Connection to The Beer Store failed.')

main()
