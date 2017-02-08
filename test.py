
class Beer:
    def __init__(self, brnd, nm, sz, qnt, alc):
        self.brand = brnd
        self.name = nm
        self.size = sz
        self.quantity = qnt
        self.alcohol = alc
    def prnt(self):
        print(str(self.quantity) + ' x ' + str(self.size) + 'mL ' + str(self.brand) + ' ' + str(self.name))

KIPA = Beer("Keiths", "India Pale Ale", 500, 24, 5.0)

Beer.prnt(KIPA)
