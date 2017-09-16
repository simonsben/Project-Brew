import json
import beerClass

class dataToFile:
        def toJSON(self, listOfBeer):
            jsonString = json.dumps([beerClass.Beer.__dict__ for beerClass.Beer in listOfBeer.list])
            return jsonString
