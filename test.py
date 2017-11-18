from multiprocessing import Process, Lock, Queue
from time import sleep, time

def work(_queue, procNm):
    l = Lock()
    while True:
        sleep(1)
        nm = _queue.get()
        if nm != 'DONE':
            print(nm)
        else:
            print('Killed: ' + str(procNm))
            break

def main():
    if __name__ == '__main__':
        queue = Queue()
        for i in range(15):
            queue.put(i)
        procs = []

        for i in range(10):
            p = Process(target=work, args=(queue,i))
            p.start()
            procs.append(p)
            queue.put('DONE')

        for pcs in procs:
            pcs.join()
        print('Done.')

main()
