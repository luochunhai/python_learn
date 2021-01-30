# coroutine 协程

import requests
import gevent

urls = ["http://www.baidu.com", "https://www.sogou.com", "http://www.imooc.com"]


def run(url):
    print("url={}".format(url))
    res = requests.get(url)
    print("url bytes is {}".format(len(res.content)))


if __name__ == '__main__':
    jobs = [gevent.spawn(run, url) for url in urls]
    gevent.joinall(jobs)
