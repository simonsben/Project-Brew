import beerClass

typeClass = beerClass.Beer
listClass = beerClass.BeerList
brew = typeClass("Brewer", "beer_name", "Can", 473, 12, 9, 25.68, 1, 20, "link.com", "url.com")
brewList = listClass()

for i in range(0, 10):
    brew = typeClass("Brewer", "beer_name"+str(i), "Can", 473, 12, 9, 25.68, (-1)**i, 20, "link.com", "url.com")
    brewList.append(brew)
    if(brewList.list[i].sale == 1):
        print("It's on sale!")
    else:
        print("It's not on sale")


brewList.prnt()

if(brew.sale == 1):
    print("It's on sale!")
else:
    print("It's not on sale")
