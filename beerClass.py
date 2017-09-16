from copy import copy

#Individual beer class
class Beer:
    infOrd = {'type': 0, 'size': 1, 'quantity': 2, 'price': 3, 'sale': 4, 'salePrice': 5, 'salePercent': 6, 'value': 7, 'valAlc': 8}
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
        if(slPrc != 0):
            calcPrice = slPrc
            self.info[0][6] = (1-slPrc/prc)*100
            self.salePercent = self.info[0][6]

        self.value = round((qnt * sz) / calcPrice, 5)
        self.valAlc = round((qnt * sz * (alc / 100)) / calcPrice, 5)
        self.info[0][7] = self.value
        self.info[0][8] = self.valAlc
        self.isSale = sl == 1
        self.price = prc
    def addBrew(self, tp, sz, qnt, prc, sl, slPrc):
        self.info.append([tp, sz, qnt, prc, sl, slPrc, 0, 0, 0])
        self.cnt = len(self.info)
        offset = len(self.info)-1
        calcPrice = prc
        if(slPrc != 0):
            calcPrice = slPrc
            self.info[offset][6] = (1-slPrc/prc)*100
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
            brew.info.sort(key=lambda list: brew.infOrd[quant], reverse=True)
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
                if brew.info[i][brew.infOrd['type']] == 'keg':
                    if mainKeg == -1:
                        mainKeg = i
                    elif brew.info[i][7] > brew.info[mainKeg][7]:
                        mainKeg = i
            if mainKeg != -1:
                kegList.append(copy(brew))
                kegList.list[len(kegList.list)-1].makeMain(len(kegList.list)-1)
        kegList.list.sort(key=lambda Beer: Beer.value, reverse=True)
        return  kegList
    def prntSng(self, ind):
        return Beer.prntAsString(self.list[ind])

