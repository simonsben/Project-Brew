import urllib2
import csv

link = []
partial_url = "http://www.thebeerstore.ca/beers/search/beer_type--"
suffix = ('Ale', 'Lager', 'Malt', 'Stout')

for i in range(0, 1):
    url = partial_url + suffix[i]
    raw = urllib2.urlopen(url)
    content = raw.read()
    start = 0
    point = 0

    page = open("temp.dat", "w")
    page.write(content)
    while(content.find("brand-link teaser", start + 1) != -1):
        point = content.find("brand-link teaser", start + 1)
        start = content.find("href=", point) + len("href=") + 1
        link.append('http://www.thebeerstore.ca' + content[start:content.find('"', start+1)])

page.close()

with open('Links.csv', 'wb') as link_file:
    writer = csv.writer(link_file)
    writer.writerow(link)
