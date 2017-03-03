from urllib.request import urlopen

class collection:
    def stripURL(self):
        link = []
        partial_url = "http://www.thebeerstore.ca/beers/search/beer_type--"
        suffix = ('Ale', 'Lager', 'Malt', 'Stout')

        for i in range(0, len(suffix)):
            url = partial_url + suffix[i]
            raw = urlopen(url)
            content = raw.read()
            content = content.decode("utf-8")
            start = 0
            point = 0

            while(content.find("brand-link teaser", start + 1) != -1):
                point = content.find("brand-link teaser", start + 1)
                start = content.find("href=", point) + len("href=") + 1
                link.append('http://www.thebeerstore.ca' + content[start:content.find('"', start+1)])

        print('Strip done.')
