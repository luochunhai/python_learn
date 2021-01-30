import threading
import time


def run(name):
    time.sleep(2)
    print("hello,I am thread {} ".format(name))


def main():
    threads = []
    for i in range(5):
        t = threading.Thread(target=run, args=(i,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


if __name__ == '__main__':
    print('start')
    main()
    print('end')
