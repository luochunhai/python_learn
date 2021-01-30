import multiprocessing
from multiprocessing import Process


def test(name):
    tname = multiprocessing.current_process().name
    print("{} is starting, worker is {}".format(tname, name))


if __name__ == '__main__':
    numlist = []
    for i in range(5):
        p = Process(target=test, args=(i,))
        numlist.append(p)
        p.start()
        p.join()

    print('=======主')
