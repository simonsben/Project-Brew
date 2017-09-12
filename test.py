import multiprocessing
import time
from urllib.request import urlopen

def action(b):
    raw = urlopen('http://google.ca/').read()
    print(str(b) + ' done.')
    return b

if __name__ == '__main__':
    start = time.time()
    numP = 50
    arguments = range(numP)

    startN = time.time()
    with multiprocessing.Pool(processes=10) as p:
        result_set = p.map(action, arguments)
    endN = time.time()
    result_set = []

    print('Normal: ' + str(endN - startN))

    #print(len(result_set))
