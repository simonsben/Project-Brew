#Beer definition template

#Individual beer class
class Beer:
    def __init__(self, brnd, nm, sz, qnt, alc, prc):
        self.brand = brnd
        self.name = nm
        self.size = sz
        self.quantity = qnt
        self.alcohol = alc
        self.price = prc
        self.value = (qnt * sz) / prc
        self.valueAlcohol = (qnt * sz * (alc / 100)) / prc
    def prnt(self):
        print(str(self.quantity) + ' x ' + str(self.size) + 'mL ' + str(self.brand) + ' ' + str(self.name))


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
                if(getattr(self.list[i], quant) > getattr(self.list[j], quant)):
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
