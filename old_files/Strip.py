from urllib.request import urlopen

link = []
url = "http://www.thebeerstore.ca/beers/search/beer_type--"

content = urlopen(url).read()
content = content.decode("utf-8")
start = 0
point = 0

while(content.find("brand-link teaser", start + 1) != -1):
    point = content.find("brand-link teaser", start + 1)
    start = content.find("href=", point) + len("href=") + 1
    link.append('http://www.thebeerstore.ca' + content[start:content.find('"', start+1)])

print('Strip done.')
