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

#Example beer information
KIPA = Beer("Keiths", "India Pale Ale", 500, 24, 5.0, 35.49)

#Calling print function
#Beer.prnt(KIPA)

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


#Declaration of beer list
listOfBeer = BeerList()

#Generation of example beer list
print("List of beer: ")
for i in range(20, 25):
    KIPA = Beer("Keiths", "India Pale Ale", i*15, 24, 5.0, i*12.35)
    listOfBeer.append(KIPA)

KIPA = Beer("Aeiths", "India Pale Ale", 150, 24, 5.0, 12.23)
listOfBeer.append(KIPA)
KIPA = Beer("Deiths", "India Pale Ale", 150, 24, 5.0, 12.45)
listOfBeer.append(KIPA)
KIPA = Beer("Peiths", "India Pale Ale", 150, 24, 5.0, 13.42)
listOfBeer.append(KIPA)
KIPA = Beer("Qeiths", "India Pale Ale", 1500, 24, 5.0, 5.32)
listOfBeer.append(KIPA)

#Printing of example beer list
listOfBeer.prnt()

print(' ')
print(' ')
print(' Sorted: ')
listOfBeer.sort("value")
listOfBeer.prnt()

'''
#Example insert into sorted list
print(' ')
print(' ')
print(' Sorted: ')
KIPA = Beer("Meiths", "India Pale Ale", 1500, 24, 5.0, 43.51)
listOfBeer.insertName(KIPA, "brand")
listOfBeer.prnt()
'''
