#Beer definition template

#Individual beer class
class Beer:
    def __init__(self, brnd, nm, tp, sz, qnt, alc, prc, sl):
        self.brand = brnd
        self.name = nm
        self.type = tp
        self.size = sz
        self.quantity = qnt
        self.alcohol = alc
        self.price = prc
        self.sale = sl
        self.value = round((qnt * sz) / prc, 5)
        self.valueAlcohol = round((qnt * sz * (alc / 100)) / prc, 5)
    def prnt(self):
        print(str(self.quantity) + ' x ' + str(self.size) + 'mL ' + str(self.type) + ' ' + str(self.brand) + ', ' + str(self.name) + ' ' + str(self.price) + '$')
    def prntAsString(self):
        #strng = str(self.quantity) + ' x ' + str(self.size) + 'mL ' + str(self.type) + ' ' + str(self.brand) + ' ' + str(self.name) + ' ' + str(self.price) + '$'
        strng = str(self.quantity) + ' x ' + str(self.size) + 'mL ' + str(self.type) + ' ' + str(self.brand) + ', ' + str(self.name) + ' ' + str(self.valueAlcohol) + ' mL alcohol/$'
        return strng

#List of all beers class
class BeerList:
    def __init__(self):
        self.list = []
        self.length = 0
    def append(self, beerData):
        self.list.append(beerData)
        self.length += 1
    def prnt(self):
        for i in range(0, self.length):
            Beer.prnt(self.list[i])
    def sort(self, quant):
        for i in range(0, self.length):
            for j in range(i, self.length):
                if(getattr(self.list[i], quant) < getattr(self.list[j], quant)):
                    swap =  self.list[i]
                    self.list[i] = self.list[j]
                    self.list[j] = swap
    def insertName(self, beerData, quant):
        for i in range(0, self.length):
            if(i == self.length - 1):
                self.append(beerData)
            elif(getattr(self.list[i], quant) > getattr(beerData, quant)):
                self.list.insert(i, beerData)
                return
    def prntSng(self, ind):
        return Beer.prntAsString(self.list[ind])

