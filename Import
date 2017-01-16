import urllib2

url = "http://www.thebeerstore.ca/beers/keiths"
raw = urllib2.urlopen(url)
content = raw.read()

data = open("temp.dat", "w")
data.write(content)
data.close()
