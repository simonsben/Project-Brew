import json
import beerClass


class dataToFile:
        def toJSON(self, listOfBeer):
            beerObject = beerClass.Beer
            jsonString = json.dumps([beerObject.__dict__ for beerObject in listOfBeer.list])
            #print(jsonString)
            return jsonString
