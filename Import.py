from urllib.request import urlopen

url = "http://www.thebeerstore.ca/beers/1857-kolsch-style-ale"
raw = urlopen(url)
content = raw.read()
#content = content.decode("utf-8")

data = open("temp.dat", "w")
data.write(content)
data.close()
